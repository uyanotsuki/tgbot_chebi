from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

district_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Калининский район")],
        [KeyboardButton(text="Ленинский район")],
        [KeyboardButton(text="Московский район")],
        [KeyboardButton(text="Заволжское территориальное управление")]
    ],
    resize_keyboard=True
)

async def start(message: types.Message):
    await message.answer(
        # "Добро пожаловать!🌟\n \nЮрПомощь Чебоксары — сервис для записи на приём в государственные учреждения.\n"
        "\nВыберите Ваш район  проживания, чтобы продолжить: ",
        reply_markup=district_kb
    )