from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
import random

from keyboards import (
    get_main_keyboard,
    get_probability_game_keyboard,
    get_coin_keyboard,
    get_dice_keyboard,
    get_even_odd_keyboard
)
from states import ProbabilityGame

async def probability_game_menu(message: types.Message, state: FSMContext):
    await state.set_state(ProbabilityGame.choosing_game)
    await message.answer("Выберите игру:", reply_markup=get_probability_game_keyboard())

# Монетка
async def coin_game(message: types.Message, state: FSMContext):
    await message.answer("Нажмите, чтобы подбросить монетку:", reply_markup=get_coin_keyboard())

async def toss_coin(message: types.Message, state: FSMContext):
    result = random.choice(["Орёл 🦅", "Решка 💰"])
    await message.answer(f"Выпало: {result}", reply_markup=get_coin_keyboard())

# Кости
async def dice_game(message: types.Message, state: FSMContext):
    await message.answer("Нажмите, чтобы кинуть кости:", reply_markup=get_dice_keyboard())

async def roll_dice(message: types.Message, state: FSMContext):
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    await message.answer(f"Кости показали: 🎲 {die1} и 🎲 {die2}", reply_markup=get_dice_keyboard())

# Чет/нечет
async def even_odd_game(message: types.Message, state: FSMContext):
    await message.answer("Нажмите, чтобы крутить рулетку:", reply_markup=get_even_odd_keyboard())

async def spin_even_odd(message: types.Message, state: FSMContext):
    number = random.randint(1, 100)
    parity = "Четное ⚖️" if number % 2 == 0 else "Нечетное 🌀"
    await message.answer(f"Выпало число {number} — {parity}", reply_markup=get_even_odd_keyboard())

def register_probability_handlers(dp):
    dp.message.register(probability_game_menu, lambda m: m.text == "🎲 Игра вероятности")
    dp.message.register(coin_game, lambda m: m.text == "🪙 Монетка", StateFilter(ProbabilityGame.choosing_game))
    dp.message.register(toss_coin, lambda m: m.text == "Кинуть монетку")
    dp.message.register(dice_game, lambda m: m.text == "🎲 Кости", StateFilter(ProbabilityGame.choosing_game))
    dp.message.register(roll_dice, lambda m: m.text == "Кинуть кости")
    dp.message.register(even_odd_game, lambda m: m.text == "🔄 Чет/нечет", StateFilter(ProbabilityGame.choosing_game))
    dp.message.register(spin_even_odd, lambda m: m.text == "Крутить рулетку")
    return dp