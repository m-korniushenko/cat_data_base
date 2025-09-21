"""
Authentication Service for managing user sessions and permissions
Following SOLID principles - Single Responsibility Principle
"""
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.database_folder.orm import AsyncOrm


class AuthService:
    """Service for managing user authentication and sessions"""
    
    # Permission levels
    ADMIN_PERMISSION = 1  # Full access
    OWNER_PERMISSION = 2  # View own cats only, no editing
    
    # Session storage (in production, use Redis or database)
    _active_sessions: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user by email and password
        Returns user data if successful, None otherwise
        """
        try:
            # Get all owners with retry logic
            owners = []
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    _, owners = await AsyncOrm.get_owner()
                    break
                except Exception as e:
                    print(f"Database access attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        import asyncio
                        await asyncio.sleep(1)  # Wait 1 second before retry
                    else:
                        raise e
            
            if not owners:
                print("No owners found in database")
                return None
            
            # Find owner by email
            owner = None
            for o in owners:
                if o.get('owner_email') == email:
                    owner = o
                    break
            
            if not owner:
                print(f"No owner found with email: {email}")
                return None
            
            # Check password (assuming password is already hashed in database)
            hashed_password = cls.hash_password(password)
            if owner.get('owner_hashed_password') != hashed_password:
                print(f"Password mismatch for email: {email}")
                return None
            
            # Return user data
            return {
                'owner_id': owner.get('owner_id'),
                'owner_firstname': owner.get('owner_firstname'),
                'owner_surname': owner.get('owner_surname'),
                'owner_email': owner.get('owner_email'),
                'owner_permission': owner.get('owner_permission', 0),
                'login_time': datetime.now()
            }
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    @classmethod
    def create_session(cls, user_data: Dict[str, Any]) -> str:
        """Create a new session and return session ID"""
        import uuid
        session_id = str(uuid.uuid4())
        
        # Store session data
        cls._active_sessions[session_id] = {
            'user_data': user_data,
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        
        return session_id
    
    @classmethod
    def get_session(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data by session ID"""
        if session_id not in cls._active_sessions:
            return None
        
        session = cls._active_sessions[session_id]
        
        # Check if session is expired (24 hours)
        if datetime.now() - session['created_at'] > timedelta(hours=24):
            del cls._active_sessions[session_id]
            return None
        
        # Update last activity
        session['last_activity'] = datetime.now()
        return session
    
    @classmethod
    def get_current_user(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current user data from session"""
        session = cls.get_session(session_id)
        if session:
            return session['user_data']
        return None
    
    @classmethod
    def logout_user(cls, session_id: str) -> bool:
        """Logout user by removing session"""
        if session_id in cls._active_sessions:
            del cls._active_sessions[session_id]
            return True
        return False
    
    @classmethod
    def has_permission(cls, user_data: Dict[str, Any], required_permission: int) -> bool:
        """Check if user has required permission level"""
        user_permission = user_data.get('owner_permission', 0)
        
        # Admin (permission 1) has access to everything
        if user_permission == cls.ADMIN_PERMISSION:
            return True
        
        # Owner (permission 2) has limited access
        if user_permission == cls.OWNER_PERMISSION:
            return required_permission <= cls.OWNER_PERMISSION
        
        # No permission for others
        return False
    
    @classmethod
    def can_edit_cat(cls, user_data: Dict[str, Any], cat_owner_id: int) -> bool:
        """Check if user can edit a specific cat"""
        user_permission = user_data.get('owner_permission', 0)
        user_id = user_data.get('owner_id')
        
        # Admin can edit all cats
        if user_permission == cls.ADMIN_PERMISSION:
            return True
        
        # Owner can only view their own cats (no editing)
        if user_permission == cls.OWNER_PERMISSION:
            return False  # Owners cannot edit
        
        return False
    
    @classmethod
    def can_view_cat(cls, user_data: Dict[str, Any], cat_owner_id: int) -> bool:
        """Check if user can view a specific cat"""
        user_permission = user_data.get('owner_permission', 0)
        user_id = user_data.get('owner_id')
        
        # Admin can view all cats
        if user_permission == cls.ADMIN_PERMISSION:
            return True
        
        # Owner can view their own cats
        if user_permission == cls.OWNER_PERMISSION:
            return user_id == cat_owner_id
        
        return False
    
    @classmethod
    def get_user_cats_filter(cls, user_data: Dict[str, Any]) -> Optional[int]:
        """Get owner_id filter for cats based on user permission"""
        user_permission = user_data.get('owner_permission', 0)
        user_id = user_data.get('owner_id')
        
        # Admin can see all cats
        if user_permission == cls.ADMIN_PERMISSION:
            return None  # No filter
        
        # Owner can only see their own cats
        if user_permission == cls.OWNER_PERMISSION:
            return user_id
        
        return -1  # No access
