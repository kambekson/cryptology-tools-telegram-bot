from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from keyboards import get_main_keyboard
from handlers.prime_handlers import send_help

async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот для криптографических инструментов.\n"
        "Вы можете использовать различные функции: генерация простых чисел, шифрование, генерация паролей и другие.\n"
        "Используйте кнопки для навигации или введите /help для получения справки.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

async def button_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Вернулись в главное меню.", reply_markup=get_main_keyboard())

async def echo_all(message: types.Message):
    await message.reply(
        "Я понимаю только команды и кнопки. Используйте кнопки ниже или введите /help для получения справки.",
        reply_markup=get_main_keyboard())

def register_general_handlers(dp):
    dp.message.register(send_welcome, CommandStart())
    dp.message.register(send_help, Command("help"))
    dp.message.register(button_back, lambda message: message.text == "🔙 Вернуться")
    dp.message.register(echo_all)
    
    return dp 