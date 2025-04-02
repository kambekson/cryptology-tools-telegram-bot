from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_encryption_keyboard
from states import DESCipher
from crypto_utils import generate_des_key, des_encrypt, des_decrypt

async def des_cipher_menu(message: types.Message, state: FSMContext):
    # Сначала очищаем предыдущее состояние, если было
    await state.clear()
    # Устанавливаем новое состояние
    await state.set_state(DESCipher.choosing_mode)
    await message.reply("Выберите режим для DES шифрования:", reply_markup=get_encryption_keyboard())

async def des_generate_key(message: types.Message, state: FSMContext):
    key = generate_des_key()
    await message.reply(
        "🔑 Ваш DES ключ сгенерирован:\n"
        f"<code>{key}</code>\n\n"
        "Сохраните этот ключ для последующего дешифрования!",
        parse_mode=ParseMode.HTML
    )
    await state.clear()
    await message.reply("Вернулись в главное меню.", reply_markup=get_main_keyboard())

async def des_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(DESCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования:", reply_markup=get_main_keyboard())

async def process_des_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(des_text=message.text)
    await state.set_state(DESCipher.waiting_for_key_encrypt)
    await message.reply("Введите DES ключ для шифрования:")

async def process_des_key_encrypt(message: types.Message, state: FSMContext):
    key = message.text.strip()
    data = await state.get_data()
    text = data.get("des_text")
    result = des_encrypt(text, key)
    
    if result.startswith("Ошибка"):
        await message.reply(f"{result}\nПопробуйте еще раз.", reply_markup=get_main_keyboard())
    else:
        await message.reply(
            "✅ Текст успешно зашифрован DES:\n"
            f"<code>{result}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    await state.clear()

async def des_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(DESCipher.waiting_for_text_decrypt)
    await message.reply("Введите зашифрованный DES текст:", reply_markup=get_main_keyboard())

async def process_des_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(des_text=message.text)
    await state.set_state(DESCipher.waiting_for_key_decrypt)
    await message.reply("Введите DES ключ для дешифрования:")

async def process_des_key_decrypt(message: types.Message, state: FSMContext):
    key = message.text.strip()
    data = await state.get_data()
    text = data.get("des_text")
    result = des_decrypt(text, key)
    
    if result.startswith("Ошибка"):
        await message.reply(f"{result}\nПопробуйте еще раз.", reply_markup=get_main_keyboard())
    else:
        await message.reply(
            "✅ Текст успешно расшифрован DES:\n"
            f"{result}",
            reply_markup=get_main_keyboard()
        )
    await state.clear()

def register_des_handlers(dp):
    dp.message.register(des_cipher_menu, lambda message: message.text == "🔏 DES шифрование")
    dp.message.register(des_generate_key, 
                       lambda message: message.text == "Сгенерировать ключ", 
                       StateFilter(DESCipher.choosing_mode))
    dp.message.register(des_encryption_start, 
                       lambda message: message.text == "Шифрование", 
                       StateFilter(DESCipher.choosing_mode))
    dp.message.register(process_des_text_encrypt, StateFilter(DESCipher.waiting_for_text_encrypt))
    dp.message.register(process_des_key_encrypt, StateFilter(DESCipher.waiting_for_key_encrypt))
    dp.message.register(des_decryption_start, 
                       lambda message: message.text == "Дешифрование", 
                       StateFilter(DESCipher.choosing_mode))
    dp.message.register(process_des_text_decrypt, StateFilter(DESCipher.waiting_for_text_decrypt))
    dp.message.register(process_des_key_decrypt, StateFilter(DESCipher.waiting_for_key_decrypt))
    
    return dp 