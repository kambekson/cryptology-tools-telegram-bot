from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Основная клавиатура
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🔍 Сгенерировать простое число"))
    builder.add(KeyboardButton(text="🔐 Шифр цезаря"))
    builder.add(KeyboardButton(text="🔑 Шифр с использованием кодового слова"))
    builder.add(KeyboardButton(text="📝 Анализатор текста"))
    builder.add(KeyboardButton(text="🔒 RSA шифрование"))
    builder.add(KeyboardButton(text="🔏 DES шифрование"))
    builder.add(KeyboardButton(text="🔐 AES шифрование"))
    builder.add(KeyboardButton(text="❓ Помощь"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)

# Клавиатура для выбора диапазона (для простых чисел)
def get_range_keyboard():
    builder = ReplyKeyboardBuilder()
    ranges = [
        "100-1000",
        "1000-10000",
        "10000-100000",
        "100000-1000000",
        "1000000-10000000",
        "10000000-100000000"
    ]
    for range_text in ranges:
        builder.add(KeyboardButton(text=range_text))
    builder.add(KeyboardButton(text="🔙 Вернуться"))
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)

# Клавиатуры для шифрования
def get_caesar_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Шифрование"))
    builder.add(KeyboardButton(text="Дешифрование"))
    builder.add(KeyboardButton(text="🔙 Вернуться"))
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_keyword_cipher_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Шифрование"))
    builder.add(KeyboardButton(text="Дешифрование"))
    builder.add(KeyboardButton(text="🔙 Вернуться"))
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_encryption_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Шифрование"))
    builder.add(KeyboardButton(text="Дешифрование"))
    builder.add(KeyboardButton(text="Сгенерировать ключ"))
    builder.add(KeyboardButton(text="🔙 Вернуться"))
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True) 