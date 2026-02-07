"""
OpenSDK AI agent initialization and configuration.
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Note: OpenSDK is a placeholder - actual implementation would use the real OpenSDK library
# For now, this provides the structure and interface that would integrate with OpenSDK


class AIAgent:
    """AI agent for processing chat messages and executing tools."""

    def __init__(self):
        """Initialize the AI agent with OpenRouter configuration."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "meta-llama/llama-3.2-3b-instruct:free"
        self.tools = []

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not configured")

    def register_tool(self, name: str, description: str, function: callable, parameters: Dict[str, Any]):
        """
        Register an MCP tool with the agent.

        Args:
            name: Tool name
            description: Tool description
            function: Tool function to execute
            parameters: Tool parameter schema
        """
        self.tools.append({
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters,
        })

    async def process_message(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        jwt_token: str,
    ) -> str:
        """
        Process a user message and generate AI response.

        Args:
            message: User message content
            conversation_history: Previous messages in conversation
            jwt_token: JWT token for tool authentication

        Returns:
            AI-generated response
        """
        # TODO: Integrate with actual OpenSDK/OpenRouter API
        # For now, provide a placeholder response that demonstrates the flow

        # Simulate AI processing
        response = await self._simulate_ai_response(message, jwt_token)
        return response

    async def _simulate_ai_response(self, message: str, jwt_token: str) -> str:
        """
        Simulate AI response (placeholder for actual OpenSDK integration).

        Args:
            message: User message
            jwt_token: JWT token

        Returns:
            Simulated response
        """
        message_lower = message.lower()

        # IMPORTANT: Check LIST first, before COMPLETE
        # This prevents "show me my complete tasks" from triggering complete action

        # Check if message is about listing tasks
        if any(keyword in message_lower for keyword in ["list", "show", "what", "tasks", "todos", "my tasks", "my todos", "how many"]):
            # Determine if filtering by completion status
            completed_filter = None
            if any(keyword in message_lower for keyword in ["incomplete", "active", "pending", "not done", "unfinished"]):
                completed_filter = False
            elif any(keyword in message_lower for keyword in ["complete", "completed", "done", "finished"]):
                completed_filter = True

            # Extract keyword for search
            keyword = None
            if "about" in message_lower or "containing" in message_lower or "with" in message_lower:
                # Try to extract search keyword
                for phrase in ["about", "containing", "with"]:
                    if phrase in message_lower:
                        parts = message_lower.split(phrase, 1)
                        if len(parts) > 1:
                            keyword = parts[1].strip().split()[0] if parts[1].strip() else None

            from .tools.list_tasks import list_tasks
            result = await list_tasks(jwt_token, completed=completed_filter, keyword=keyword)

            if result.get("success"):
                tasks = result.get("data", {}).get("tasks", [])
                count = result.get("data", {}).get("count", 0)

                if count == 0:
                    if completed_filter is False:
                        return "You don't have any incomplete tasks. Great job! 🎉"
                    elif completed_filter is True:
                        return "You haven't completed any tasks yet. Keep going!"
                    else:
                        return "You don't have any tasks yet. Would you like to create one?"

                # Format task list
                status_text = ""
                if completed_filter is False:
                    status_text = "incomplete "
                elif completed_filter is True:
                    status_text = "completed "

                task_list = []
                for i, task in enumerate(tasks[:10], 1):  # Show first 10 tasks
                    status_icon = "✓" if task.get("completed") else "○"
                    title = task.get("title", "Untitled")
                    task_list.append(f"{i}. {status_icon} {title}")

                formatted_list = "\n".join(task_list)

                if count > 10:
                    formatted_list += f"\n\n... and {count - 10} more tasks"

                return f"Here are your {status_text}tasks ({count} total):\n\n{formatted_list}"
            else:
                return f"I couldn't retrieve your tasks. Error: {result.get('error', 'Unknown error')}"

        # Check if message is about completing/marking a task as done
        # IMPORTANT: Check for "incomplete" first to avoid false matches
        elif (any(keyword in message_lower for keyword in ["complete", "finish"]) and "incomplete" not in message_lower) or \
           ("mark" in message_lower and "done" in message_lower) or \
           ("done" in message_lower and "with" in message_lower):
            # First, get all tasks to find the one to complete
            from .tools.list_tasks import list_tasks
            from .tools.toggle_task import toggle_task

            tasks_result = await list_tasks(jwt_token, completed=False)

            if not tasks_result.get("success"):
                return f"I couldn't retrieve your tasks. Error: {tasks_result.get('error', 'Unknown error')}"

            tasks = tasks_result.get("data", {}).get("tasks", [])

            if not tasks:
                return "You don't have any incomplete tasks to complete."

            # Try to find the task by matching keywords in the message
            task_to_complete = None
            for task in tasks:
                task_title_lower = task.get("title", "").lower()
                # Check if any words from the task title are in the message
                title_words = task_title_lower.split()
                if any(word in message_lower for word in title_words if len(word) > 3):
                    task_to_complete = task
                    break

            if not task_to_complete:
                # If no match found, complete the first task
                task_to_complete = tasks[0]

            # Toggle the task
            result = await toggle_task(jwt_token, str(task_to_complete.get("id")))

            if result.get("success"):
                task = result.get("data", {}).get("task", {})
                return f"✓ Marked '{task.get('title')}' as completed! Great job!"
            else:
                return f"I couldn't complete the task. Error: {result.get('error', 'Unknown error')}"

        # Check if message is about deleting a task
        elif any(keyword in message_lower for keyword in ["delete", "remove"]) or \
             ("get" in message_lower and "rid" in message_lower):
            # First, get all tasks to find the one to delete
            from .tools.list_tasks import list_tasks
            from .tools.delete_task import delete_task

            tasks_result = await list_tasks(jwt_token)

            if not tasks_result.get("success"):
                return f"I couldn't retrieve your tasks. Error: {tasks_result.get('error', 'Unknown error')}"

            tasks = tasks_result.get("data", {}).get("tasks", [])

            if not tasks:
                return "You don't have any tasks to delete."

            # Try to find the task by matching keywords in the message
            task_to_delete = None
            for task in tasks:
                task_title_lower = task.get("title", "").lower()
                # Check if any words from the task title are in the message
                title_words = task_title_lower.split()
                if any(word in message_lower for word in title_words if len(word) > 3):
                    task_to_delete = task
                    break

            if not task_to_delete:
                # If no match found, ask for clarification
                task_list = "\n".join([f"{i+1}. {task.get('title')}" for i, task in enumerate(tasks[:5])])
                return f"Which task would you like to delete? Here are your tasks:\n\n{task_list}\n\nPlease be more specific."

            # Delete the task
            result = await delete_task(jwt_token, str(task_to_delete.get("id")))

            if result.get("success"):
                return f"✓ Deleted '{task_to_delete.get('title')}' from your task list."
            else:
                return f"I couldn't delete the task. Error: {result.get('error', 'Unknown error')}"

        # Check if message is about updating a task
        elif any(keyword in message_lower for keyword in ["update", "change", "modify", "edit", "rename"]):
            # First, get all tasks to find the one to update
            from .tools.list_tasks import list_tasks
            from .tools.update_task import update_task

            tasks_result = await list_tasks(jwt_token)

            if not tasks_result.get("success"):
                return f"I couldn't retrieve your tasks. Error: {tasks_result.get('error', 'Unknown error')}"

            tasks = tasks_result.get("data", {}).get("tasks", [])

            if not tasks:
                return "You don't have any tasks to update."

            # Try to find the task by matching keywords in the message
            task_to_update = None
            for task in tasks:
                task_title_lower = task.get("title", "").lower()
                # Check if any words from the task title are in the message
                title_words = task_title_lower.split()
                if any(word in message_lower for word in title_words if len(word) > 3):
                    task_to_update = task
                    break

            if not task_to_update:
                # If no match found, ask for clarification
                task_list = "\n".join([f"{i+1}. {task.get('title')}" for i, task in enumerate(tasks[:5])])
                return f"Which task would you like to update? Here are your tasks:\n\n{task_list}\n\nPlease be more specific."

            # Extract new title from message (improved extraction)
            new_title = None

            # Try to find text after "to" keyword
            if " to " in message.lower():
                parts = message.lower().split(" to ", 1)
                if len(parts) > 1:
                    new_title = parts[1].strip()

            # If no "to" found, try basic extraction
            if not new_title:
                new_title = message
                for keyword in ["update", "change", "modify", "edit", "rename", "the", "task"]:
                    new_title = new_title.lower().replace(keyword, "")
                new_title = new_title.strip()

                # Remove the old task title from the new title
                old_title_words = task_to_update.get("title", "").lower().split()
                for word in old_title_words:
                    new_title = new_title.replace(word, "")
                new_title = new_title.strip()

            if not new_title:
                return f"What would you like to change '{task_to_update.get('title')}' to?"

            # Update the task
            result = await update_task(jwt_token, str(task_to_update.get("id")), title=new_title)

            if result.get("success"):
                task = result.get("data", {}).get("task", {})
                return f"✓ Updated task to: '{task.get('title')}'"
            else:
                return f"I couldn't update the task. Error: {result.get('error', 'Unknown error')}"

        # Check if message is about creating a task
        elif any(keyword in message_lower for keyword in ["create", "add", "new task", "todo", "remind me"]):
            # Extract task title from message (simple extraction)
            title = message
            for keyword in ["create a task to", "create task to", "add a task to", "add task to", "create", "add", "task", "todo", "remind me to", "remind me about"]:
                title = title.lower().replace(keyword, "")
            title = title.strip()

            if not title:
                title = "New task from chat"

            # Simulate calling create_task tool
            from .tools.create_task import create_task
            result = await create_task(jwt_token, title=title, description="")

            if result.get("success"):
                task = result.get("data", {}).get("task", {})
                return f"✓ I've created a task: '{task.get('title', title)}'. You can see it in your task list!"
            else:
                return f"I couldn't create the task. Error: {result.get('error', 'Unknown error')}"

        # Default response
        return (
            "I'm your AI task assistant! I can help you:\n\n"
            "📝 Create tasks: 'Create a task to buy groceries'\n"
            "📋 List tasks: 'Show me my tasks' or 'What are my incomplete tasks?'\n"
            "✓ Complete tasks: 'Mark the grocery task as done'\n"
            "✏️ Update tasks: 'Change the grocery task to include eggs'\n"
            "🗑️ Delete tasks: 'Delete the grocery task'\n\n"
            "What would you like to do?"
        )


