"""
Task service layer for the Todo CLI application.
Handles business logic for task operations.
"""
from typing import Optional, List
from .models import InMemoryTaskStorage, Task


class TaskService:
    """
    Service layer for task operations.
    """
    def __init__(self):
        self.storage = InMemoryTaskStorage()

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task.

        Args:
            title: Required task title
            description: Optional task description

        Returns:
            The created Task object

        Raises:
            ValueError: If title is empty
        """
        if not title or not title.strip():
            raise ValueError("Task title is required")
        return self.storage.add_task(title, description)

    def list_tasks(self) -> List[Task]:
        """
        List all tasks.

        Returns:
            List of all Task objects
        """
        return self.storage.get_all_tasks()

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        return self.storage.get_task(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated Task object if found, None otherwise
        """
        return self.storage.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        return self.storage.delete_task(task_id)

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            Updated Task object if found, None otherwise
        """
        return self.storage.mark_complete(task_id)

    def mark_task_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            Updated Task object if found, None otherwise
        """
        return self.storage.mark_incomplete(task_id)