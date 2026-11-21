import unittest
import tempfile
from pathlib import Path

import python_task_tracker.database as db


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use an isolated temporary SQLite database for each test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db_path = Path(self.temp_dir.name) / "test_task.db"

        self.original_db_path = db.DB_PATH
        db.DB_PATH = self.test_db_path
        db.init_db()

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_init_db_creates_table(self):
        with db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
            )
            table = cursor.fetchone()
            self.assertIsNotNone(table)
            self.assertEqual(table["name"], "tasks")

    def test_add_task(self):
        task_id = db.add_task(
            title="Read book",
            priority="high",
            due_date="2026-11-30",
            description="Read 20 pages",
        )
        self.assertEqual(task_id, 1)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Read book")
        self.assertEqual(tasks[0].priority, "high")
        self.assertEqual(tasks[0].due_date, "2026-11-30")
        self.assertEqual(tasks[0].description, "Read 20 pages")
        self.assertEqual(tasks[0].status, "todo")

    def test_get_all_tasks_filtering(self):
        id1 = db.add_task("Task 1", "low")
        id2 = db.add_task("Task 2", "high")
        db.mark_done(id2)

        # All tasks
        all_tasks = db.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)

        # Filter by todo
        todo_tasks = db.get_all_tasks(status="todo")
        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0].id, id1)

        # Filter by done
        done_tasks = db.get_all_tasks(status="done")
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].id, id2)

    def test_mark_done(self):
        task_id = db.add_task("Write tests", "medium")
        success = db.mark_done(task_id)
        self.assertTrue(success)

        tasks = db.get_all_tasks()
        self.assertEqual(tasks[0].status, "done")

    def test_mark_done_non_existent_id(self):
        success = db.mark_done(999)
        self.assertFalse(success)

    def test_delete_task(self):
        task_id = db.add_task("Delete me", "low")
        success = db.delete_task(task_id)
        self.assertTrue(success)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_task_non_existent_id(self):
        success = db.delete_task(999)
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
