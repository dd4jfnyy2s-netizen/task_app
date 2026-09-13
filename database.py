import sqlite3

conn = sqlite3.connect("task.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE  IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    password TEXT,
    UNIQUE (name)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    completed INTEGER DEFAULT 0
    )
""")

conn.commit()

conn.close()