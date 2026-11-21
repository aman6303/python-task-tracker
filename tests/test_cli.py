import io
import unittest
from unittest.mock import patch
import tempfile
from pathlib import Path

import python_task_tracker.database as db
from python_task_tracker.main import main


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db_path = Path(self.temp_dir.name) / "test_task.db"

        self.original_db_path = db.DB_PATH
        db.DB_PATH = self.test_db_path
        db.init_db()

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_cli_add_command(self):
        with patch("sys.argv", ["main.py", "add", "Test Task", "-p", "high", "--desc", "Test Details"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("Created task 'Test Task'", output)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")
        self.assertEqual(tasks[0].priority, "high")
        self.assertEqual(tasks[0].description, "Test Details")

    def test_cli_add_title_too_long(self):
        long_title = "This title has more than 20 characters"
        with patch("sys.argv", ["main.py", "add", long_title]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("Title cannot have more than 20 letters", output)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_cli_list_command(self):
        db.add_task("First Task", "low", description="Desc 1")
        with patch("sys.argv", ["main.py", "list"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("First Task", output)
                self.assertIn("low", output)
                self.assertIn("Desc 1", output)

    def test_cli_done_command(self):
        task_id = db.add_task("Finish homework")
        with patch("sys.argv", ["main.py", "done", str(task_id)]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn(f"Task {task_id} marked as done", output)

        tasks = db.get_all_tasks()
        self.assertEqual(tasks[0].status, "done")

    def test_cli_delete_command(self):
        task_id = db.add_task("Discard task")
        with patch("sys.argv", ["main.py", "delete", str(task_id)]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn(f"Task {task_id} deleted", output)

        tasks = db.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_cli_default_calls_interactive_menu(self):
        with patch("sys.argv", ["main.py"]):
            with patch("python_task_tracker.main.interactive_menu") as mock_interactive:
                main()
                mock_interactive.assert_called_once()


if __name__ == "__main__":
    unittest.main()
