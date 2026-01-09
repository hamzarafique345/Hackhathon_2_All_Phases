# Data Model: The Evolution of Todo – Phase I: In-Memory Python Console Application

## Task Entity

### Attributes
- **id** (Integer)
  - Type: int
  - Description: Unique identifier for the task
  - Constraints: Auto-generated, positive integer, unique across all tasks
  - Required: Yes (system-generated)

- **title** (String)
  - Type: str
  - Description: The main title/description of what needs to be done
  - Constraints: Non-empty string, required field
  - Required: Yes

- **description** (String)
  - Type: str or None
  - Description: Additional details about the task
  - Constraints: Optional, can be None or empty string
  - Required: No

- **completed** (Boolean)
  - Type: bool
  - Description: Whether the task has been completed
  - Constraints: Boolean value, defaults to False
  - Required: Yes (system-defaulted)

### Relationships
- None (standalone entity)

### Validation Rules
1. Title must not be empty or None when creating a task
2. ID must be positive integer
3. Completed status must be boolean
4. Task with given ID must exist before update/delete operations

### State Transitions
- `completed = False` → `completed = True`: When task is marked complete
- `completed = True` → `completed = False`: When task is marked incomplete

## In-Memory Storage Model

### Task Storage Structure
- **Data Structure**: Dictionary (dict)
- **Key**: Task ID (integer)
- **Value**: Task object/representation
- **Access Pattern**: O(1) lookup by ID

### Storage Operations
- **Create**: Add new entry to dictionary with auto-generated ID
- **Read**: Access by ID key
- **Update**: Modify existing entry by ID
- **Delete**: Remove entry by ID
- **List All**: Iterate through all values in dictionary

### ID Generation Strategy
- **Starting Value**: 1
- **Increment**: +1 for each new task
- **Collision Handling**: None needed (sequential generation)
- **Gap Handling**: IDs remain permanently assigned (no reuse after deletion)

## Data Integrity Constraints
1. No duplicate IDs
2. No null titles for active tasks
3. Consistent state during operations
4. Thread safety: Not required (CLI application, single-threaded)