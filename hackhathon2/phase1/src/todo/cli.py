"""
CLI interface for the Todo CLI application.
"""
import sys
from typing import Optional
from .service import TaskService


class TodoCLI:
    """
    Command-line interface for the todo application.
    """
    def __init__(self):
        self.service = TaskService()

    def run(self):
        """
        Run the CLI application.
        """
        # Always enter menu mode for user-friendly experience
        self._menu_mode()

    def _menu_mode(self):
        """Run the CLI in menu mode with numbered options."""
        print("=====================================")
        print("      TODO LIST APPLICATION")
        print("=====================================")
        print()

        while True:
            # Display current tasks
            self._display_tasks()
            print()
            print("OPTIONS:")
            print("1. Add Task")
            print("2. View All Tasks")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Mark Task Complete")
            print("6. Mark Task Incomplete")
            print("7. Exit")
            print()

            try:
                choice = input("Enter your choice (1-7): ").strip()

                if choice == '1':
                    self._add_task_menu()
                elif choice == '2':
                    self._view_tasks_menu()
                elif choice == '3':
                    self._update_task_menu()
                elif choice == '4':
                    self._delete_task_menu()
                elif choice == '5':
                    self._mark_complete_menu()
                elif choice == '6':
                    self._mark_incomplete_menu()
                elif choice == '7':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1-7.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    def _display_tasks(self):
        """Display all tasks in a formatted way."""
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks available. Add some tasks!")
            return

        print("CURRENT TASKS:")
        print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
        print("-" * 60)

        for task in tasks:
            status = "✓" if task.completed else "✗"
            description = task.description if task.description else ""
            print(f"{task.id:<4} {status:<8} {task.title:<30} {description}")

    def _add_task_menu(self):
        """Menu for adding a task."""
        print("\n--- ADD NEW TASK ---")
        title = input("Enter task title: ").strip()

        if not title:
            print("Title cannot be empty!")
            return

        description = input("Enter task description (optional, press Enter to skip): ").strip()
        if not description:
            description = None

        try:
            task = self.service.add_task(title, description)
            print(f"✓ Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"✗ Error: {e}")

    def _view_tasks_menu(self):
        """Menu for viewing tasks."""
        print("\n--- ALL TASKS ---")
        self._display_tasks()

    def _update_task_menu(self):
        """Menu for updating a task."""
        print("\n--- UPDATE TASK ---")
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks available to update.")
            return

        task_id = input("Enter task ID to update: ").strip()
        try:
            task_id = int(task_id)
        except ValueError:
            print("✗ Error: Task ID must be a number")
            return

        task = self.service.get_task(task_id)
        if not task:
            print(f"✗ Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: {task.title}")
        if task.description:
            print(f"Current description: {task.description}")

        new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
        if not new_title:
            new_title = None  # Keep current title
        elif new_title == task.title:
            new_title = None  # Keep current title if same input

        new_description = input(f"Enter new description (current: '{task.description or 'None'}', press Enter to keep current): ").strip()
        if new_description == '':
            new_description = None  # Keep current or set to None
        elif new_description == (task.description or ''):
            new_description = None  # Keep current if same input

        updated_task = self.service.update_task(task_id, new_title, new_description)
        if updated_task:
            print(f"✓ Task {task_id} updated successfully")
        else:
            print(f"✗ Error: Failed to update task {task_id}")

    def _delete_task_menu(self):
        """Menu for deleting a task."""
        print("\n--- DELETE TASK ---")
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks available to delete.")
            return

        task_id = input("Enter task ID to delete: ").strip()
        try:
            task_id = int(task_id)
        except ValueError:
            print("✗ Error: Task ID must be a number")
            return

        success = self.service.delete_task(task_id)
        if success:
            print(f"✓ Task {task_id} deleted successfully")
        else:
            print(f"✗ Error: Task with ID {task_id} not found.")

    def _mark_complete_menu(self):
        """Menu for marking a task as complete."""
        print("\n--- MARK TASK COMPLETE ---")
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks available to mark complete.")
            return

        task_id = input("Enter task ID to mark complete: ").strip()
        try:
            task_id = int(task_id)
        except ValueError:
            print("✗ Error: Task ID must be a number")
            return

        task = self.service.mark_task_complete(task_id)
        if task:
            print(f"✓ Task {task_id} marked as complete")
        else:
            print(f"✗ Error: Task with ID {task_id} not found.")

    def _mark_incomplete_menu(self):
        """Menu for marking a task as incomplete."""
        print("\n--- MARK TASK INCOMPLETE ---")
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks available to mark incomplete.")
            return

        task_id = input("Enter task ID to mark incomplete: ").strip()
        try:
            task_id = int(task_id)
        except ValueError:
            print("✗ Error: Task ID must be a number")
            return

        task = self.service.mark_task_incomplete(task_id)
        if task:
            print(f"✓ Task {task_id} marked as incomplete")
        else:
            print(f"✗ Error: Task with ID {task_id} not found.")

    def _handle_add(self, args):
        """Handle the add command (for backward compatibility)."""
        try:
            task = self.service.add_task(args.title, args.description)
            print(f"Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def _handle_list(self, args=None):
        """Handle the list command (for backward compatibility)."""
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
        print("-" * 60)

        for task in tasks:
            status = "✓" if task.completed else "✗"
            description = task.description if task.description else ""
            print(f"{task.id:<4} {status:<8} {task.title:<30} {description}")

    def _handle_update(self, args):
        """Handle the update command (for backward compatibility)."""
        task = self.service.get_task(args.id)
        if not task:
            print(f"Error: Task with ID {args.id} not found.", file=sys.stderr)
            sys.exit(1)

        updated_task = self.service.update_task(args.id, args.title, args.description)
        if updated_task:
            print(f"Task {args.id} updated successfully")
        else:
            print(f"Error: Failed to update task {args.id}", file=sys.stderr)
            sys.exit(1)

    def _handle_delete(self, args):
        """Handle the delete command (for backward compatibility)."""
        success = self.service.delete_task(args.id)
        if success:
            print(f"Task {args.id} deleted successfully")
        else:
            print(f"Error: Task with ID {args.id} not found.", file=sys.stderr)
            sys.exit(1)

    def _handle_complete(self, args):
        """Handle the complete command (for backward compatibility)."""
        task = self.service.mark_task_complete(args.id)
        if task:
            print(f"Task {args.id} marked as complete")
        else:
            print(f"Error: Task with ID {args.id} not found.", file=sys.stderr)
            sys.exit(1)

    def _handle_incomplete(self, args):
        """Handle the incomplete command (for backward compatibility)."""
        task = self.service.mark_task_incomplete(args.id)
        if task:
            print(f"Task {args.id} marked as incomplete")
        else:
            print(f"Error: Task with ID {args.id} not found.", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()