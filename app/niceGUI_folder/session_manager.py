"""
Session manager for storing multiple user sessions
"""
from typing import Optional, Dict, Any

# Хранилище сессий: session_id -> user_data
sessions: Dict[str, Dict[str, Any]] = {}


class SessionManager:
    """Session manager for multiple user sessions"""

    @staticmethod
    def set_current_user(user_data: Dict[str, Any], session_id: str):
        """Set user data for specific session"""
        sessions[session_id] = user_data

    @staticmethod
    def get_current_user(session_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by session_id"""
        return sessions.get(session_id)

    @staticmethod
    def is_authenticated(session_id: str) -> bool:
        """Check if session_id exists and is valid"""
        return session_id in sessions and sessions[session_id] is not None

    @staticmethod
    def clear_session(session_id: str):
        """Clear session by session_id"""
        if session_id in sessions:
            del sessions[session_id]
