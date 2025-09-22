"""
Authentication check page - redirects to login if not authenticated
"""
from nicegui import ui
from fastapi import Request
from app.niceGUI_folder.session_manager import SessionManager


def auth_check_page_render(request: Request):
    """Check authentication and redirect accordingly"""
    ui.page_title('Authentication Check - Cat Database')
    
    # Check if user is authenticated
    session_id = request.cookies.get("session_id")
    if session_id and SessionManager.is_authenticated(session_id):
        # User is authenticated, redirect to dashboard
        ui.navigate.to('/dashboard')
    else:
        # User is not authenticated, redirect to login
        ui.navigate.to('/login')
