from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from keyboards import get_main_keyboard
from states import TextAnalyzer
from crypto_utils import analyze_text

async def text_analyzer_start(message: types.Message, state: FSMContext):
    await state.set_state(TextAnalyzer.waiting_for_text)
    await message.reply("Введите текст для анализа:", reply_markup=get_main_keyboard())

async def process_text_analysis(message: types.Message, state: FSMContext):
    text = message.text
    result = analyze_text(text)
    await message.reply(result, reply_markup=get_main_keyboard())
    await state.clear()

def register_text_analyzer_handlers(dp):
    dp.message.register(text_analyzer_start, lambda message: message.text == "📝 Анализатор текста")
    dp.message.register(process_text_analysis, StateFilter(TextAnalyzer.waiting_for_text))
    
    return dp 