# Quickstart Guide: The Evolution of Todo – Phase I: In-Memory Python Console Application

## Setup

1. **Install Python 3.11** (if not already installed)
2. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```
3. **Initialize the project**:
   ```bash
   uv init
   ```
4. **Navigate to the project directory** and install dependencies:
   ```bash
   uv pip install -e .
   ```

## Running the Application

To run the todo application:
```bash
python src/main.py --help
```

## Available Commands

### Add a Task
```bash
python src/main.py add --title "My Task Title" --description "Optional description here"
```

### View All Tasks
```bash
python src/main.py list
```

### Update a Task
```bash
python src/main.py update --id 1 --title "New Title" --description "New Description"
```

### Delete a Task
```bash
python src/main.py delete --id 1
```

### Mark Task as Complete
```bash
python src/main.py complete --id 1
```

### Mark Task as Incomplete
```bash
python src/main.py incomplete --id 1
```

## Example Workflow

1. **Add a task**:
   ```bash
   python src/main.py add --title "Buy groceries" --description "Milk, bread, eggs"
   ```

2. **View all tasks**:
   ```bash
   python src/main.py list
   ```

3. **Mark task as complete**:
   ```bash
   python src/main.py complete --id 1
   ```

4. **View tasks again**:
   ```bash
   python src/main.py list
   ```

## Error Handling

- If you try to update/delete/complete a non-existent task ID, the application will show an error message
- If you try to add a task without a title, the application will show an error message
- Invalid command usage will display help information

## Project Structure

- `src/main.py` - Application entry point
- `src/todo/models.py` - Task data model and storage
- `src/todo/service.py` - Business logic for task operations
- `src/todo/cli.py` - Command-line interface
- `tests/` - Unit tests for the application