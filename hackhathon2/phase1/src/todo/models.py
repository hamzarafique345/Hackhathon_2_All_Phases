"""
Task model and in-memory storage for the Todo CLI application.
"""
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class Task:
    """
    Represents a todo task with ID, title, description, and completion status.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")


class InMemoryTaskStorage:
    """
    In-memory storage for tasks using a dictionary.
    """
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with a unique ID."""
        task = Task(id=self._next_id, title=title, description=description, completed=False)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update a task's title and/or description."""
        task = self._tasks.get(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as complete."""
        task = self._tasks.get(task_id)
        if task:
            task.completed = True
        return task

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """Mark a task as incomplete."""
        task = self._tasks.get(task_id)
        if task:
            task.completed = False
        return task