from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_encryption_keyboard
from states import AESCipher
from crypto_utils import generate_aes_key, aes_encrypt, aes_decrypt

async def aes_cipher_menu(message: types.Message, state: FSMContext):
    # Сначала очищаем предыдущее состояние, если было
    await state.clear()
    # Устанавливаем новое состояние
    await state.set_state(AESCipher.choosing_mode)
    await message.reply("Выберите режим для AES шифрования:", reply_markup=get_encryption_keyboard())

async def aes_generate_key(message: types.Message, state: FSMContext):
    key = generate_aes_key()
    await message.reply(
        "🔑 Ваш AES ключ сгенерирован:\n"
        f"<code>{key}</code>\n\n"
        "Сохраните этот ключ для последующего дешифрования!",
        parse_mode=ParseMode.HTML
    )
    await state.clear()
    await message.reply("Вернулись в главное меню.", reply_markup=get_main_keyboard())

async def aes_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(AESCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования:", reply_markup=get_main_keyboard())

async def process_aes_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(aes_text=message.text)
    await state.set_state(AESCipher.waiting_for_key_encrypt)
    await message.reply("Введите AES ключ для шифрования:")

async def process_aes_key_encrypt(message: types.Message, state: FSMContext):
    key = message.text.strip()
    data = await state.get_data()
    text = data.get("aes_text")
    result = aes_encrypt(text, key)
    
    if result.startswith("Ошибка"):
        await message.reply(f"{result}\nПопробуйте еще раз.", reply_markup=get_main_keyboard())
    else:
        await message.reply(
            "✅ Текст успешно зашифрован AES:\n"
            f"<code>{result}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    await state.clear()

async def aes_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(AESCipher.waiting_for_text_decrypt)
    await message.reply("Введите зашифрованный AES текст:", reply_markup=get_main_keyboard())

async def process_aes_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(aes_text=message.text)
    await state.set_state(AESCipher.waiting_for_key_decrypt)
    await message.reply("Введите AES ключ для дешифрования:")

async def process_aes_key_decrypt(message: types.Message, state: FSMContext):
    key = message.text.strip()
    data = await state.get_data()
    text = data.get("aes_text")
    result = aes_decrypt(text, key)
    
    if result.startswith("Ошибка"):
        await message.reply(f"{result}\nПопробуйте еще раз.", reply_markup=get_main_keyboard())
    else:
        await message.reply(
            "✅ Текст успешно расшифрован AES:\n"
            f"{result}",
            reply_markup=get_main_keyboard()
        )
    await state.clear()

def register_aes_handlers(dp):
    dp.message.register(aes_cipher_menu, lambda message: message.text == "🔐 AES шифрование")
    dp.message.register(aes_generate_key, 
                       lambda message: message.text == "Сгенерировать ключ", 
                       StateFilter(AESCipher.choosing_mode))
    dp.message.register(aes_encryption_start, 
                       lambda message: message.text == "Шифрование", 
                       StateFilter(AESCipher.choosing_mode))
    dp.message.register(process_aes_text_encrypt, StateFilter(AESCipher.waiting_for_text_encrypt))
    dp.message.register(process_aes_key_encrypt, StateFilter(AESCipher.waiting_for_key_encrypt))
    dp.message.register(aes_decryption_start, 
                       lambda message: message.text == "Дешифрование", 
                       StateFilter(AESCipher.choosing_mode))
    dp.message.register(process_aes_text_decrypt, StateFilter(AESCipher.waiting_for_text_decrypt))
    dp.message.register(process_aes_key_decrypt, StateFilter(AESCipher.waiting_for_key_decrypt))
    
    return dp 