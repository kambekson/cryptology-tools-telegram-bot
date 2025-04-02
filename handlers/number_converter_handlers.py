from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_number_converter_keyboard, get_base_keyboard
from states import NumberConverter
from crypto_utils import decimal_to_base, base_to_decimal

# Обработчик для запуска конвертера систем счисления
async def cmd_number_converter(message: types.Message, state: FSMContext):
    await message.reply(
        "Выберите режим конвертации систем счисления:",
        reply_markup=get_number_converter_keyboard()
    )
    await state.set_state(NumberConverter.choosing_mode)

# Обработчик выбора режима конвертации
async def number_converter_mode(message: types.Message, state: FSMContext):
    if message.text == "Из 10-й в другую":
        await state.update_data(mode="dec_to_base")
        await message.reply(
            "Введите целое число в десятичной системе счисления:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(NumberConverter.waiting_for_decimal_input)
    elif message.text == "Из другой в 10-ю":
        await state.update_data(mode="base_to_dec")
        await message.reply(
            "Выберите исходную систему счисления:",
            reply_markup=get_base_keyboard()
        )
        await state.set_state(NumberConverter.waiting_for_base_input)
    else:
        await message.reply(
            "Пожалуйста, воспользуйтесь клавиатурой для выбора режима",
            reply_markup=get_number_converter_keyboard()
        )

# Обработчик ввода десятичного числа
async def process_decimal_input(message: types.Message, state: FSMContext):
    try:
        decimal_num = int(message.text)
        await state.update_data(decimal_num=decimal_num)
        await message.reply(
            "Выберите целевую систему счисления:",
            reply_markup=get_base_keyboard()
        )
        await state.set_state(NumberConverter.waiting_for_base_output)
    except ValueError:
        await message.reply(
            "Пожалуйста, введите корректное целое число в десятичной системе счисления.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Обработчик выбора исходной системы счисления
async def process_base_input(message: types.Message, state: FSMContext):
    if message.text == "2 (двоичная)":
        await state.update_data(input_base=2)
        await message.reply(
            "Введите число в двоичной системе счисления (используйте только 0 и 1):",
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif message.text == "8 (восьмеричная)":
        await state.update_data(input_base=8)
        await message.reply(
            "Введите число в восьмеричной системе счисления (используйте цифры от 0 до 7):",
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif message.text == "16 (шестнадцатеричная)":
        await state.update_data(input_base=16)
        await message.reply(
            "Введите число в шестнадцатеричной системе счисления (используйте цифры от 0 до 9 и буквы от A до F):",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.reply(
            "Пожалуйста, выберите систему счисления из предложенных вариантов",
            reply_markup=get_base_keyboard()
        )
        return
    
    await state.set_state(NumberConverter.waiting_for_base_output)

# Обработчик выбора целевой системы счисления и ввода числа
async def process_base_output(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    mode = user_data.get("mode")
    
    if mode == "dec_to_base":
        # Конвертация из десятичной в выбранную
        decimal_num = user_data.get("decimal_num")
        
        if message.text == "2 (двоичная)":
            result = decimal_to_base(decimal_num, 2)
            base_name = "двоичную"
            base = 2
        elif message.text == "8 (восьмеричная)":
            result = decimal_to_base(decimal_num, 8)
            base_name = "восьмеричную"
            base = 8
        elif message.text == "16 (шестнадцатеричная)":
            result = decimal_to_base(decimal_num, 16)
            base_name = "шестнадцатеричную"
            base = 16
        else:
            await message.reply(
                "Пожалуйста, выберите систему счисления из предложенных вариантов",
                reply_markup=get_base_keyboard()
            )
            return
        
        await message.reply(
            f"<b>Результат конвертации</b>\n\n"
            f"Исходное число (десятичное): <code>{decimal_num}</code>\n"
            f"Результат ({base_name}): <code>{result}</code>\n\n"
            f"Формат: <code>{decimal_num}₁₀ = {result}_{base}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
        
    elif mode == "base_to_dec":
        # Конвертация из выбранной в десятичную
        input_base = user_data.get("input_base")
        
        try:
            if input_base == 2:
                for char in message.text:
                    if char not in "01":
                        raise ValueError("Двоичное число должно содержать только символы 0 и 1")
                base_name = "двоичной"
            elif input_base == 8:
                for char in message.text:
                    if char not in "01234567":
                        raise ValueError("Восьмеричное число должно содержать только цифры от 0 до 7")
                base_name = "восьмеричной"
            elif input_base == 16:
                for char in message.text.upper():
                    if char not in "0123456789ABCDEF":
                        raise ValueError("Шестнадцатеричное число должно содержать только цифры от 0 до 9 и буквы от A до F")
                base_name = "шестнадцатеричной"
            
            result = base_to_decimal(message.text, input_base)
            
            await message.reply(
                f"<b>Результат конвертации</b>\n\n"
                f"Исходное число ({base_name}): <code>{message.text}</code>\n"
                f"Результат (десятичное): <code>{result}</code>\n\n"
                f"Формат: <code>{message.text}_{input_base} = {result}₁₀</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=get_main_keyboard()
            )
        except ValueError as e:
            await message.reply(
                f"Ошибка: {str(e)}. Попробуйте еще раз.",
                reply_markup=types.ReplyKeyboardRemove()
            )
            return
    
    # Очищаем состояние
    await state.clear()

# Регистрация обработчиков
def register_number_converter_handlers(dp):
    dp.message.register(cmd_number_converter, lambda message: message.text == "🔢 Конвертер систем счисления")
    dp.message.register(number_converter_mode, NumberConverter.choosing_mode)
    dp.message.register(process_decimal_input, NumberConverter.waiting_for_decimal_input)
    dp.message.register(process_base_input, NumberConverter.waiting_for_base_input)
    dp.message.register(process_base_output, NumberConverter.waiting_for_base_output)
    
    return dp 
