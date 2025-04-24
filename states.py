from aiogram.fsm.state import StatesGroup, State

# FSM-состояния для игры вероятности
class ProbabilityGame(StatesGroup):
    choosing_game = State()

# FSM-состояния для шифра Эллипс кривых

class EllipticState(StatesGroup):
    choosing_mode = State()
    waiting_for_text_to_sign = State()
    waiting_for_private_key = State()
    waiting_for_text_verify = State()
    waiting_for_signature = State()
    waiting_for_public_key = State()

# FSM-состояния для шифра Цезаря
class CaesarCipher(StatesGroup):
    choosing_mode = State()
    waiting_for_text_encrypt = State()
    waiting_for_key_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_key_decrypt = State()

# FSM-состояния для шифра с кодовым словом
class KeywordCipher(StatesGroup):
    choosing_mode = State()
    waiting_for_text_encrypt = State()
    waiting_for_keyword_encrypt = State()
    waiting_for_text_decrypt = State()
    waiting_for_keyword_decrypt = State()

# FSM-состояние для анализатора текста
class TextAnalyzer(StatesGroup):
    waiting_for_text = State()

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

# FSM-состояния для генератора паролей
class PasswordGenerator(StatesGroup):
    waiting_for_length = State()
    waiting_for_options = State()

# FSM-состояния для конвертера систем счисления
class NumberConverter(StatesGroup):
    choosing_mode = State()
    waiting_for_decimal_input = State()
    waiting_for_base_input = State()
    waiting_for_base_output = State()

# FSM-состояния для переводчика раскладки клавиатуры
class KeyboardLayoutTranslator(StatesGroup):
    choosing_mode = State()
    waiting_for_text = State() 