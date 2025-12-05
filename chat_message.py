"""
Simple ChatMessage class for Streamlit chat interface.
This is a compatibility layer for langchain_core.messages.chat.ChatMessage
"""

from typing import Optional


class ChatMessage:
    """Simple chat message class with role and content."""
    
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def __repr__(self):
        return f"ChatMessage(role={self.role!r}, content={self.content!r})"

