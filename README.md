# 🤖 Telegram-бот для юридической помощи
Этот Telegram-бот предоставляет бесплатную юридическую помощь жителям Чебоксар, позволяя пользователям выбрать район, тип помощи, указать имя и телефон, а также выбрать время записи к юристу.

## 📦 Установка
1. Клонируйте репозиторий:
   ```bash
    git clone https://github.com/uyanotsuki/tgbot_chebi.git
2. Создайте виртуальное окружение:
    ```bash
   python -m venv .venv
3. Активируйте виртуальное окружение:
   ```bash
   .venv\Scripts\activate
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   (Или вручную: pip install aiogram python-dotenv)

## 🚀 Запуск бота
```bash
python bot.py


## 📁 Структура проекта
legal-help-bot/
- ├── bot.py                  
- ├── auth.py                 \# Обработка имени и телефона через FSM
- ├── start.py                \# Стартовые сообщения и логика
- ├── db_init.py              \# Создание SQLite базы данных
- ├── users.db                \# Файл базы данных (создаётся автоматически)
- ├── .env                    \# Хранение токена бота
- ├── config.py               \# Загрузка переменных окружения
- └── README.md


### 🗄️ База данных
Используется встроенная база данных SQLite. Файл users.db создаётся автоматически с таблицей

### 🧰 Используемые библиотеки
- aiofiles==24.1.0
- aiogram==3.20.0.post0
- aiohappyeyeballs==2.6.1
- aiohttp==3.11.18
- aiosignal==1.3.2
- annotated-types==0.7.0
- attrs==25.3.0
- certifi==2025.4.26
- frozenlist==1.6.0
- idna==3.10
- magic-filter==1.0.12
- multidict==6.4.3
- propcache==0.3.1
- pydantic==2.11.4
- pydantic_core==2.33.2
- python-dotenv==1.1.0
- typing-inspection==0.4.0
- typing_extensions==4.13.2
- yarl==1.20.0
