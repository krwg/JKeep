import sqlite3
from tkinter import messagebox

conn = None
cur = None

def db_start():
    global conn, cur
    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT,
                pinned INTEGER DEFAULT 0,
                formatted_text TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        messagebox.showerror("Error", "Database connection error.")

def close_db():
    global conn
    if conn:
        conn.close()

def get_notes():
    try:
        cur.execute("SELECT id, note, pinned, formatted_text FROM notes")
        return cur.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error getting list of notes: {e}")
        return []

def get_note_by_id(note_id):
    try:
        cur.execute("SELECT note, pinned, formatted_text FROM notes WHERE id=?", (note_id,))
        return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error receiving note: {e}")
        return None

def insert_note(note, formatted_text):
    try:
        cur.execute("INSERT INTO notes (note, formatted_text) VALUES (?, ?)", (note, formatted_text))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error saving note: {e}")

def update_note(note_id, note, formatted_text):
    try:
        cur.execute("UPDATE notes SET note=?, formatted_text=? WHERE id=?", (note, formatted_text, note_id))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error saving note: {e}")

def delete_note(note_id):
    try:
        cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error deleting note: {e}")

def update_pinned(note_id, pinned):
    try:
        cur.execute("UPDATE notes SET pinned=? WHERE id=?", (pinned, note_id))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error changing pin status: {e}")