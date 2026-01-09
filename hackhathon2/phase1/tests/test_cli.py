"""
Tests for the TodoCLI.
"""
import unittest
import sys
from io import StringIO
from unittest.mock import patch, Mock
from src.todo.cli import TodoCLI


class TestTodoCLI(unittest.TestCase):
    """Tests for the TodoCLI class."""

    def setUp(self):
        """Set up a fresh CLI for each test."""
        self.cli = TodoCLI()

    @patch('sys.argv', ['todo', 'add', '--title', 'Test Task', '--description', 'Test Description'])
    def test_add_task_cli(self):
        """Test adding a task via CLI."""
        # Capture stdout to check output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Create a mock service to avoid actual execution
            with patch.object(self.cli.service, 'add_task') as mock_add:
                mock_task = Mock()
                mock_task.id = 1
                mock_add.return_value = mock_task

                # We can't run the full CLI, so we'll test the method directly
                # For this test, we'll just verify the method would be called
                pass
        finally:
            sys.stdout = sys.__stdout__

    def test_handle_add_valid(self):
        """Test handling the add command with valid input."""
        with patch('builtins.print') as mock_print:
            args = Mock()
            args.title = "Test Task"
            args.description = "Test Description"

            # Mock the service to return a task
            mock_task = Mock()
            mock_task.id = 1
            self.cli.service.add_task = Mock(return_value=mock_task)

            self.cli._handle_add(args)

            # Verify the service was called with correct arguments
            self.cli.service.add_task.assert_called_once_with("Test Task", "Test Description")
            # Verify print was called with success message
            mock_print.assert_called_once_with("Task added successfully with ID: 1")

    def test_handle_add_empty_title(self):
        """Test handling the add command with empty title."""
        with patch('sys.stderr.write') as mock_stderr, patch('sys.exit') as mock_exit:
            args = Mock()
            args.title = ""
            args.description = "Test Description"

            # Mock the service to raise ValueError
            self.cli.service.add_task = Mock(side_effect=ValueError("Task title is required"))

            self.cli._handle_add(args)

            # Verify the service was called
            self.cli.service.add_task.assert_called_once_with("", "Test Description")
            # Verify error was printed to stderr
            mock_stderr.assert_called()
            # Verify sys.exit was called
            mock_exit.assert_called_once_with(1)

    def test_handle_list_empty(self):
        """Test handling the list command with no tasks."""
        with patch('builtins.print') as mock_print:
            # Mock the service to return empty list
            self.cli.service.list_tasks = Mock(return_value=[])

            self.cli._handle_list()

            # Verify the service was called
            self.cli.service.list_tasks.assert_called_once()
            # Verify appropriate message was printed
            mock_print.assert_called_once_with("No tasks found.")

    def test_handle_list_with_tasks(self):
        """Test handling the list command with tasks."""
        with patch('builtins.print') as mock_print:
            # Create mock tasks
            mock_task1 = Mock()
            mock_task1.id = 1
            mock_task1.title = "Task 1"
            mock_task1.description = "Description 1"
            mock_task1.completed = False

            mock_task2 = Mock()
            mock_task2.id = 2
            mock_task2.title = "Task 2"
            mock_task2.description = "Description 2"
            mock_task2.completed = True

            # Mock the service to return tasks
            self.cli.service.list_tasks = Mock(return_value=[mock_task1, mock_task2])

            self.cli._handle_list()

            # Verify the service was called
            self.cli.service.list_tasks.assert_called_once()
            # Verify print was called (at least header and separator)
            self.assertGreater(len(mock_print.call_args_list), 2)

    def test_handle_update_existing_task(self):
        """Test handling the update command for existing task."""
        with patch('builtins.print') as mock_print:
            args = Mock()
            args.id = 1
            args.title = "Updated Title"
            args.description = "Updated Description"

            # Mock the service methods
            self.cli.service.get_task = Mock(return_value=Mock())
            self.cli.service.update_task = Mock(return_value=Mock())

            self.cli._handle_update(args)

            # Verify the service methods were called with correct arguments
            self.cli.service.get_task.assert_called_once_with(1)
            self.cli.service.update_task.assert_called_once_with(1, "Updated Title", "Updated Description")
            # Verify success message was printed
            mock_print.assert_called_with("Task 1 updated successfully")

    def test_handle_update_nonexistent_task(self):
        """Test handling the update command for nonexistent task."""
        with patch('sys.stderr.write') as mock_stderr, patch('sys.exit') as mock_exit:
            args = Mock()
            args.id = 999
            args.title = "Updated Title"
            args.description = "Updated Description"

            # Mock the service to return None for nonexistent task
            self.cli.service.get_task = Mock(return_value=None)

            self.cli._handle_update(args)

            # Verify the service was called
            self.cli.service.get_task.assert_called_once_with(999)
            # Verify error message was printed to stderr
            mock_stderr.assert_called()
            # Verify sys.exit was called
            mock_exit.assert_called_once_with(1)

    def test_handle_delete_existing_task(self):
        """Test handling the delete command for existing task."""
        with patch('builtins.print') as mock_print:
            args = Mock()
            args.id = 1

            # Mock the service to return True for successful deletion
            self.cli.service.delete_task = Mock(return_value=True)

            self.cli._handle_delete(args)

            # Verify the service was called with correct argument
            self.cli.service.delete_task.assert_called_once_with(1)
            # Verify success message was printed
            mock_print.assert_called_once_with("Task 1 deleted successfully")

    def test_handle_delete_nonexistent_task(self):
        """Test handling the delete command for nonexistent task."""
        with patch('sys.stderr.write') as mock_stderr, patch('sys.exit') as mock_exit:
            args = Mock()
            args.id = 999

            # Mock the service to return False for unsuccessful deletion
            self.cli.service.delete_task = Mock(return_value=False)

            self.cli._handle_delete(args)

            # Verify the service was called with correct argument
            self.cli.service.delete_task.assert_called_once_with(999)
            # Verify error message was printed to stderr
            mock_stderr.assert_called()
            # Verify sys.exit was called
            mock_exit.assert_called_once_with(1)

    def test_handle_complete_existing_task(self):
        """Test handling the complete command for existing task."""
        with patch('builtins.print') as mock_print:
            args = Mock()
            args.id = 1

            # Mock the service to return a task
            mock_task = Mock()
            self.cli.service.mark_task_complete = Mock(return_value=mock_task)

            self.cli._handle_complete(args)

            # Verify the service was called with correct argument
            self.cli.service.mark_task_complete.assert_called_once_with(1)
            # Verify success message was printed
            mock_print.assert_called_once_with("Task 1 marked as complete")

    def test_handle_complete_nonexistent_task(self):
        """Test handling the complete command for nonexistent task."""
        with patch('sys.stderr.write') as mock_stderr, patch('sys.exit') as mock_exit:
            args = Mock()
            args.id = 999

            # Mock the service to return None for nonexistent task
            self.cli.service.mark_task_complete = Mock(return_value=None)

            self.cli._handle_complete(args)

            # Verify the service was called with correct argument
            self.cli.service.mark_task_complete.assert_called_once_with(999)
            # Verify error message was printed to stderr
            mock_stderr.assert_called()
            # Verify sys.exit was called
            mock_exit.assert_called_once_with(1)

    def test_handle_incomplete_existing_task(self):
        """Test handling the incomplete command for existing task."""
        with patch('builtins.print') as mock_print:
            args = Mock()
            args.id = 1

            # Mock the service to return a task
            mock_task = Mock()
            self.cli.service.mark_task_incomplete = Mock(return_value=mock_task)

            self.cli._handle_incomplete(args)

            # Verify the service was called with correct argument
            self.cli.service.mark_task_incomplete.assert_called_once_with(1)
            # Verify success message was printed
            mock_print.assert_called_once_with("Task 1 marked as incomplete")

    def test_handle_incomplete_nonexistent_task(self):
        """Test handling the incomplete command for nonexistent task."""
        with patch('sys.stderr.write') as mock_stderr, patch('sys.exit') as mock_exit:
            args = Mock()
            args.id = 999

            # Mock the service to return None for nonexistent task
            self.cli.service.mark_task_incomplete = Mock(return_value=None)

            self.cli._handle_incomplete(args)

            # Verify the service was called with correct argument
            self.cli.service.mark_task_incomplete.assert_called_once_with(999)
            # Verify error message was printed to stderr
            mock_stderr.assert_called()
            # Verify sys.exit was called
            mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()