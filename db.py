import sqlite3


def make_table():
    conn = None
    try:
        conn = sqlite3.connect('log.db')
        c = conn.cursor()
        c.execute("""
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY,
            status text,
            date timestamp 
        )
        """)
        print("Successfully created table")
    except sqlite3.OperationalError:
        # Database already exists
        print("Table already exists")
        pass
    finally:
        if conn:
            conn.commit()
            conn.close()


def check_last_row():
    conn = None
    try:
        conn = sqlite3.connect('log.db')
        c = conn.cursor()
        c.execute("""
        SELECT * FROM logs ORDER BY id DESC LIMIT 1;
        """)
        lastStatus = c.fetchone()
    finally:
        if conn:
            conn.close()

    return lastStatus


def insert_status(status):
    conn = None
    try:
        conn = sqlite3.connect('log.db')
        c = conn.cursor()
        c.execute("INSERT INTO logs (status, date) VALUES (?, DATE('now')) ", status)
    finally:
        if conn:
            conn.commit()
            conn.close()
