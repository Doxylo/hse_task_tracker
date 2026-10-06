import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DATABASE_PATH", "data/tasks.db"))

if not DB_PATH.is_absolute():
    DB_PATH = BASE_DIR / DB_PATH

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )''')

        connection.commit()
    finally:
        connection.close()

if __name__ == "__main__":
    init_db()

def get_all_tasks():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute("SELECT id, title, description, completed FROM tasks ORDER BY id").fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "completed": bool(row["completed"])
            }
            for row in rows
        ]
    finally:
        connection.close()

def insert_task(title: str, description: str):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute("INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)", (title, description))
        connection.commit()
        return {
            "id": cursor.lastrowid,
            "title": title,
            "description": description,
            "completed": False
        }
    finally:
        connection.close()

def mark_task_completed(task_id: int):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return None
        row = connection.execute("SELECT id, title, description, completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
        
        return {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "completed": bool(row["completed"]) 
        }
    finally:
        connection.close()