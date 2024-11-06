import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            username TEXT,
            plan TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_timer_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timers (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            interval_hours INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()

#----------------------------------------------------------------------------------------------------------------------
"""users db"""

def register_user(user_id, username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)',
                       (user_id, username))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Пользователь уже зарегистрирован.")

    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id, ))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_plan(user_id, plan):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET plan = ? WHERE user_id = ?', (plan, user_id))

    conn.commit()
    conn.close()

#----------------------------------------------------------------------------------------------------------------------
"""timer table"""

def add_timer(user_id, start_time, end_time, interval_hours):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO timers (user_id, start_time, end_time, interval_hours) VALUES (?, ?, ?, ?)',
                   (user_id, start_time, end_time, interval_hours))

    conn.commit()
    conn.close()

def get_timer(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM timers WHERE user_id = ?', (user_id, ))
    timer = cursor.fetchone()
    conn.close()
    return timer

def update_timer(user_id, start_time, end_time, interval_hours):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE timers SET start_time = ?, end_time = ?, interval_hours = ? WHERE user_id = ?',
                   (start_time, end_time, interval_hours, user_id))

    conn.commit()
    conn.close()

def delete_timer(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM timers WHERE user_id = ?', (user_id, ))

    conn.commit()
    conn.close()