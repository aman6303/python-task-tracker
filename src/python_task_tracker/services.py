# contain service that will be used by the program

from typing import List, Optional
from python_task_tracker.models import Task


def create_task(title: str, priority: str = "medium", due_date: Optional[str] = None, description: str = "") -> Task:
    tid = db_add