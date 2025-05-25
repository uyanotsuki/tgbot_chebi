import sqlite3

# Функция для добавления пользователя
def add_user(name, phone):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

# Функция для получения пользователя по телефону
def get_user_by_phone(phone):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    user = cursor.fetchone()  # Получаем первую запись, если она есть
    conn.close()
    return user

# # Функция для получения всех пользователей из базы данных
# def get_all_users():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM users')
#     users = cursor.fetchall()
#     conn.close()
#     return users
