from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from keyboards import get_encryption_keyboard, get_main_keyboard
from states import EllipticState
from crypto_utils import generate_elliptic_keys, sign_message_elliptic, verify_signature_elliptic

async def elliptic_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(EllipticState.choosing_mode)
    await message.reply("Выберите режим для эллиптической криптографии:", reply_markup=get_encryption_keyboard())

async def generate_keys(message: types.Message, state: FSMContext):
    private_key, public_key = generate_elliptic_keys()
    await message.reply(f"🔑 Приватный ключ:\n{private_key}\n\n🔐 Публичный ключ:\n{public_key}", reply_markup=get_main_keyboard())
    await state.clear()

async def start_signing(message: types.Message, state: FSMContext):
    await state.set_state(EllipticState.waiting_for_text_to_sign)
    await message.reply("Введите текст, который нужно подписать:")

async def process_sign_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(EllipticState.waiting_for_private_key)
    await message.reply("Введите приватный ключ (hex):")

async def process_private_key(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    signature = sign_message_elliptic(text, message.text.strip())
    await message.reply(f"📩 Подпись:\n{signature}", reply_markup=get_main_keyboard())
    await state.clear()

async def start_verification(message: types.Message, state: FSMContext):
    await state.set_state(EllipticState.waiting_for_text_verify)
    await message.reply("Введите текст для проверки подписи:")

async def process_verify_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(EllipticState.waiting_for_signature)
    await message.reply("Введите подпись (base64):")

async def process_signature(message: types.Message, state: FSMContext):
    await state.update_data(signature=message.text)
    await state.set_state(EllipticState.waiting_for_public_key)
    await message.reply("Введите публичный ключ (hex):")

async def process_public_key(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    signature = data.get("signature")
    valid = verify_signature_elliptic(text, signature, message.text.strip())
    if valid:
        await message.reply("✅ Подпись подтверждена!", reply_markup=get_main_keyboard())
    else:
        await message.reply("❌ Подпись недействительна.", reply_markup=get_main_keyboard())
    await state.clear()

def register_elliptic_handlers(dp):
    dp.message.register(elliptic_menu, lambda m: m.text == "🧮 Эллиптическая криптография")
    dp.message.register(generate_keys, lambda m: m.text == "Сгенерировать ключ", StateFilter(EllipticState.choosing_mode))
    dp.message.register(start_signing, lambda m: m.text == "Шифрование", StateFilter(EllipticState.choosing_mode))
    dp.message.register(process_sign_text, StateFilter(EllipticState.waiting_for_text_to_sign))
    dp.message.register(process_private_key, StateFilter(EllipticState.waiting_for_private_key))
    dp.message.register(start_verification, lambda m: m.text == "Дешифрование", StateFilter(EllipticState.choosing_mode))
    dp.message.register(process_verify_text, StateFilter(EllipticState.waiting_for_text_verify))
    dp.message.register(process_signature, StateFilter(EllipticState.waiting_for_signature))
    dp.message.register(process_public_key, StateFilter(EllipticState.waiting_for_public_key))
    return dp
