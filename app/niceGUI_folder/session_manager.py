"""
Simple session manager for storing current user data
"""
from typing import Optional, Dict, Any

# Global storage for current user (in production, use Redis or database)
_current_user: Optional[Dict[str, Any]] = None
_session_id: Optional[str] = None


class SessionManager:
    """Simple session manager"""
    
    @staticmethod
    def set_current_user(user_data: Dict[str, Any], session_id: str):
        """Set current user data"""
        global _current_user, _session_id
        _current_user = user_data
        _session_id = session_id
    
    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """Get current user data"""
        return _current_user
    
    @staticmethod
    def get_session_id() -> Optional[str]:
        """Get current session ID"""
        return _session_id
    
    @staticmethod
    def clear_session():
        """Clear current session"""
        global _current_user, _session_id
        _current_user = None
        _session_id = None
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return _current_user is not None
