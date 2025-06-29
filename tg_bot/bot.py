import asyncio
import os
from aiogram import Bot, Dispatcher, types # type: ignore
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton # type: ignore
from aiogram.filters import CommandStart # type: ignore
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню с кнопками
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кто имеет право на получение БЮП?")],
        [KeyboardButton(text="Куда можно обратиться за получением БЮП?")],
        [KeyboardButton(text="Как с нами связаться?")],
        [KeyboardButton(text="Часто задаваемые вопросы и ответы")],
        # [KeyboardButton(text="Анкетирование")],
    ],
    resize_keyboard=True
)

# Клавиатура с кнопкой "Вернуться в главное меню"
back_to_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "🌟 Здравствуйте! Вас приветствует чат-бот, который расскажет Вам об оказании бесплатной юридической помощи на территории Чувашской Республики!\n"
        "Готов ответить на самые популярные вопросы.\n\n"
        "Пожалуйста, выберите из меню интересующий Вас вопрос:",
        reply_markup=main_menu_kb
    )

@dp.message(lambda m: m.text == "Кто имеет право на получение БЮП?")
async def categories_handler(message: types.Message):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Инвалиды I и II группы", callback_data="category_invalidy")],
        [InlineKeyboardButton(text="Малоимущие граждане", callback_data="category_maloimushhie")],
        [InlineKeyboardButton(text="Многодетные семьи", callback_data="category_mnogodetnye")],
        [InlineKeyboardButton(text="Участники СВО и их семьи", callback_data="category_svo")],
        [InlineKeyboardButton(text="Дети-инвалиды, сироты", callback_data="category_deti")],
        [InlineKeyboardButton(text="Ветераны ВОВ и боевых действий", callback_data="category_veterany")],
        [InlineKeyboardButton(
            text="Иные категории 👉",
            url="https://minust.cap.ru/deyateljnostj/activity/besplatnaya-yuridicheskaya-pomoschj/kategorii-grazhdan-imeyuschih-pravo-na-poluchenie"
        )],
    ])

    # Показываем категории и меняем клавиатуру на кнопку "Вернуться"
    await message.answer(
        "Категории граждан, которые имеют право на получение бесплатной юридической помощи.\n\n",
        reply_markup=back_to_main_kb  # заменяем клавиатуру на "Вернуться"
    )
    # Отправляем инлайн-кнопки с категориями отдельным сообщением (inline клавиатура не конфликтует с ReplyKeyboard)
    await message.answer(
        "Выберите одну из для подробной информации:",
        reply_markup=inline_kb
    )

@dp.callback_query(lambda c: c.data and c.data.startswith('category_'))
async def process_category_callback(callback_query: types.CallbackQuery):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Перечень документов",
            url="https://minust.cap.ru/deyateljnostj/activity/besplatnaya-yuridicheskaya-pomoschj/perechenj-dokumentov-na-osnovanii-kotorih-okazivae"
        )]
    ])

    category_names = {
        "category_invalidy": "Инвалиды I и II группы",
        "category_maloimushhie": "Малоимущие граждане",
        "category_mnogodetnye": "Многодетные семьи",
        "category_svo": "Участники СВО и их семьи",
        "category_deti": "Дети-инвалиды, сироты",
        "category_veterany": "Ветераны ВОВ и боевых действий",
    }

    category = callback_query.data
    category_name = category_names.get(category, "Категория")

    response_text = (
        f"Информация по категории: {category_name}.\n\n"
        "Для получения бесплатной юридической помощи гражданин или его представитель должен предоставить:\n\n"
        "• *паспорт* или иной документ, удостоверяющий личность гражданина Российской Федерации\n"
        "• *документы*, подтверждающие *отнесение его* к одной из категорий граждан\n\n"
    )

    await callback_query.answer()  # Убираем часы загрузки у кнопки
    await callback_query.message.answer(response_text, reply_markup=inline_kb, parse_mode='Markdown')

@dp.message(lambda m: m.text == "Куда можно обратиться за получением БЮП?")
async def where_to_go_handler(message: types.Message):
    await message.answer(
        "Бесплатная юридическая помощь оказывается в рамках государственной и негосударственной систем:\n\n"
        "•  Адвокаты\n"
        "•  КУ ЧР «Центр предоставления мер социальной поддержки» Минтруда Чувашии\n"
        "•  Исполнительные органы Чувашской Республики и подведомственные им учреждения\n"
        "•  Негосударственные центры бесплатной юридической помощи\n"
        "•  Юридические клиники при ВУЗах\n"
        "•  Социально ориентированные некоммерческие организации",
        reply_markup=back_to_main_kb  #Вернуться
    )

@dp.message(lambda m: m.text == "Как с нами связаться?")
async def contact_handler(message: types.Message):
    await message.answer(
        "📞 По всем возникающим вопросам можно позвонить в Госслужбу Чувашии по делам юстиции по номеру:\n\n"
        "<a href='tel:+78352565112'>(88352) 56-51-12</a>",
        reply_markup=back_to_main_kb,
        parse_mode='HTML'
    )

@dp.message(lambda m: m.text == "Часто задаваемые вопросы и ответы")
async def faq_handler(message: types.Message):
    await message.answer(
        "Ответы на часто задаваемые вопросы:\n\n"
        "👉 https://minust.cap.ru/deyateljnostj/activity/besplatnaya-yuridicheskaya-pomoschj/naibolee-chasto-zadavaemie-voprosi-grazhdan",
        reply_markup=back_to_main_kb
    )

@dp.message(lambda m: m.text == "Анкетирование")
async def survey_handler(message: types.Message):
    await message.answer(
        "Спасибо, что решили пройти анкетирование!\n\n(тут может быть ссылка или встроенный опрос)",
        reply_markup=back_to_main_kb
    )

@dp.message(lambda m: m.text == "⬅️ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")
async def back_to_main_menu(message: types.Message):
    await message.answer(
        "Вы вернулись в главное меню. Выберите интересующий вас вопрос:",
        reply_markup=main_menu_kb
    )

# Запуск
async def main():
    print("Бот запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())