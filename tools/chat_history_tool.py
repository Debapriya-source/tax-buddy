from langchain.tools import BaseTool
from typing import List
from langchain_core.messages import BaseMessage
from langchain.agents import tool


class ChatHistoryLookupTool(BaseTool):
    name: str = "chat_history_lookup"
    description: str = """
    Look up previous conversation history to understand context for follow-up questions.
    Use this tool when the user:
    - Asks follow-up questions like "tell me more about that", "what about the previous question"
    - References something mentioned earlier in the conversation
    - Uses pronouns like "it", "that", "this" without clear context
    - Asks for clarification on previous responses
    
    Input should be a search query or keyword to find relevant previous messages.
    Examples: "previous tax question", "deduction", "section 80C", "last question"
    """

    chat_history: List[BaseMessage] = []

    def __init__(self, chat_history: List[BaseMessage] = None):
        super().__init__()
        self.chat_history = chat_history or []

    def _run(self, query: str) -> str:
        """Look up chat history based on query."""
        if not self.chat_history:
            return "No previous conversation history available."

        # If query is empty or just asking for history, return recent messages
        if not query.strip() or query.lower() in ["history", "previous", "last"]:
            return self._get_recent_history(5)

        # Search for relevant messages
        relevant_messages = self._search_history(query.lower())

        if not relevant_messages:
            return f"No relevant previous messages found for '{query}'. Recent conversation:\n{self._get_recent_history(3)}"

        return self._format_messages(relevant_messages)

    def _search_history(self, query: str) -> List[tuple]:
        """Search chat history for relevant messages."""
        relevant = []
        query_words = query.split()

        for i, message in enumerate(self.chat_history):
            content_lower = message.content.lower()

            # Check if any query words are in the message content
            relevance_score = sum(1 for word in query_words if word in content_lower)

            if relevance_score > 0:
                relevant.append((i, message, relevance_score))

        # Sort by relevance score (descending) and recency
        relevant.sort(key=lambda x: (x[2], x[0]), reverse=True)

        # Return top 6 most relevant messages
        return relevant[:6]

    def _get_recent_history(self, count: int = 5) -> str:
        """Get the most recent messages."""
        if not self.chat_history:
            return "No conversation history available."

        recent_messages = (
            self.chat_history[-count:]
            if len(self.chat_history) > count
            else self.chat_history
        )
        return self._format_messages(
            [(i, msg, 1) for i, msg in enumerate(recent_messages)]
        )

    def _format_messages(self, messages: List[tuple]) -> str:
        """Format messages for display."""
        if not messages:
            return "No messages to display."

        formatted = "Previous conversation context:\n\n"

        for _, message, _ in messages:
            role = "User" if message.type == "human" else "Assistant"
            # Truncate very long messages
            content = (
                message.content[:400] + "..."
                if len(message.content) > 400
                else message.content
            )
            formatted += f"{role}: {content}\n\n"

        return formatted.strip()

    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        return self._run(query)


def create_chat_history_tool(chat_history: List[BaseMessage]) -> ChatHistoryLookupTool:
    """Factory function to create chat history tool with current history."""
    return ChatHistoryLookupTool(chat_history=chat_history)
