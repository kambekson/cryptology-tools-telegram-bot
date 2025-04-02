from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_keyboard_layout_translator
from states import KeyboardLayoutTranslator
from crypto_utils import ru_to_en, en_to_ru, ru_to_kz, kz_to_ru, en_to_kz, kz_to_en

# Обработчик для запуска переводчика раскладки клавиатуры
async def cmd_keyboard_layout_translator(message: types.Message, state: FSMContext):
    await message.reply(
        "Выберите направление перевода раскладки клавиатуры:",
        reply_markup=get_keyboard_layout_translator()
    )
    await state.set_state(KeyboardLayoutTranslator.choosing_mode)

# Обработчик выбора режима перевода
async def keyboard_layout_mode(message: types.Message, state: FSMContext):
    if message.text == "🇷🇺→🇬🇧 Русская → Английская":
        await state.update_data(mode="ru_to_en", mode_name="Русская → Английская")
    elif message.text == "🇬🇧→🇷🇺 Английская → Русская":
        await state.update_data(mode="en_to_ru", mode_name="Английская → Русская")
    elif message.text == "🇷🇺→🇰🇿 Русская → Казахская":
        await state.update_data(mode="ru_to_kz", mode_name="Русская → Казахская")
    elif message.text == "🇰🇿→🇷🇺 Казахская → Русская":
        await state.update_data(mode="kz_to_ru", mode_name="Казахская → Русская")
    elif message.text == "🇬🇧→🇰🇿 Английская → Казахская":
        await state.update_data(mode="en_to_kz", mode_name="Английская → Казахская")
    elif message.text == "🇰🇿→🇬🇧 Казахская → Английская":
        await state.update_data(mode="kz_to_en", mode_name="Казахская → Английская")
    else:
        await message.reply(
            "Пожалуйста, выберите один из предложенных вариантов.",
            reply_markup=get_keyboard_layout_translator()
        )
        return
    
    mode_data = await state.get_data()
    mode_name = mode_data.get("mode_name")
    
    await message.reply(
        f"Вы выбрали режим: <b>{mode_name}</b>\n"
        f"Введите текст для перевода раскладки:",
        parse_mode=ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(KeyboardLayoutTranslator.waiting_for_text)

# Обработчик ввода текста для перевода
async def process_text_for_translation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    mode = user_data.get("mode")
    mode_name = user_data.get("mode_name")
    
    input_text = message.text
    result_text = ""
    
    if mode == "ru_to_en":
        result_text = ru_to_en(input_text)
    elif mode == "en_to_ru":
        result_text = en_to_ru(input_text)
    elif mode == "ru_to_kz":
        result_text = ru_to_kz(input_text)
    elif mode == "kz_to_ru":
        result_text = kz_to_ru(input_text)
    elif mode == "en_to_kz":
        result_text = en_to_kz(input_text)
    elif mode == "kz_to_en":
        result_text = kz_to_en(input_text)
    
    await message.reply(
        f"<b>Результат перевода раскладки {mode_name}</b>\n\n"
        f"Исходный текст:\n<code>{input_text}</code>\n\n"
        f"Результат:\n<code>{result_text}</code>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )
    
    # Очищаем состояние
    await state.clear()

# Регистрация обработчиков
def register_keyboard_layout_handlers(dp):
    dp.message.register(cmd_keyboard_layout_translator, lambda message: message.text == "⌨️ Переводчик раскладки клавиатуры")
    dp.message.register(keyboard_layout_mode, KeyboardLayoutTranslator.choosing_mode)
    dp.message.register(process_text_for_translation, KeyboardLayoutTranslator.waiting_for_text)
    
    return dp 
