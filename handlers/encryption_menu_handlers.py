from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards import get_encryption_methods_keyboard, get_main_keyboard
from states import EncryptionMenu

# Handler for the encryption menu button
async def cmd_encryption_menu(message: types.Message, state: FSMContext):
    await message.reply(
        "Выберите метод шифрования:",
        reply_markup=get_encryption_methods_keyboard()
    )
    await state.set_state(EncryptionMenu.choosing_method)

# Обработчик выбора метода шифрования
async def process_encryption_method_selection(message: types.Message, state: FSMContext):
    # Не очищаем состояние здесь, это будет сделано в конкретных обработчиках
    # Используем метод pass_to_parent для правильной обработки запроса
    return message

# Функция регистрации обработчиков
def register_encryption_menu_handlers(dp):
    dp.message.register(cmd_encryption_menu, lambda message: message.text == "🔐 Шифрование")
    dp.message.register(process_encryption_method_selection, EncryptionMenu.choosing_method)
    
    return dp 
