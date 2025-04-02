import random
import asyncio
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Cipher import PKCS1_OAEP
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from sympy import isprime

# Импорты для работы с состояниями
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

API_TOKEN = '7089277164:AAHoJMAOSpMnD3-Pso90EKmEN9oj19e-FpQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Основная клавиатура с кнопками, где кнопка "❓ Помощь" теперь в конце

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


# Клавиатуры для меню шифрования
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

# 2. ДОБАВИТЬ В СЕКЦИЮ КЛАВИАТУР (после функции get_keyword_cipher_keyboard())
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🔍 Сгенерировать простое число"))
    builder.add(KeyboardButton(text="🔐 Шифр цезаря"))
    builder.add(KeyboardButton(text="🔑 Шифр с использованием кодового слова"))
    builder.add(KeyboardButton(text="📝 Анализатор текста"))
    # Добавляем новые кнопки для RSA, DES и AES
    builder.add(KeyboardButton(text="🔒 RSA шифрование"))
    builder.add(KeyboardButton(text="🔏 DES шифрование"))
    builder.add(KeyboardButton(text="🔐 AES шифрование"))
    builder.add(KeyboardButton(text="❓ Помощь"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def get_encryption_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Шифрование"))
    builder.add(KeyboardButton(text="Дешифрование"))
    builder.add(KeyboardButton(text="Сгенерировать ключ"))
    builder.add(KeyboardButton(text="🔙 Вернуться"))
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

# Функции для генерации простых чисел
def generate_random_number(min_value, max_value):
    return random.randint(min_value, max_value)


def is_prime_rabin_miller(n):
    return isprime(n)


def generate_random_prime(min_value, max_value):
    while True:
        num = generate_random_number(min_value, max_value)
        if is_prime_rabin_miller(num):
            return num


# Функции шифрования/дешифрования с использованием русского алфавита
def caesar_encrypt_russian(text, key):
    result = ""
    alphabet_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    alphabet_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    for char in text:
        if char in alphabet_lower:
            idx = alphabet_lower.index(char)
            new_idx = (idx + key) % len(alphabet_lower)
            result += alphabet_lower[new_idx]
        elif char in alphabet_upper:
            idx = alphabet_upper.index(char)
            new_idx = (idx + key) % len(alphabet_upper)
            result += alphabet_upper[new_idx]
        else:
            result += char
    return result


def caesar_decrypt_russian(text, key):
    return caesar_encrypt_russian(text, -key)


def vigenere_encrypt_russian(text, keyword):
    result = ""
    alphabet_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    alphabet_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    keyword_lower = keyword.lower()
    j = 0
    for char in text:
        if char in alphabet_lower:
            shift = alphabet_lower.index(keyword_lower[j % len(keyword_lower)])
            idx = alphabet_lower.index(char)
            new_idx = (idx + shift) % len(alphabet_lower)
            result += alphabet_lower[new_idx]
            j += 1
        elif char in alphabet_upper:
            shift = alphabet_lower.index(keyword_lower[j % len(keyword_lower)])
            idx = alphabet_upper.index(char)
            new_idx = (idx + shift) % len(alphabet_upper)
            result += alphabet_upper[new_idx]
            j += 1
        else:
            result += char
    return result


def vigenere_decrypt_russian(text, keyword):
    result = ""
    alphabet_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    alphabet_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    keyword_lower = keyword.lower()
    j = 0
    for char in text:
        if char in alphabet_lower:
            shift = alphabet_lower.index(keyword_lower[j % len(keyword_lower)])
            idx = alphabet_lower.index(char)
            new_idx = (idx - shift) % len(alphabet_lower)
            result += alphabet_lower[new_idx]
            j += 1
        elif char in alphabet_upper:
            shift = alphabet_lower.index(keyword_lower[j % len(keyword_lower)])
            idx = alphabet_upper.index(char)
            new_idx = (idx - shift) % len(alphabet_upper)
            result += alphabet_upper[new_idx]
            j += 1
        else:
            result += char
    return result

# 4. ДОБАВИТЬ ФУНКЦИИ ШИФРОВАНИЯ (после функций vigenere_decrypt_russian())
# Функции для RSA шифрования
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode('utf-8')
    public_key = key.publickey().export_key().decode('utf-8')
    return private_key, public_key


def rsa_encrypt(message, public_key_str):
    try:
        public_key = RSA.import_key(public_key_str)
        cipher = PKCS1_OAEP.new(public_key)
        # Для поддержки длинных сообщений, разделяем их на части
        message_bytes = message.encode('utf-8')
        chunk_size = 200  # Размер сегмента для шифрования
        encrypted = []
        
        for i in range(0, len(message_bytes), chunk_size):
            chunk = message_bytes[i:i+chunk_size]
            encrypted_chunk = cipher.encrypt(chunk)
            encrypted.append(base64.b64encode(encrypted_chunk).decode('utf-8'))
        
        return ":::".join(encrypted)
    except Exception as e:
        return f"Ошибка шифрования: {str(e)}"


def rsa_decrypt(encrypted_message, private_key_str):
    try:
        private_key = RSA.import_key(private_key_str)
        cipher = PKCS1_OAEP.new(private_key)
        
        # Разделяем зашифрованное сообщение на сегменты
        encrypted_chunks = encrypted_message.split(":::")
        decrypted = []
        
        for chunk in encrypted_chunks:
            encrypted_bytes = base64.b64decode(chunk)
            decrypted_chunk = cipher.decrypt(encrypted_bytes)
            decrypted.append(decrypted_chunk)
        
        return b''.join(decrypted).decode('utf-8')
    except Exception as e:
        return f"Ошибка дешифрования: {str(e)}"


# Функции для DES шифрования
def generate_des_key():
    key = get_random_bytes(8)  # 8 байт для DES
    return base64.b64encode(key).decode('utf-8')


def des_encrypt(message, key_str):
    try:
        key = base64.b64decode(key_str)
        cipher = DES.new(key, DES.MODE_CBC)
        data = message.encode('utf-8')
        ct_bytes = cipher.encrypt(pad(data, DES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return f"{iv}:::{ct}"
    except Exception as e:
        return f"Ошибка шифрования: {str(e)}"


def des_decrypt(encrypted_message, key_str):
    try:
        key = base64.b64decode(key_str)
        iv, ct = encrypted_message.split(":::")
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), DES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        return f"Ошибка дешифрования: {str(e)}"


# Функции для AES шифрования
def generate_aes_key():
    key = get_random_bytes(16)  # 16 байт для AES-128
    return base64.b64encode(key).decode('utf-8')


def aes_encrypt(message, key_str):
    try:
        key = base64.b64decode(key_str)
        cipher = AES.new(key, AES.MODE_CBC)
        data = message.encode('utf-8')
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return f"{iv}:::{ct}"
    except Exception as e:
        return f"Ошибка шифрования: {str(e)}"


def aes_decrypt(encrypted_message, key_str):
    try:
        key = base64.b64decode(key_str)
        iv, ct = encrypted_message.split(":::")
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        return f"Ошибка дешифрования: {str(e)}"

# FSM-состояния для шифра Цезаря (разделённый ввод)
class CaesarCipher(StatesGroup):
    choosing_mode = State()
    waiting_for_text_encrypt = State()
    waiting_for_key_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_key_decrypt = State()


# FSM-состояния для шифра с кодовым словом (разделённый ввод)
class KeywordCipher(StatesGroup):
    choosing_mode = State()
    waiting_for_text_encrypt = State()
    waiting_for_keyword_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_keyword_decrypt = State()


# FSM-состояние для анализатора текста
class TextAnalyzer(StatesGroup):
    waiting_for_text = State()

# 3. ДОБАВИТЬ КЛАССЫ СОСТОЯНИЙ (после класса TextAnalyzer)
# FSM-состояния для RSA шифрования
class RSACipher(StatesGroup):
    choosing_mode = State()
    generating_keys = State()
    waiting_for_text_encrypt = State()
    waiting_for_key_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_key_decrypt = State()


# FSM-состояния для DES шифрования
class DESCipher(StatesGroup):
    choosing_mode = State()
    generating_key = State()
    waiting_for_text_encrypt = State()
    waiting_for_key_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_key_decrypt = State()


# FSM-состояния для AES шифрования
class AESCipher(StatesGroup):
    choosing_mode = State()
    generating_key = State()
    waiting_for_text_encrypt = State()
    waiting_for_key_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_key_decrypt = State()
# 5. ДОБАВИТЬ ОБРАБОТЧИКИ RSA (перед обработчиком @dp.message())
# ------------------ Обработчики для RSA шифрования ------------------
@dp.message(lambda message: message.text == "🔒 RSA шифрование")
async def rsa_cipher_menu(message: types.Message, state: FSMContext):
    await state.set_state(RSACipher.choosing_mode)
    await message.reply("Выберите режим для RSA шифрования:", reply_markup=get_encryption_keyboard())


@dp.message(lambda message: message.text == "Сгенерировать ключ", StateFilter(RSACipher.choosing_mode))
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


@dp.message(lambda message: message.text == "Шифрование", StateFilter(RSACipher.choosing_mode))
async def rsa_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(RSACipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(RSACipher.waiting_for_text_encrypt))
async def process_rsa_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(rsa_text=message.text)
    await state.set_state(RSACipher.waiting_for_key_encrypt)
    await message.reply(
        "Введите публичный ключ RSA для шифрования:\n"
        "(начинается с -----BEGIN PUBLIC KEY-----)"
    )


@dp.message(StateFilter(RSACipher.waiting_for_key_encrypt))
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


@dp.message(lambda message: message.text == "Дешифрование", StateFilter(RSACipher.choosing_mode))
async def rsa_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(RSACipher.waiting_for_text_decrypt)
    await message.reply("Введите зашифрованный RSA текст:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(RSACipher.waiting_for_text_decrypt))
async def process_rsa_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(rsa_text=message.text)
    await state.set_state(RSACipher.waiting_for_key_decrypt)
    await message.reply(
        "Введите приватный ключ RSA для дешифрования:\n"
        "(начинается с -----BEGIN RSA PRIVATE KEY-----)"
    )


@dp.message(StateFilter(RSACipher.waiting_for_key_decrypt))
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


# ------------------ Обработчики для DES шифрования ------------------
@dp.message(lambda message: message.text == "🔏 DES шифрование")
async def des_cipher_menu(message: types.Message, state: FSMContext):
    await state.set_state(DESCipher.choosing_mode)
    await message.reply("Выберите режим для DES шифрования:", reply_markup=get_encryption_keyboard())


@dp.message(lambda message: message.text == "Сгенерировать ключ", StateFilter(DESCipher.choosing_mode))
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


@dp.message(lambda message: message.text == "Шифрование", StateFilter(DESCipher.choosing_mode))
async def des_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(DESCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(DESCipher.waiting_for_text_encrypt))
async def process_des_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(des_text=message.text)
    await state.set_state(DESCipher.waiting_for_key_encrypt)
    await message.reply("Введите DES ключ для шифрования:")


@dp.message(StateFilter(DESCipher.waiting_for_key_encrypt))
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


@dp.message(lambda message: message.text == "Дешифрование", StateFilter(DESCipher.choosing_mode))
async def des_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(DESCipher.waiting_for_text_decrypt)
    await message.reply("Введите зашифрованный DES текст:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(DESCipher.waiting_for_text_decrypt))
async def process_des_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(des_text=message.text)
    await state.set_state(DESCipher.waiting_for_key_decrypt)
    await message.reply("Введите DES ключ для дешифрования:")


@dp.message(StateFilter(DESCipher.waiting_for_key_decrypt))
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


# ------------------ Обработчики для AES шифрования ------------------
@dp.message(lambda message: message.text == "🔐 AES шифрование")
async def aes_cipher_menu(message: types.Message, state: FSMContext):
    await state.set_state(AESCipher.choosing_mode)
    await message.reply("Выберите режим для AES шифрования:", reply_markup=get_encryption_keyboard())


@dp.message(lambda message: message.text == "Сгенерировать ключ", StateFilter(AESCipher.choosing_mode))
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


@dp.message(lambda message: message.text == "Шифрование", StateFilter(AESCipher.choosing_mode))
async def aes_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(AESCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(AESCipher.waiting_for_text_encrypt))
async def process_aes_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(aes_text=message.text)
    await state.set_state(AESCipher.waiting_for_key_encrypt)
    await message.reply("Введите AES ключ для шифрования:")


@dp.message(StateFilter(AESCipher.waiting_for_key_encrypt))
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


@dp.message(lambda message: message.text == "Дешифрование", StateFilter(AESCipher.choosing_mode))
async def aes_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(AESCipher.waiting_for_text_decrypt)
    await message.reply("Введите зашифрованный AES текст:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(AESCipher.waiting_for_text_decrypt))
async def process_aes_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(aes_text=message.text)
    await state.set_state(AESCipher.waiting_for_key_decrypt)
    await message.reply("Введите AES ключ для дешифрования:")


@dp.message(StateFilter(AESCipher.waiting_for_key_decrypt))
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
# ------------------ Обработчики для генерации простых чисел ------------------

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот для генерации псевдослучайных простых чисел.\n"
        "Используйте кнопки для навигации или команду /prime &lt;min&gt; &lt;max&gt; для генерации простого числа в заданном диапазоне.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )


# 6. ОБНОВИТЬ HELP СООБЩЕНИЕ (в функции send_help)
@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply(
        "Команды бота:\n"
        "/start - начать работу с ботом\n"
        "/help - показать справку\n\n"
        "🤖 Генератор простых чисел:\n"
        " - Нажмите кнопку '🔍 Сгенерировать простое число'\n"
        " - Выберите предустановленный диапазон или введите свой в формате &lt;min&gt;-&lt;max&gt;\n"
        " - Бот сгенерирует для вас случайное простое число\n\n"
        "🔐 Функции шифрования:\n"
        " - Шифр Цезаря (простой шифр сдвига)\n"
        " - Шифр с использованием кодового слова (Виженера)\n"
        " - RSA шифрование (асимметричный алгоритм)\n"
        " - DES шифрование (симметричный блочный шифр)\n"
        " - AES шифрование (современный блочный шифр)\n\n"
        "📝 Анализатор текста - для анализа частотности символов",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("prime"))
async def generate_prime_cmd(message: types.Message):
    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            await message.reply(
                "Ошибка! Используйте команду в формате: /prime &lt;min&gt; &lt;max&gt;",
                parse_mode=ParseMode.HTML,
                reply_markup=get_main_keyboard()
            )
            return
        min_value = int(args[0])
        max_value = int(args[1])
        await process_prime_generation(message, min_value, max_value)
    except ValueError:
        await message.reply(
            "Ошибка! Аргументы должны быть целыми числами.",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        await message.reply(
            f"Произошла ошибка: {str(e)}",
            reply_markup=get_main_keyboard()
        )


async def process_prime_generation(message, min_value, max_value):
    if min_value <= 1:
        min_value = 2
    if min_value > max_value:
        await message.reply("Ошибка! Минимальное значение должно быть меньше максимального.",
                            reply_markup=get_main_keyboard())
        return
    if max_value > 10 ** 10:
        await message.reply("Ошибка! Максимальное значение не должно превышать 10^10.",
                            reply_markup=get_main_keyboard())
        return
    if max_value > 10 ** 7:
        await message.reply(
            "⚠️ Внимание! Генерация простого числа в большом диапазоне может занять некоторое время. Пожалуйста, подождите...",
            reply_markup=get_main_keyboard())
    await message.reply("🔄 Генерирую простое число...")
    prime_number = generate_random_prime(min_value, max_value)
    await message.reply(
        f"🔢 Псевдослучайное простое число в диапазоне [{min_value}, {max_value}]:\n\n<b>{prime_number}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )


@dp.message(lambda message: message.text == "🔍 Сгенерировать простое число")
async def button_generate_prime(message: types.Message):
    await message.reply(
        "Выберите диапазон для генерации простого числа или введите свой в формате &lt;min&gt;-&lt;max&gt;:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_range_keyboard()
    )


@dp.message(lambda message: message.text == "❓ Помощь")
async def button_help(message: types.Message):
    await send_help(message)


@dp.message(lambda message: message.text == "🔙 Вернуться")
async def button_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Вернулись в главное меню.", reply_markup=get_main_keyboard())


@dp.message(lambda message: message.text in ["100-1000", "1000-10000", "10000-100000", "100000-1000000",
                                             "1000000-10000000", "10000000-100000000"])
async def process_range_selection(message: types.Message):
    range_parts = message.text.split('-')
    min_value = int(range_parts[0])
    max_value = int(range_parts[1])
    await process_prime_generation(message, min_value, max_value)


@dp.message(lambda message: '-' in message.text and len(message.text.split('-')) == 2)
async def process_custom_range(message: types.Message):
    try:
        range_parts = message.text.split('-')
        min_value = int(range_parts[0])
        max_value = int(range_parts[1])
        await process_prime_generation(message, min_value, max_value)
    except ValueError:
        await message.reply(
            "Ошибка! Введите диапазон в формате &lt;min&gt;-&lt;max&gt;, где min и max - целые числа.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_range_keyboard()
        )


# ------------------ Обработчики для шифра Цезаря (русский алфавит, разделённый ввод) ------------------

@dp.message(lambda message: message.text == "🔐 Шифр цезаря")
async def caesar_cipher_menu(message: types.Message, state: FSMContext):
    await state.set_state(CaesarCipher.choosing_mode)
    await message.reply("Выберите режим для шифра Цезаря:", reply_markup=get_caesar_keyboard())


@dp.message(lambda message: message.text == "Шифрование", StateFilter(CaesarCipher.choosing_mode))
async def caesar_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(CaesarCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования (на русском языке):", reply_markup=get_main_keyboard())


@dp.message(StateFilter(CaesarCipher.waiting_for_text_encrypt))
async def process_caesar_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(caesar_text=message.text)
    await state.set_state(CaesarCipher.waiting_for_key_encrypt)
    await message.reply("Введите числовой ключ для шифрования:")


@dp.message(StateFilter(CaesarCipher.waiting_for_key_encrypt))
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


@dp.message(lambda message: message.text == "Дешифрование", StateFilter(CaesarCipher.choosing_mode))
async def caesar_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(CaesarCipher.waiting_for_text_decrypt)
    await message.reply("Введите текст для дешифрования (на русском языке):", reply_markup=get_main_keyboard())


@dp.message(StateFilter(CaesarCipher.waiting_for_text_decrypt))
async def process_caesar_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(caesar_text=message.text)
    await state.set_state(CaesarCipher.waiting_for_key_decrypt)
    await message.reply("Введите числовой ключ для дешифрования:")


@dp.message(StateFilter(CaesarCipher.waiting_for_key_decrypt))
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


# ------------------ Обработчики для шифра с кодовым словом (русский алфавит, разделённый ввод) ------------------

@dp.message(lambda message: message.text == "🔑 Шифр с использованием кодового слова")
async def keyword_cipher_menu(message: types.Message, state: FSMContext):
    await state.set_state(KeywordCipher.choosing_mode)
    await message.reply("Выберите режим для шифра с использованием кодового слова:",
                        reply_markup=get_keyword_cipher_keyboard())


@dp.message(lambda message: message.text == "Шифрование", StateFilter(KeywordCipher.choosing_mode))
async def keyword_encryption_start(message: types.Message, state: FSMContext):
    await state.set_state(KeywordCipher.waiting_for_text_encrypt)
    await message.reply("Введите текст для шифрования (на русском языке):", reply_markup=get_main_keyboard())


@dp.message(StateFilter(KeywordCipher.waiting_for_text_encrypt))
async def process_keyword_text_encrypt(message: types.Message, state: FSMContext):
    await state.update_data(keyword_text=message.text)
    await state.set_state(KeywordCipher.waiting_for_keyword_encrypt)
    await message.reply("Введите кодовое слово для шифрования:")


@dp.message(StateFilter(KeywordCipher.waiting_for_keyword_encrypt))
async def process_keyword_encrypt(message: types.Message, state: FSMContext):
    keyword = message.text.strip()
    data = await state.get_data()
    text = data.get("keyword_text")
    result = vigenere_encrypt_russian(text, keyword)
    await message.reply(f"Результат шифрования: {result}", reply_markup=get_main_keyboard())
    await state.clear()


@dp.message(lambda message: message.text == "Дешифрование", StateFilter(KeywordCipher.choosing_mode))
async def keyword_decryption_start(message: types.Message, state: FSMContext):
    await state.set_state(KeywordCipher.waiting_for_text_decrypt)
    await message.reply("Введите текст для дешифрования (на русском языке):", reply_markup=get_main_keyboard())


@dp.message(StateFilter(KeywordCipher.waiting_for_text_decrypt))
async def process_keyword_text_decrypt(message: types.Message, state: FSMContext):
    await state.update_data(keyword_text=message.text)
    await state.set_state(KeywordCipher.waiting_for_keyword_decrypt)
    await message.reply("Введите кодовое слово для дешифрования:")


@dp.message(StateFilter(KeywordCipher.waiting_for_keyword_decrypt))
async def process_keyword_decrypt(message: types.Message, state: FSMContext):
    keyword = message.text.strip()
    data = await state.get_data()
    text = data.get("keyword_text")
    result = vigenere_decrypt_russian(text, keyword)
    await message.reply(f"Результат дешифрования: {result}", reply_markup=get_main_keyboard())
    await state.clear()


# ------------------ Обработчик анализатора текста ------------------

@dp.message(lambda message: message.text == "📝 Анализатор текста")
async def text_analyzer_start(message: types.Message, state: FSMContext):
    await state.set_state(TextAnalyzer.waiting_for_text)
    await message.reply("Введите текст для анализа:", reply_markup=get_main_keyboard())


@dp.message(StateFilter(TextAnalyzer.waiting_for_text))
async def process_text_analysis(message: types.Message, state: FSMContext):
    text = message.text
    words = text.split()
    word_count = len(words)

    letter_total = 0
    digit_total = 0
    special_total = 0
    letter_count = {}
    digit_count = {}
    special_count = {}

    for char in text:
        if char.isalpha():
            letter_total += 1
            char_lower = char.lower()
            letter_count[char_lower] = letter_count.get(char_lower, 0) + 1
        elif char.isdigit():
            digit_total += 1
            digit_count[char] = digit_count.get(char, 0) + 1
        elif not char.isspace():
            special_total += 1
            special_count[char] = special_count.get(char, 0) + 1

    letter_freq = "\n".join([f"{letter}: {count}" for letter, count in sorted(letter_count.items())])
    digit_freq = "\n".join([f"{digit}: {count}" for digit, count in sorted(digit_count.items())])
    special_freq = "\n".join([f"{symbol}: {count}" for symbol, count in sorted(special_count.items())])

    result = (
        "📊 Анализ текста:\n"
        f"Количество слов: {word_count}\n"
        f"Количество букв: {letter_total}\n"
        f"Количество цифр: {digit_total}\n"
        f"Количество спецсимволов: {special_total}\n\n"
        "Частота букв:\n"
        f"{letter_freq}\n\n"
        "Частота цифр:\n"
        f"{digit_freq}\n"
        "Частота спецсимволов:\n"
        f"{special_freq}"
    )
    await message.reply(result, reply_markup=get_main_keyboard())
    await state.clear()


# ------------------ Обработчик для всех остальных сообщений ------------------

@dp.message()
async def echo_all(message: types.Message):
    await message.reply(
        "Я понимаю только команды и кнопки. Используйте кнопки ниже или введите /help для получения справки.",
        reply_markup=get_main_keyboard())


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот запущен...")
    asyncio.run(main())
