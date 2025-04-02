"""
Конфигурация прокси для обхода блокировок Telegram API

Для использования прокси, раскомментируйте соответствующий блок кода
в файле main.py и установите здесь настройки вашего прокси.
"""

# SOCKS5 прокси (требуется установка pip install aiohttp-socks)
SOCKS5_PROXY = {
    'url': 'socks5://user:password@proxy_address:port',
    'enabled': False  # Установите в True для активации
}

# HTTP прокси
HTTP_PROXY = {
    'url': 'http://user:password@proxy_address:port',
    'enabled': False  # Установите в True для активации
} 