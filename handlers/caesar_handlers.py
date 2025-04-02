from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from keyboards import get_main_keyboard, get_caesar_keyboard
from states import CaesarCipher
from crypto_utils import caesar_encrypt_russian, caesar_decrypt_russian

async def caesar_cipher_menu(message: types.Message, state: FSMContext):
    await state.set_state(CaesarCipher.choosing_mode)
    await message.reply("Выберите режим для шифра Цезаря:", reply_markup=get_caesar_keyboard())

async def caesar_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(CaesarCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования (на русском языке):", reply_markup=get_main_keyboard())

async def process_caesar_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(caesar_text=message.text)
    await state.set_state(CaesarCipher.waiting_for_key_encrypt)
    await message.reply("Введите числовой ключ для шифрования:")

async def process_caesar_key_encrypt(message: types.Message, state: FSMContext):
    try:
        key = int(message.text.strip())
        data = await state.get_data()
        text = data.get("caesar_text")
        result = caesar_encrypt_russian(text, key)
        await message.reply(f"Результат шифрования: {result}", reply_markup=get_main_keyboard())
    except ValueError:
        await message.reply("Ошибка! Ключ должен быть числом. Попробуйте еще раз.")
    await state.clear()

async def caesar_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(CaesarCipher.waiting_for_text_decrypt)
    await message.reply("Введите текст для дешифрования (на русском языке):", reply_markup=get_main_keyboard())

async def process_caesar_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(caesar_text=message.text)
    await state.set_state(CaesarCipher.waiting_for_key_decrypt)
    await message.reply("Введите числовой ключ для дешифрования:")

async def process_caesar_key_decrypt(message: types.Message, state: FSMContext):
    try:
        key = int(message.text.strip())
        data = await state.get_data()
        text = data.get("caesar_text")
        result = caesar_decrypt_russian(text, key)
        await message.reply(f"Результат дешифрования: {result}", reply_markup=get_main_keyboard())
    except ValueError:
        await message.reply("Ошибка! Ключ должен быть числом. Попробуйте еще раз.")
    await state.clear()

def register_caesar_handlers(dp):
    dp.message.register(caesar_cipher_menu, lambda message: message.text == "🔐 Шифр цезаря")
    dp.message.register(caesar_encryption_start, 
                       lambda message: message.text == "Шифрование", 
                       StateFilter(CaesarCipher.choosing_mode))
    dp.message.register(process_caesar_text_encrypt, StateFilter(CaesarCipher.waiting_for_text_encrypt))
    dp.message.register(process_caesar_key_encrypt, StateFilter(CaesarCipher.waiting_for_key_encrypt))
    dp.message.register(caesar_decryption_start, 
                       lambda message: message.text == "Дешифрование", 
                       StateFilter(CaesarCipher.choosing_mode))
    dp.message.register(process_caesar_text_decrypt, StateFilter(CaesarCipher.waiting_for_text_decrypt))
    dp.message.register(process_caesar_key_decrypt, StateFilter(CaesarCipher.waiting_for_key_decrypt))
    
    return dp 