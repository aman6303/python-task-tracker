# contain service or methods that will be used by the program

from typing import List, Optional
from python_task_tracker.models import Task

from python_task_tracker.database import add_task, get_all_tasks, mark_done, delete_task

# method to create task and adding it to db

def create_task(title: str, priority: str = "medium", due_date: Optional[str] = None, description: str = "") -> Task:
    tid = add_task(title, priority, due_date, description)
    return Task(id=tid, title=title, priority=priority, due_date=due_date, description=description)


# method to list tasks after fetching from DB
def list_task(status: Optional[str] = None) -> List[Task]:
    return get_all_tasks(status)


# method to mark complete
def complete_task(task_id: int) -> bool:
    return mark_done(task_id)

# method to delete a task
def remove_task(task_id: int) -> bool:
    return delete_task(task_id)

# we NOT need to create all this methods separately, we can directly use database operations
