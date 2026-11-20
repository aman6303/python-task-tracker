# data models used in program

from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:

    # to track a task
    id: Optional[int]
    title: str
    priority: str = "medium"
    due_date: Optional[str] = None
    status: str = "todo" # it may be done or todo
    description: str = ""