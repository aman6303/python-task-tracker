
import sqlite3
from contextlib import contextmanager
from typing import List, Optional

from python_task_tracker.config import DB_PATH
from python_task_tracker.models import Task

# defining the context manager method for easy acess
@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# initialize sqlite database
def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                status TEXT DEFAULT 'todo',
                description TEXT
            )
            """
        )
        conn.commit()


# add new task to db
def add_task(title: str, priority: str = "medium", due_date: Optional[str] = None, description: str = "") -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, priority, due_date, description) VALUES (?, ?, ?, ?)", (title, priority, due_date, description)
        )
        conn.commit()
        if cursor.lastrowid is None:
            raise RuntimeError("Failed to retrieve lastrowid after inserting task")
        return cursor.lastrowid  # returning the last inserted row id


# method which will convert sqlite returned row into task model type (useful when getting the data from DB)
# making the method internal as private (with single underscore) so it will be used under this module
def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id = row["id"],
        title = row["title"],
        priority=row["priority"],
        due_date=row["due_date"],
        status=row["status"],
        description=row["description"] or "",

    )

# get all tasks from the database

def get_all_tasks(status: Optional[str] = None) -> List[Task]:
    with get_connection() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY due_date, priority DESC", # DESC means decending
                (status,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY due_date, priority DESC"
            ).fetchall()

        return [_row_to_task(r) for r in rows] # converting each row in task data model and the storing in list then returning


# method to mark down a task in database

def mark_done(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

# method to delete a task in databse

def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

