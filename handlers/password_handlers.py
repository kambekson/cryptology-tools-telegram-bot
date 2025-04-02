from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import get_main_keyboard, get_password_options_keyboard, get_password_customization_keyboard
from states import PasswordGenerator
from crypto_utils import generate_password

async def password_generator_start(message: types.Message, state: FSMContext):
    await message.reply(
        "🔑 <b>Генератор паролей</b>\n\n"
        "Выберите тип пароля, который вы хотите сгенерировать:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_password_options_keyboard()
    )
    await state.clear()

async def generate_simple_password(message: types.Message, state: FSMContext):
    password = generate_password(length=8, use_uppercase=False, use_special=False)
    await message.reply(
        f"🔑 <b>Ваш простой пароль:</b>\n\n"
        f"<code>{password}</code>\n\n"
        f"Длина: 8 символов\n"
        f"Содержит: строчные буквы и цифры",
        parse_mode=ParseMode.HTML,
        reply_markup=get_password_options_keyboard()
    )

async def generate_complex_password(message: types.Message, state: FSMContext):
    password = generate_password(length=16)
    await message.reply(
        f"🔑 <b>Ваш сложный пароль:</b>\n\n"
        f"<code>{password}</code>\n\n"
        f"Длина: 16 символов\n"
        f"Содержит: заглавные и строчные буквы, цифры и специальные символы",
        parse_mode=ParseMode.HTML,
        reply_markup=get_password_options_keyboard()
    )

async def customize_password_start(message: types.Message, state: FSMContext):
    await message.reply(
        "🔧 <b>Настройка пароля</b>\n\n"
        "Введите желаемую длину пароля (от 4 до 32 символов):",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(PasswordGenerator.waiting_for_length)

async def process_password_length(message: types.Message, state: FSMContext):
    try:
        length = int(message.text.strip())
        if length < 4 or length > 32:
            await message.reply(
                "❌ Длина пароля должна быть от 4 до 32 символов. Попробуйте снова:"
            )
            return
        await state.update_data(length=length, 
                               use_uppercase=True, 
                               use_lowercase=True, 
                               use_digits=True, 
                               use_special=True)
        await message.reply(
            f"✅ Длина пароля установлена: {length} символов\n\n"
            "Теперь настройте параметры пароля:",
            reply_markup=get_password_customization_keyboard()
        )
        await state.set_state(PasswordGenerator.waiting_for_options)
    except ValueError:
        await message.reply(
            "❌ Пожалуйста, введите число от 4 до 32."
        )

async def process_uppercase_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['use_uppercase'] = True
    await state.update_data(data)
    await message.reply("✅ Пароль будет содержать заглавные буквы", 
                        reply_markup=get_password_customization_keyboard())

async def process_no_uppercase_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['use_uppercase'] = False
    await state.update_data(data)
    await message.reply("✅ Пароль не будет содержать заглавные буквы", 
                        reply_markup=get_password_customization_keyboard())

async def process_digits_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['use_digits'] = True
    await state.update_data(data)
    await message.reply("✅ Пароль будет содержать цифры", 
                        reply_markup=get_password_customization_keyboard())

async def process_no_digits_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['use_digits'] = False
    await state.update_data(data)
    await message.reply("✅ Пароль не будет содержать цифры", 
                        reply_markup=get_password_customization_keyboard())

async def process_special_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['use_special'] = True
    await state.update_data(data)
    await message.reply("✅ Пароль будет содержать специальные символы", 
                        reply_markup=get_password_customization_keyboard())

async def process_no_special_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['use_special'] = False
    await state.update_data(data)
    await message.reply("✅ Пароль не будет содержать специальные символы", 
                        reply_markup=get_password_customization_keyboard())

async def generate_custom_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # Проверка, чтобы хотя бы один тип символов был включен
    if not any([data.get('use_uppercase', True), 
               data.get('use_lowercase', True), 
               data.get('use_digits', True), 
               data.get('use_special', True)]):
        await message.reply(
            "❌ Необходимо включить хотя бы один тип символов.",
            reply_markup=get_password_customization_keyboard()
        )
        return
    
    password = generate_password(
        length=data.get('length', 12),
        use_uppercase=data.get('use_uppercase', True),
        use_lowercase=data.get('use_lowercase', True),
        use_digits=data.get('use_digits', True),
        use_special=data.get('use_special', True)
    )
    
    content_description = []
    if data.get('use_uppercase', True):
        content_description.append("заглавные буквы")
    if data.get('use_lowercase', True):
        content_description.append("строчные буквы")
    if data.get('use_digits', True):
        content_description.append("цифры")
    if data.get('use_special', True):
        content_description.append("специальные символы")
    
    content_text = ", ".join(content_description)
    
    await message.reply(
        f"🔑 <b>Ваш настроенный пароль:</b>\n\n"
        f"<code>{password}</code>\n\n"
        f"Длина: {data.get('length', 12)} символов\n"
        f"Содержит: {content_text}",
        parse_mode=ParseMode.HTML,
        reply_markup=get_password_options_keyboard()
    )
    await state.clear()

def register_password_handlers(dp):
    dp.message.register(password_generator_start, lambda message: message.text == "🔑 Генератор паролей")
    dp.message.register(generate_simple_password, lambda message: message.text == "Простой пароль")
    dp.message.register(generate_complex_password, lambda message: message.text == "Сложный пароль")
    dp.message.register(customize_password_start, lambda message: message.text == "Настроить пароль")
    
    dp.message.register(process_password_length, PasswordGenerator.waiting_for_length)
    
    dp.message.register(process_uppercase_option, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "С заглавными буквами")
    dp.message.register(process_no_uppercase_option, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "Без заглавных букв")
    dp.message.register(process_digits_option, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "С цифрами")
    dp.message.register(process_no_digits_option, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "Без цифр")
    dp.message.register(process_special_option, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "Со спецсимволами")
    dp.message.register(process_no_special_option, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "Без спецсимволов")
    dp.message.register(generate_custom_password, 
                      PasswordGenerator.waiting_for_options, 
                      lambda message: message.text == "Сгенерировать")
    
    return dp 