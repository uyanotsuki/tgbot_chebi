import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);
''')

conn.commit()  # Сохраняем изменения
conn.close()   # Закрываем соединение с базой данных

print("База данных и таблица успешно созданы!")
