from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from start import start, district_kb
from database import add_user, get_user_by_phone
import re
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Form(StatesGroup):
    name = State()
    phone = State()

# Функция для проверки номера телефона
def is_valid_phone(phone):
    # Регулярное выражение для проверки формата +7XXXXXXXXXX
    pattern = r'^\+7\d{10}$'
    return re.match(pattern, phone)

# Декоратор для команды /start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)  # Переход к состоянию "name"
    await message.answer("Добро пожаловать!🌟\n \nЮрПомощь Чебоксары — сервис для записи на приём в государственные учреждения.\n \nЧтобы начать пользоваться ботом введите ваше ФИО:")

# Обработка введенного имени
async def process_name(message: types.Message, state: FSMContext):
    # Сохраняем ФИО в контексте FSM
    await state.update_data(name=message.text)
    await state.set_state(Form.phone)  # Переход к состоянию "phone"
    await message.answer("Теперь введите ваш номер телефона:")

# Обработка введенного номера телефона
async def process_phone(message: types.Message, state: FSMContext):
    support_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="📩 Написать в поддержку", 
        url="https://www.youtube.com/watch?v=1F3OGIFnW1k&list=PLiQyj3m-vBew0phFUFwrt4QQj0j7Z3w-f&index=24"
    )]
    ])
    phone = message.text

    # Проверка формата номера
    if not is_valid_phone(phone):
        await message.answer("Ошибка❗ Пожалуйста, введите номер телефона в формате +7XXXXXXXXXX")
        return
    
    await state.update_data(phone=phone)  # Сохраняем номер
    user_data = await state.get_data()
    name = user_data['name']

    # Проверка, есть ли уже пользователь с таким номером
    existing_user = get_user_by_phone(phone)
    if existing_user:
        if existing_user[1] != name:  # Сравниваем ФИО
            await message.answer(
                "Ошибка❌\nЭтот номер уже зарегистрирован под другим именем.\nЕсли вы уверены, что это ошибка — напишите в поддержку.",
                reply_markup=support_kb
            )
            await state.clear()
            return
        else:
            await message.answer(
                "Авторизация успешна🌟",
                reply_markup=district_kb
            )
            await state.clear()
            await start(message)
            return

    # Добавляем пользователя в базу данных
    add_user(name, phone)

     # Проверяем, добавился ли пользователь
    user_in_db = get_user_by_phone(phone)
    if user_in_db:
        print(f"Пользователь добавлен в базу данных:\nФИО: {user_in_db[1]}\nТелефон: {user_in_db[2]}")
    else:
        print("Что-то пошло не так, пользователь не добавлен!")

    # Выводим данные пользователя
    await message.answer(
        f"Авторизация успешна✅\nВаши данные:\nФИО: {name}\nТелефон: {phone}",
        reply_markup=district_kb  # Предлагаем меню с районами
    )

    await state.clear()  # Очищаем состояние после завершения авторизации

    # После авторизации передаем управление в start, чтобы вывести меню районов
    await start(message)  # Убедись, что start импортирован и вызывается