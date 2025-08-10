import sqlite3

def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        contact TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT,
        contact TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

