"""
Tests for the Task model and InMemoryTaskStorage.
"""
import unittest
from src.todo.models import Task, InMemoryTaskStorage


class TestTask(unittest.TestCase):
    """Tests for the Task class."""

    def test_task_creation(self):
        """Test creating a task with valid data."""
        task = Task(id=1, title="Test task", description="Test description", completed=False)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)

    def test_task_creation_defaults(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)

    def test_task_empty_title_error(self):
        """Test that creating a task with empty title raises an error."""
        with self.assertRaises(ValueError):
            Task(id=1, title="")

        with self.assertRaises(ValueError):
            Task(id=1, title="   ")


class TestInMemoryTaskStorage(unittest.TestCase):
    """Tests for the InMemoryTaskStorage class."""

    def setUp(self):
        """Set up a fresh storage for each test."""
        self.storage = InMemoryTaskStorage()

    def test_add_task(self):
        """Test adding a task."""
        task = self.storage.add_task("Test task", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        task = self.storage.add_task("Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)

    def test_get_task(self):
        """Test getting a task by ID."""
        task = self.storage.add_task("Test task")
        retrieved_task = self.storage.get_task(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        task = self.storage.get_task(999)
        self.assertIsNone(task)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        task1 = self.storage.add_task("Task 1")
        task2 = self.storage.add_task("Task 2")

        all_tasks = self.storage.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)
        self.assertIn(task1, all_tasks)
        self.assertIn(task2, all_tasks)

    def test_update_task(self):
        """Test updating a task."""
        task = self.storage.add_task("Original title", "Original description")

        updated_task = self.storage.update_task(task.id, "New title", "New description")
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

        # Verify the task was updated in storage
        retrieved_task = self.storage.get_task(task.id)
        self.assertEqual(retrieved_task.title, "New title")
        self.assertEqual(retrieved_task.description, "New description")

    def test_update_task_partial(self):
        """Test updating only title or description."""
        task = self.storage.add_task("Original title", "Original description")

        # Update only title
        updated_task = self.storage.update_task(task.id, title="New title")
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Original description")

        # Update only description
        updated_task = self.storage.update_task(task.id, description="New description")
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        result = self.storage.update_task(999, "New title")
        self.assertIsNone(result)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.storage.add_task("Test task")
        success = self.storage.delete_task(task.id)
        self.assertTrue(success)

        # Verify the task is gone
        retrieved_task = self.storage.get_task(task.id)
        self.assertIsNone(retrieved_task)

    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        success = self.storage.delete_task(999)
        self.assertFalse(success)

    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = self.storage.add_task("Test task")
        self.assertFalse(task.completed)

        marked_task = self.storage.mark_complete(task.id)
        self.assertTrue(marked_task.completed)

        # Verify the task was updated in storage
        retrieved_task = self.storage.get_task(task.id)
        self.assertTrue(retrieved_task.completed)

    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.storage.add_task("Test task")
        task.completed = True  # Manually mark as complete first

        marked_task = self.storage.mark_incomplete(task.id)
        self.assertFalse(marked_task.completed)

        # Verify the task was updated in storage
        retrieved_task = self.storage.get_task(task.id)
        self.assertFalse(retrieved_task.completed)

    def test_mark_nonexistent_task(self):
        """Test marking complete/incomplete a task that doesn't exist."""
        result = self.storage.mark_complete(999)
        self.assertIsNone(result)

        result = self.storage.mark_incomplete(999)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()