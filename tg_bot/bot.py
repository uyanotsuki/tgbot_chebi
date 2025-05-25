import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext # для состояний FSM
from dotenv import load_dotenv  # для контекста FSM
from auth import cmd_start, process_name, process_phone, Form  # Импортируем из auth.py
from start import start


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Подключаем обработчики авторизации
dp.message.register(cmd_start, CommandStart())
dp.message.register(process_name, StateFilter(Form.name))
dp.message.register(process_phone, StateFilter(Form.phone))

# 👇 словарь со списком юристов
lawyers_schedule = {
    "Консультирование в области семейного, трудового, гражданского и прочего права": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Юрист-консультант",
            "name": "Иванова А.А.",
            "time": "Пн 10:00, Пн 13:00, Ср 14:00", 
            # "time": "5 Мая Пн 10:00, 5 Мая Пн 13:00, 7 Мая Ср 14:00", 
            "address": "г. Чебоксары, ул. Гагарина, д. 12, подъезд 2"
        },
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Юрист-аналитик",
            "name": "Григорьев В.И.",
            "time": "9 Мая Пт 13:00, 9 Мая Пт 15:00",
            "address": "Проспект Мира, 3, подъезд 1"
        }
    ],
    "Подготовка и подача исков, претензий, жалоб": [
        {
            "institution": "Московский районный суд",
            "role": "Юрист по гражданским делам",
            "name": "Смирнова Л.В.",
            "time": "6 Мая Вт 09:00, 6 Мая Вт 14:45, 8 Мая Чт 10:00, 9 Мая Пт 13:30",
            "address": "Улица Ленина, 45, подъезд 3"
        },
        {
            "institution": "Московский районный суд",
            "role": "Юрист по гражданским делам",
            "name": "Алексеев И.М.",
            "time": "16 Мая Ср 09:00, 17 Мая Чт 10:00, 18 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        },
        {
            "institution": "Московский районный суд",
            "role": "Юрист по гражданским делам",
            "name": "Демидова С.Н",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Сопровождение сделок с недвижимостью": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Юрист по недвижимости",
            "name": "Кузнецова И.Г.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Решение наследственных споров и оформление наследства": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус",
            "name": "Мельникова Т.Д.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        },
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Юрист по имущественным спорам",
            "name": "Орлов А.С.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        },
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Юрист по правам собственности",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Защита авторских прав": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Обжалование решений суда": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Возврат водительских прав": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Жилищные вопросы": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Представление прав в исполнительном производстве": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Правовая экспертиза договоров": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Помощь в спорах с банками и в борьбе с коллекторами": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ],
    "Получение гражданства и вида на жительство": [
        {
            "institution": "Центр правовой помощи Ленинского района",
            "role": "Нотариус по вопросам авторского права",
            "name": "Быков Т.О.",
            "time": "5 Мая Пн 09:00, 7 Мая Ср 10:15, 9 Мая Пт 13:30",
            "address": "Улица Октябрьская, 18, подъезд 5"
        }
    ]
}

# 👇 Меню с районами

# 👇 Меню с видами юр. помощи
services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Консультирование в области семейного, трудового, гражданского и прочего права")],
        [KeyboardButton(text="Подготовка и подача исков, претензий, жалоб")],
        [KeyboardButton(text="Сопровождение сделок с недвижимостью")],
        [KeyboardButton(text="Решение наследственных споров и оформлениенаследства")],
        [KeyboardButton(text="Защита авторских прав")],
        [KeyboardButton(text="Обжалование решений суда")],
        [KeyboardButton(text="Возврат водительских прав")],
        [KeyboardButton(text="Жилищные вопросы")],
        [KeyboardButton(text="Представление прав в исполнительном производстве")],
        [KeyboardButton(text="Правовая экспертиза договоров")],
        [KeyboardButton(text="Помощь в спорах с банками и в борьбе с коллекторами")],
        [KeyboardButton(text="Получение гражданства и вида на жительство")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
# async def start(message: types.Message):
#     await message.answer("Добро пожаловать! ЮрПомощь Чебоксары — сервис для записи на приём в государственные учреждения. Выберите район Ваш проживания, чтобы продолжить: ", reply_markup=district_kb)

@dp.message(lambda message: message.text in ["Калининский район", "Ленинский район", "Московский район", "Заволжское территориальное управление"])
async def district_selected(message: types.Message):
    await message.answer(
        f"Ваш район: {message.text}\nТеперь выберите вид услуги:",
        reply_markup=services_kb
    )

from aiogram.utils.keyboard import InlineKeyboardBuilder

@dp.message(lambda message: message.text in lawyers_schedule)
async def service_selected(message: types.Message):
    selected_service = message.text
    schedule = lawyers_schedule[selected_service]

    institution = schedule[0].get("institution", "—")

    response = f"🏬 <b>Учреждение:</b> {institution}\n\n"
    response += f"<b>Вы выбрали услугу:</b>\n{selected_service}\n\n"
    response += "<b>Доступные сотрудники:</b>\n"

    days_map = {
        "Пн": "Понедельник",
        "Вт": "Вторник",
        "Ср": "Среда",
        "Чт": "Четверг",
        "Пт": "Пятница",
        "Сб": "Суббота",
        "Вс": "Воскресенье"
    }

    builder = InlineKeyboardBuilder()  # обязательно создать экземпляр билдера

    for lawyer in schedule:
        response += f"<b>Должность:</b> {lawyer.get('role', '—')}\n"
        response += f"👩🏻‍💻 <b>{lawyer['name']}</b>\n"
        response += f"<b>Время записи:</b>\n"

        time_slots = lawyer['time'].split(", ")
        for slot in time_slots:
            try:
                day_code, hour = slot.strip().split(" ")
                full_day = days_map.get(day_code, day_code)
                response += f" 🕒 {full_day} - {hour}\n"
                # match = re.match(r"(\d{1,2} [А-Яа-я]+) (\d{1,2}:\d{2})", slot.strip())
                # if match:
                #     day_code = match.group(1)
                #     hour = match.group(2)
                #     full_day = days_map.get(day_code.split()[1], day_code.split()[1])  # Переводим день
                #     response += f" 🕒 {full_day} - {hour}\n"
            except ValueError:
                continue

        response += "\n"

        # кнопка с именем специалиста
        builder.button(text=lawyer["name"], callback_data=f"choose_lawyer:{lawyer['name']}")

    builder.adjust(1)  # по одной кнопке в ряд

    await message.answer(response, parse_mode="HTML")
    await message.answer("👩🏻‍💻Выберите специалиста:", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith("choose_lawyer:"))
async def choose_lawyer(callback: CallbackQuery):
    name = callback.data.split(":")[1]

    for lawyers in lawyers_schedule.values():
        for lawyer in lawyers:
            if lawyer["name"] == name:
                builder = InlineKeyboardBuilder()
                for slot in lawyer['time'].split(", "):
                    builder.button(text=slot, callback_data=f"choose_time:{name}:{slot}")
                await callback.message.answer(
                    f"📌 Специалист: <b>{name}</b>\nВыберите удобное для Вас время:",
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
                await callback.answer()
                return
    await callback.answer("Юрист не найден", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("choose_time:"))
async def choose_time(callback: CallbackQuery):
    _, name, time_slot = callback.data.split(":", 2)
    address = None  # Здесь будем хранить адрес юриста

    for service, lawyers in lawyers_schedule.items():
        for lawyer in lawyers:
            if lawyer['name'] == name:
                address = lawyer['address']
                break
        if address:
            break

    if address:
        await callback.message.answer(
            f"Вы успешно записаны к <b>{name}</b> на {time_slot}. ✅\n\n"
            f"📍 Адрес: {address}",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer("Ошибка❌ Юрист с таким именем не найден.")
    await callback.answer("Запись подтверждена")
    


async def main():
    print("Бот запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())