from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from keyboards import get_main_keyboard, get_keyword_cipher_keyboard
from states import KeywordCipher
from crypto_utils import vigenere_encrypt_russian, vigenere_decrypt_russian

async def keyword_cipher_menu(message: types.Message, state: FSMContext):
    # Сначала очищаем предыдущее состояние, если было
    await state.clear()
    # Устанавливаем новое состояние
    await state.set_state(KeywordCipher.choosing_mode)
    await message.reply("Выберите режим для шифра с использованием кодового слова:",
                       reply_markup=get_keyword_cipher_keyboard())

async def keyword_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(KeywordCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования (на русском языке):", reply_markup=get_main_keyboard())

async def process_keyword_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(keyword_text=message.text)
    await state.set_state(KeywordCipher.waiting_for_keyword_encrypt)
    await message.reply("Введите кодовое слово для шифрования:")

async def process_keyword_encrypt(message: types.Message, state: FSMContext):
    keyword = message.text.strip()
    data = await state.get_data()
    text = data.get("keyword_text")
    result = vigenere_encrypt_russian(text, keyword)
    await message.reply(f"Результат шифрования: {result}", reply_markup=get_main_keyboard())
    await state.clear()

async def keyword_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(KeywordCipher.waiting_for_text_decrypt)
    await message.reply("Введите текст для дешифрования (на русском языке):", reply_markup=get_main_keyboard())

async def process_keyword_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(keyword_text=message.text)
    await state.set_state(KeywordCipher.waiting_for_keyword_decrypt)
    await message.reply("Введите кодовое слово для дешифрования:")

async def process_keyword_decrypt(message: types.Message, state: FSMContext):
    keyword = message.text.strip()
    data = await state.get_data()
    text = data.get("keyword_text")
    result = vigenere_decrypt_russian(text, keyword)
    await message.reply(f"Результат дешифрования: {result}", reply_markup=get_main_keyboard())
    await state.clear()

def register_keyword_handlers(dp):
    dp.message.register(keyword_cipher_menu, lambda message: message.text == "🔑 Шифр с кодовым словом")
    dp.message.register(keyword_encryption_start, 
                       lambda message: message.text == "Шифрование", 
                       StateFilter(KeywordCipher.choosing_mode))
    dp.message.register(process_keyword_text_encrypt, StateFilter(KeywordCipher.waiting_for_text_encrypt))
    dp.message.register(process_keyword_encrypt, StateFilter(KeywordCipher.waiting_for_keyword_encrypt))
    dp.message.register(keyword_decryption_start, 
                       lambda message: message.text == "Дешифрование", 
                       StateFilter(KeywordCipher.choosing_mode))
    dp.message.register(process_keyword_text_decrypt, StateFilter(KeywordCipher.waiting_for_text_decrypt))
    dp.message.register(process_keyword_decrypt, StateFilter(KeywordCipher.waiting_for_keyword_decrypt))
    
    return dp 