# Инлайн клавиатуры
# Задача "Ещё больше выбора"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = '76'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb_1 = InlineKeyboardMarkup(resize_keyboard=True)
button_r = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_f = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_1.row(button_r, button_f)

# инициализируем клавиатуру, с возможностью подстраивания под размеры интерфейса устройства
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Расчитать')   # создаём кнопки
button_2 = KeyboardButton(text='Информация')
kb.row(button_1, button_2)   # добавляем кнопки в клавиатуру  в ряд


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start_(message):
    await message.answer(text='Привет, я бот помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler(text = ['Расчитать'])
async def main_menu(message):                  # 1    main_menu
    await message.answer(text='Выберите опцию:', reply_markup=kb_1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):                  # 2
    await call.message.answer('(10 x вес(кг)) +(6,25 x рост(см)) – (5 x возраст(г) – 161')


@dp.callback_query_handler(text='calories')
async def set_age(call):                  # 3
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(text = ['Информация'])
async def inform(message):                 # Информация
    await message.answer('Это информация о боте')

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight'])) + (6.25 * float(data['growth'])) - (5 * int(data['age'])) - 161
    await message.answer(f"Ваша норма каллорий {result}")
    await state.finish()

@dp.message_handler()
async def start_any(message):
    await message.answer('Введите команду /start чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