# Global agent instance
_agent_instance: Optional[AIAgent] = None


def get_agent() -> AIAgent:
    """Get or create the global AI agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = AIAgent()
        _register_tools(_agent_instance)
    return _agent_instance


def _register_tools(agent: AIAgent):
    """Register all MCP tools with the agent."""
    from .tools.list_tasks import list_tasks
    from .tools.create_task import create_task
    from .tools.get_task import get_task
    from .tools.delete_task import delete_task
    from .tools.toggle_task import toggle_task
    from .tools.update_task import update_task

    # Register list_tasks tool
    agent.register_tool(
        name="list_tasks",
        description="List all tasks for the authenticated user, optionally filtered by completion status",
        function=list_tasks,
        parameters={
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status (optional)",
                }
            },
        },
    )

    # Register create_task tool
    agent.register_tool(
        name="create_task",
        description="Create a new task for the authenticated user",
        function=create_task,
        parameters={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Task title (required)",
                },
                "description": {
                    "type": "string",
                    "description": "Task description (optional)",
                },
            },
            "required": ["title"],
        },
    )

    # Register get_task tool
    agent.register_tool(
        name="get_task",
        description="Get details of a specific task by ID",
        function=get_task,
        parameters={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "Task ID to retrieve",
                }
            },
            "required": ["task_id"],
        },
    )

    # Register delete_task tool
    agent.register_tool(
        name="delete_task",
        description="Delete a task by ID",
        function=delete_task,
        parameters={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "Task ID to delete",
                }
            },
            "required": ["task_id"],
        },
    )

    # Register toggle_task tool
    agent.register_tool(
        name="toggle_task",
        description="Toggle the completion status of a task",
        function=toggle_task,
        parameters={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "Task ID to toggle",
                }
            },
            "required": ["task_id"],
        },
    )

    # Register update_task tool
    agent.register_tool(
        name="update_task",
        description="Update a task's title, description, or completion status",
        function=update_task,
        parameters={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "Task ID to update",
                },
                "title": {
                    "type": "string",
                    "description": "New task title (optional)",
                },
                "description": {
                    "type": "string",
                    "description": "New task description (optional)",
                },
                "completed": {
                    "type": "boolean",
                    "description": "New completion status (optional)",
                },
            },
            "required": ["task_id"],
        },
    )
