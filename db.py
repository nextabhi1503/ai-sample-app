import sqlite3

def init_db():
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()

def add_task(task, time):
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (task, time))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute("SELECT task, time FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return [{"task": row[0], "time": row[1]} for row in tasks]

def add_note(note):
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute("SELECT content FROM notes")
    notes = [row[0] for row in c.fetchall()]
    conn.close()
    return notes

def delete_task(task):
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE task = ?", (task,))
    conn.commit()
    conn.close()

def delete_note(note):
    conn = sqlite3.connect("assistant.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE content = ?", (note,))
    conn.commit()
    conn.close()