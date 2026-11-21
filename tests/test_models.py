import unittest
from python_task_tracker.models import Task


class TestTaskModel(unittest.TestCase):
    def test_task_creation_with_defaults(self):
        task = Task(id=1, title="Buy groceries")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.priority, "medium")
        self.assertEqual(task.status, "todo")
        self.assertIsNone(task.due_date)
        self.assertEqual(task.description, "")

    def test_task_creation_with_custom_values(self):
        task = Task(
            id=2,
            title="Submit report",
            priority="high",
            due_date="2026-12-01",
            status="done",
            description="Q4 financial report",
        )
        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Submit report")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.due_date, "2026-12-01")
        self.assertEqual(task.status, "done")
        self.assertEqual(task.description, "Q4 financial report")


if __name__ == "__main__":
    unittest.main()
