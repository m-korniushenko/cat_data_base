"""
Authentication middleware for protecting routes
"""
from nicegui import ui
from app.niceGUI_folder.auth_service import AuthService
from app.niceGUI_folder.session_manager import SessionManager


def require_auth(required_permission: int = 1):
    """Decorator to require authentication for a page"""
    def decorator(page_func):
        async def wrapper(*args, **kwargs):
            # Check if user is authenticated
            if not SessionManager.is_authenticated():
                ui.notify('Please login to access this page', type='negative', position='top')
                ui.navigate.to('/login')
                return
            
            # Get current user data
            user_data = SessionManager.get_current_user()
            session_id = SessionManager.get_session_id()
            
            if not user_data:
                ui.notify('Session expired. Please login again', type='negative', position='top')
                SessionManager.clear_session()
                ui.navigate.to('/login')
                return
            
            # Check permission
            if not AuthService.has_permission(user_data, required_permission):
                ui.notify('You do not have permission to access this page', type='negative', position='top')
                ui.navigate.to('/dashboard')
                return
            
            # Add user data to kwargs for use in page
            kwargs['current_user'] = user_data
            kwargs['session_id'] = session_id
            
            # Call original page function
            return await page_func(*args, **kwargs)
        
        return wrapper
    return decorator


def get_current_user_from_session() -> dict:
    """Get current user data from session (synchronous version)"""
    # This is a simplified version for header display
    # Real authentication is handled in page decorators
    return None


def logout_user():
    """Logout current user"""
    try:
        # Clear session from SessionManager
        SessionManager.clear_session()
        
        # Clear session from browser
        ui.run_javascript('localStorage.removeItem("session_id")')
        
        ui.notify('Logged out successfully', type='positive', position='top')
        ui.navigate.to('/login')
    except Exception as e:
        print(f"Error during logout: {e}")
        ui.navigate.to('/login')
