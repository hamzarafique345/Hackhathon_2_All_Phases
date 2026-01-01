# The Evolution of Todo – Phase I: In-Memory Python Console Application

A simple and user-friendly CLI-based todo application built with Python 3.11 that manages tasks entirely in memory.

## Features

- Add new tasks with title and optional description
- View all tasks with ID and completion status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- In-memory storage (no persistence)
- Simple menu-based interface with numbered options
- User-friendly prompts and input validation

## Prerequisites

- Python 3.11
- uv (for dependency management)

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

3. **Install project dependencies**:
   ```bash
   uv sync
   ```

   Or if you want to install in development mode:
   ```bash
   uv develop
   ```

## Setup

1. **Initialize the project** (if starting fresh):
   ```bash
   uv init
   ```

2. **Make sure you're using Python 3.11**:
   ```bash
   python --version
   ```

   If you don't have Python 3.11, install it using your system's package manager or pyenv.

## Usage

### Running the Application

To run the todo application with the user-friendly menu interface:

```bash
python src/main.py
```

This will start the application in menu mode where you can:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

### Menu-Based Interface (Recommended)

When you run `python src/main.py`, you'll see a menu with numbered options:

```
=====================================
      TODO LIST APPLICATION
=====================================

CURRENT TASKS:
ID   Status   Title                         Description
------------------------------------------------------------
No tasks available. Add some tasks!

OPTIONS:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice (1-7):
```

Simply enter the number of the option you want to use.

### Working Process

1. **Starting the Application**:
   - Run `python src/main.py`
   - The menu will appear with all your current tasks displayed
   - Enter a number (1-7) to select an option

2. **Adding a Task**:
   - Select option 1
   - Enter the task title when prompted
   - Enter an optional description (or press Enter to skip)

3. **Viewing Tasks**:
   - Select option 2
   - All tasks will be displayed with their ID, status (✓/✗), title, and description

4. **Updating a Task**:
   - Select option 3
   - Enter the task ID you want to update
   - Enter new title or description when prompted (or press Enter to keep current)

5. **Deleting a Task**:
   - Select option 4
   - Enter the task ID you want to delete

6. **Marking Complete/Incomplete**:
   - Select option 5 (complete) or 6 (incomplete)
   - Enter the task ID you want to change

7. **Exiting**:
   - Select option 7 to exit the application

### Command-Line Interface (Alternative)

For advanced users, you can still use the original command-line interface:

#### Add a Task
```bash
python src/main.py add --title "My Task Title" --description "Optional description here"
```

#### View All Tasks
```bash
python src/main.py list
```

#### Update a Task
```bash
python src/main.py update --id 1 --title "New Title" --description "New Description"
```

#### Delete a Task
```bash
python src/main.py delete --id 1
```

#### Mark Task as Complete
```bash
python src/main.py complete --id 1
```

#### Mark Task as Incomplete
```bash
python src/main.py incomplete --id 1
```

### Example Workflow

1. **Start the application**:
   ```bash
   python src/main.py
   ```

2. **Add a task** (option 1):
   - Enter "Buy groceries" as title
   - Enter "Milk, bread, eggs" as description

3. **View all tasks** (option 2):
   - See your tasks displayed in a table

4. **Mark task as complete** (option 5):
   - Enter the task ID (e.g., 1)

5. **Exit the application** (option 7)

## Storage Mechanism

The application uses **in-memory storage only**. All tasks are stored in a Python dictionary within the application's memory space:

- **Storage Location**: In-memory dictionary (`_tasks: Dict[int, Task]`)
- **Data Persistence**: None - all data is lost when the application exits
- **Task IDs**: Auto-incrementing integers starting from 1
- **Storage Type**: Python `dict` with integer keys and `Task` object values
- **Access Time**: O(1) lookup by task ID

### Storage Details
- **File**: `src/todo/models.py`
- **Class**: `InMemoryTaskStorage`
- **Dictionary Structure**: `self._tasks: Dict[int, Task]` where key is task ID and value is the Task object
- **Next ID Tracking**: `self._next_id: int` starts at 1 and increments for each new task

### Data Lifecycle
1. Data exists only during the application runtime
2. All data is stored in memory until the application terminates
3. When application exits, all data is automatically cleared
4. New application instance starts with empty storage

## Project Structure

```
src/
├── main.py                 # Application entry point
├── todo/
│   ├── __init__.py
│   ├── models.py          # Task data model and in-memory storage
│   ├── service.py         # Business logic for task operations
│   └── cli.py             # Command-line interface
└── tests/
    ├── __init__.py
    ├── test_models.py     # Tests for data models
    ├── test_service.py    # Tests for service layer
    └── test_cli.py        # Tests for CLI interface
```

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- **Models (`models.py`)**: Data structures and storage logic
- **Service (`service.py`)**: Business logic and task operations
- **CLI (`cli.py`)**: Command-line interface and user interaction
- **Main (`main.py`)**: Application entry point

## Running Tests

To run the unit tests:

```bash
python -m unittest discover tests/
```

Or run specific test files:

```bash
python -m unittest tests.test_models
python -m unittest tests.test_service
python -m unittest tests.test_cli
```

## Development

### Adding Dependencies

If you need to add new dependencies (though the current implementation uses only standard library):

```bash
uv pip install <package-name>
```

### Project Philosophy

This application follows these principles:
- In-memory storage only (no databases or file persistence)
- User-friendly menu-based interface
- Clean architecture with separation of concerns
- Standard Python library only (no external dependencies)
- User-friendly error messages

## Error Handling

- If you try to update/delete/complete a non-existent task ID, the application will show an error message
- If you try to add a task without providing a title, the application will show an error as title is required
- Invalid input will prompt for correct input

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests to ensure everything works (`python -m unittest discover tests/`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

[Specify your license here]