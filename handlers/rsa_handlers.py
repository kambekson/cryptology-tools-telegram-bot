from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_encryption_keyboard
from states import RSACipher
from crypto_utils import generate_rsa_keys, rsa_encrypt, rsa_decrypt

async def rsa_cipher_menu(message: types.Message, state: FSMContext):
    # Сначала очищаем предыдущее состояние, если было
    await state.clear()
    # Устанавливаем новое состояние
    await state.set_state(RSACipher.choosing_mode)
    await message.reply("Выберите режим для RSA шифрования:", reply_markup=get_encryption_keyboard())

async def rsa_generate_keys(message: types.Message, state: FSMContext):
    await message.reply("Генерирую RSA ключи, пожалуйста, подождите...")
    private_key, public_key = generate_rsa_keys()
    
    await message.reply(
        "🔑 Ваши RSA ключи сгенерированы:\n\n"
        "Приватный ключ (храните в тайне!):\n"
        f"<code>{private_key}</code>\n\n"
        "Публичный ключ (для шифрования):\n"
        f"<code>{public_key}</code>",
        parse_mode=ParseMode.HTML
    )
    await state.clear()
    await message.reply("Вернулись в главное меню.", reply_markup=get_main_keyboard())

async def rsa_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(RSACipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования:", reply_markup=get_main_keyboard())

async def process_rsa_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(rsa_text=message.text)
    await state.set_state(RSACipher.waiting_for_key_encrypt)
    await message.reply(
        "Введите публичный ключ RSA для шифрования:\n"
        "(начинается с -----BEGIN PUBLIC KEY-----)"
    )

async def process_rsa_key_encrypt(message: types.Message, state: FSMContext):
    public_key = message.text.strip()
    data = await state.get_data()
    text = data.get("rsa_text")
    result = rsa_encrypt(text, public_key)
    
    if result.startswith("Ошибка"):
        await message.reply(f"{result}\nПопробуйте еще раз.", reply_markup=get_main_keyboard())
    else:
        await message.reply(
            "✅ Текст успешно зашифрован RSA:\n"
            f"<code>{result}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    await state.clear()

async def rsa_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(RSACipher.waiting_for_text_decrypt)
    await message.reply("Введите зашифрованный RSA текст:", reply_markup=get_main_keyboard())

async def process_rsa_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(rsa_text=message.text)
    await state.set_state(RSACipher.waiting_for_key_decrypt)
    await message.reply(
        "Введите приватный ключ RSA для дешифрования:\n"
        "(начинается с -----BEGIN RSA PRIVATE KEY-----)"
    )

async def process_rsa_key_decrypt(message: types.Message, state: FSMContext):
    private_key = message.text.strip()
    data = await state.get_data()
    text = data.get("rsa_text")
    result = rsa_decrypt(text, private_key)
    
    if result.startswith("Ошибка"):
        await message.reply(f"{result}\nПопробуйте еще раз.", reply_markup=get_main_keyboard())
    else:
        await message.reply(
            "✅ Текст успешно расшифрован RSA:\n"
            f"{result}",
            reply_markup=get_main_keyboard()
        )
    await state.clear()

def register_rsa_handlers(dp):
    dp.message.register(rsa_cipher_menu, lambda message: message.text == "🔒 RSA шифрование")
    dp.message.register(rsa_generate_keys, 
                       lambda message: message.text == "Сгенерировать ключ", 
                       StateFilter(RSACipher.choosing_mode))
    dp.message.register(rsa_encryption_start, 
                       lambda message: message.text == "Шифрование", 
                       StateFilter(RSACipher.choosing_mode))
    dp.message.register(process_rsa_text_encrypt, StateFilter(RSACipher.waiting_for_text_encrypt))
    dp.message.register(process_rsa_key_encrypt, StateFilter(RSACipher.waiting_for_key_encrypt))
    dp.message.register(rsa_decryption_start, 
                       lambda message: message.text == "Дешифрование", 
                       StateFilter(RSACipher.choosing_mode))
    dp.message.register(process_rsa_text_decrypt, StateFilter(RSACipher.waiting_for_text_decrypt))
    dp.message.register(process_rsa_key_decrypt, StateFilter(RSACipher.waiting_for_key_decrypt))
    
    return dp 