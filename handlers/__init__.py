from handlers.elliptic_handlers import register_elliptic_handlers
from handlers.prime_handlers import register_prime_handlers
from handlers.caesar_handlers import register_caesar_handlers
from handlers.keyword_handlers import register_keyword_handlers
from handlers.rsa_handlers import register_rsa_handlers
from handlers.des_handlers import register_des_handlers 
from handlers.aes_handlers import register_aes_handlers
from handlers.text_analyzer_handlers import register_text_analyzer_handlers
from handlers.general_handlers import register_general_handlers
from handlers.password_handlers import register_password_handlers
from handlers.number_converter_handlers import register_number_converter_handlers
from handlers.keyboard_layout_handlers import register_keyboard_layout_handlers
from handlers.encryption_menu_handlers import register_encryption_menu_handlers
from handlers.probability_handlers import register_probability_handlers

def register_all_handlers(dp):
    dp = register_prime_handlers(dp)
    dp = register_text_analyzer_handlers(dp)
    dp = register_password_handlers(dp)
    dp = register_number_converter_handlers(dp)
    dp = register_keyboard_layout_handlers(dp)
    dp = register_probability_handlers(dp)
    
    # Сначала регистрируем меню шифрования
    dp = register_encryption_menu_handlers(dp)
    
    # Затем регистрируем конкретные шифры
    dp = register_caesar_handlers(dp)
    dp = register_keyword_handlers(dp)
    dp = register_rsa_handlers(dp)
    dp = register_des_handlers(dp)
    dp = register_aes_handlers(dp)
    dp = register_elliptic_handlers(dp)
    dp = register_text_analyzer_handlers(dp)
    dp = register_password_handlers(dp)
    dp = register_number_converter_handlers(dp)
    dp = register_keyboard_layout_handlers(dp)
    dp = register_general_handlers(dp)
    
    return dp