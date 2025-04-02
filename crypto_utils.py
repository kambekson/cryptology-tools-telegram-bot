import random
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Cipher import PKCS1_OAEP
from sympy import isprime

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

# Анализатор текста
def analyze_text(text):
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

    return result 

# Генератор паролей
def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
                      use_digits=True, use_special=True):
    """
    Генерирует случайный пароль с заданными параметрами.
    
    Args:
        length: Длина пароля (по умолчанию 12)
        use_uppercase: Использовать ли заглавные буквы
        use_lowercase: Использовать ли строчные буквы
        use_digits: Использовать ли цифры
        use_special: Использовать ли специальные символы
        
    Returns:
        Строка со случайным паролем
    """
    charset = ""
    
    if use_uppercase:
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_lowercase:
        charset += "abcdefghijklmnopqrstuvwxyz"
    if use_digits:
        charset += "0123456789"
    if use_special:
        charset += "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    
    # Если ни один из типов символов не выбран, используем по умолчанию все
    if not charset:
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    
    # Генерируем пароль
    if length <= 0:
        length = 12
    
    password = ''.join(random.choice(charset) for _ in range(length))
    return password 

# Функции для работы с системами счисления
def decimal_to_base(decimal_num, base):
    """
    Конвертирует число из десятичной системы в указанную систему счисления
    """
    try:
        decimal_num = int(decimal_num)
        if base == 2:
            return bin(decimal_num)[2:]  # Удаляем префикс '0b'
        elif base == 8:
            return oct(decimal_num)[2:]  # Удаляем префикс '0o'
        elif base == 16:
            return hex(decimal_num)[2:].upper()  # Удаляем префикс '0x' и преобразуем в верхний регистр
        else:
            return f"Неподдерживаемая система счисления: {base}"
    except ValueError:
        return "Ошибка: введите корректное целое число"

def base_to_decimal(number, base):
    """
    Конвертирует число из указанной системы счисления в десятичную
    """
    try:
        if base == 2:
            return int(number, 2)
        elif base == 8:
            return int(number, 8)
        elif base == 16:
            return int(number, 16)
        else:
            return f"Неподдерживаемая система счисления: {base}"
    except ValueError:
        return f"Ошибка: введите корректное число в системе счисления с основанием {base}" 