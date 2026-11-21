import unittest
import tempfile
from pathlib import Path

import python_task_tracker.database as db
from python_task_tracker.services import (
    create_task,
    list_task,
    complete_task,
    remove_task,
)
from python_task_tracker.models import Task


class TestServices(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db_path = Path(self.temp_dir.name) / "test_task.db"

        self.original_db_path = db.DB_PATH
        db.DB_PATH = self.test_db_path
        db.init_db()

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_create_task(self):
        task = create_task(
            title="Clean room",
            priority="low",
            due_date="2026-11-25",
            description="Vacuum and dust",
        )
        self.assertIsInstance(task, Task)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Clean room")
        self.assertEqual(task.priority, "low")
        self.assertEqual(task.due_date, "2026-11-25")
        self.assertEqual(task.description, "Vacuum and dust")

    def test_list_task(self):
        create_task("Task A", "medium")
        create_task("Task B", "high")

        tasks = list_task()
        self.assertEqual(len(tasks), 2)
        self.assertEqual({t.title for t in tasks}, {"Task A", "Task B"})

    def test_complete_task(self):
        task = create_task("Do laundry")
        self.assertTrue(complete_task(task.id))
        self.assertFalse(complete_task(999))

        tasks = list_task(status="done")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task.id)

    def test_remove_task(self):
        task = create_task("Pay bills")
        self.assertTrue(remove_task(task.id))
        self.assertFalse(remove_task(999))

        tasks = list_task()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
