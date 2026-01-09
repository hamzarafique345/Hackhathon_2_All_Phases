"""
Tests for the TaskService.
"""
import unittest
from src.todo.service import TaskService


class TestTaskService(unittest.TestCase):
    """Tests for the TaskService class."""

    def setUp(self):
        """Set up a fresh service for each test."""
        self.service = TaskService()

    def test_add_task_success(self):
        """Test adding a task successfully."""
        task = self.service.add_task("Test task", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        task = self.service.add_task("Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)

    def test_add_task_empty_title_error(self):
        """Test that adding a task with empty title raises an error."""
        with self.assertRaises(ValueError):
            self.service.add_task("")

        with self.assertRaises(ValueError):
            self.service.add_task("   ")

    def test_list_tasks_empty(self):
        """Test listing tasks when there are no tasks."""
        tasks = self.service.list_tasks()
        self.assertEqual(len(tasks), 0)

    def test_list_tasks_with_tasks(self):
        """Test listing tasks when there are tasks."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")

        tasks = self.service.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIn(task1, tasks)
        self.assertIn(task2, tasks)

    def test_get_task_exists(self):
        """Test getting a task that exists."""
        original_task = self.service.add_task("Test task")
        retrieved_task = self.service.get_task(original_task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, original_task.id)
        self.assertEqual(retrieved_task.title, original_task.title)

    def test_get_task_not_exists(self):
        """Test getting a task that doesn't exist."""
        task = self.service.get_task(999)
        self.assertIsNone(task)

    def test_update_task_success(self):
        """Test updating a task successfully."""
        original_task = self.service.add_task("Original title", "Original description")

        updated_task = self.service.update_task(original_task.id, "New title", "New description")
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

        # Verify the task was updated in storage
        retrieved_task = self.service.get_task(original_task.id)
        self.assertEqual(retrieved_task.title, "New title")
        self.assertEqual(retrieved_task.description, "New description")

    def test_update_task_partial(self):
        """Test updating only title or description."""
        original_task = self.service.add_task("Original title", "Original description")

        # Update only title
        updated_task = self.service.update_task(original_task.id, title="New title")
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Original description")

        # Update only description
        updated_task = self.service.update_task(original_task.id, description="New description")
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_task_not_exists(self):
        """Test updating a task that doesn't exist."""
        result = self.service.update_task(999, "New title")
        self.assertIsNone(result)

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        original_task = self.service.add_task("Test task")
        success = self.service.delete_task(original_task.id)
        self.assertTrue(success)

        # Verify the task is gone
        retrieved_task = self.service.get_task(original_task.id)
        self.assertIsNone(retrieved_task)

    def test_delete_task_not_exists(self):
        """Test deleting a task that doesn't exist."""
        success = self.service.delete_task(999)
        self.assertFalse(success)

    def test_mark_task_complete_success(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test task")
        self.assertFalse(task.completed)

        marked_task = self.service.mark_task_complete(task.id)
        self.assertTrue(marked_task.completed)

        # Verify the task was updated in storage
        retrieved_task = self.service.get_task(task.id)
        self.assertTrue(retrieved_task.completed)

    def test_mark_task_complete_not_exists(self):
        """Test marking complete a task that doesn't exist."""
        result = self.service.mark_task_complete(999)
        self.assertIsNone(result)

    def test_mark_task_incomplete_success(self):
        """Test marking a task as incomplete."""
        task = self.service.add_task("Test task")
        task.completed = True  # Manually mark as complete first

        marked_task = self.service.mark_task_incomplete(task.id)
        self.assertFalse(marked_task.completed)

        # Verify the task was updated in storage
        retrieved_task = self.service.get_task(task.id)
        self.assertFalse(retrieved_task.completed)

    def test_mark_task_incomplete_not_exists(self):
        """Test marking incomplete a task that doesn't exist."""
        result = self.service.mark_task_incomplete(999)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()