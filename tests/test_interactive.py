import io
import unittest
from unittest.mock import patch
import tempfile
from pathlib import Path

import python_task_tracker.database as db
from python_task_tracker.main import interactive_menu


class TestInteractiveMenu(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db_path = Path(self.temp_dir.name) / "test_task.db"

        self.original_db_path = db.DB_PATH
        db.DB_PATH = self.test_db_path
        db.init_db()

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_quit_immediately(self):
        with patch("builtins.input", side_effect=["q"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                interactive_menu()
                output = mock_stdout.getvalue()
                self.assertIn("thanks for using the program", output)

    def test_add_task_interactive(self):
        # 1: Add task -> title -> priority -> due -> desc -> q: quit
        inputs = ["1", "Interactive Task", "high", "2026-12-31", "My description", "q"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                interactive_menu()
                output = mock_stdout.getvalue()
                self.assertIn("Created task 'Interactive Task'", output)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Interactive Task")
        self.assertEqual(tasks[0].priority, "high")
        self.assertEqual(tasks[0].due_date, "2026-12-31")
        self.assertEqual(tasks[0].description, "My description")

    def test_add_task_validation_reprompts(self):
        # 1: Add task -> empty title (fails) -> title > 20 chars (fails) -> valid title -> priority -> due -> desc -> q
        too_long = "This title is way too long to be valid"
        inputs = ["1", "", too_long, "Short Title", "low", "", "", "q"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                interactive_menu()
                output = mock_stdout.getvalue()
                self.assertIn("Title cannot be empty.", output)
                self.assertIn("Title cannot have more than 20 letters.", output)
                self.assertIn("Created task 'Short Title'", output)

    def test_list_tasks_interactive(self):
        db.add_task("Existing Task", "medium")
        inputs = ["2", "all", "q"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                interactive_menu()
                output = mock_stdout.getvalue()
                self.assertIn("Existing Task", output)

    def test_mark_done_interactive(self):
        task_id = db.add_task("To be done", "high")
        inputs = ["3", str(task_id), "q"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                interactive_menu()
                output = mock_stdout.getvalue()
                self.assertIn("Task marked as done.", output)

        tasks = db.get_all_tasks()
        self.assertEqual(tasks[0].status, "done")

    def test_delete_interactive(self):
        task_id = db.add_task("To be deleted", "low")
        inputs = ["4", str(task_id), "q"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                interactive_menu()
                output = mock_stdout.getvalue()
                self.assertIn("Task deleted.", output)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
