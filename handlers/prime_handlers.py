from aiogram import types
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_range_keyboard
from crypto_utils import generate_random_prime

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
        "🔑 Генератор паролей:\n"
        " - Простые пароли (8 символов, строчные буквы и цифры)\n"
        " - Сложные пароли (16 символов, все типы символов)\n"
        " - Настраиваемые пароли с выбором длины и типов символов\n\n"
        "📝 Анализатор текста - для анализа частотности символов",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

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

async def button_generate_prime(message: types.Message):
    await message.reply(
        "Выберите диапазон для генерации простого числа или введите свой в формате &lt;min&gt;-&lt;max&gt;:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_range_keyboard()
    )

async def button_help(message: types.Message):
    await send_help(message)

async def process_range_selection(message: types.Message):
    range_parts = message.text.split('-')
    min_value = int(range_parts[0])
    max_value = int(range_parts[1])
    await process_prime_generation(message, min_value, max_value)

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

def register_prime_handlers(dp):
    dp.message.register(generate_prime_cmd, Command("prime"))
    dp.message.register(button_generate_prime, lambda message: message.text == "🔍 Сгенерировать простое число")
    dp.message.register(button_help, lambda message: message.text == "❓ Помощь")
    dp.message.register(process_range_selection, lambda message: message.text in [
        "100-1000", "1000-10000", "10000-100000", "100000-1000000",
        "1000000-10000000", "10000000-100000000"
    ])
    dp.message.register(process_custom_range, lambda message: '-' in message.text 
                        and len(message.text.split('-')) == 2 
                        and message.text[0].isdigit())
    
    return dp 