"""
Authentication middleware for protecting routes (cookie-based)
"""
from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui

from app.niceGUI_folder.auth_service import AuthService
from app.niceGUI_folder.session_manager import SessionManager


def require_auth(required_permission: int = 1):
    """Decorator to require authentication for a page (cookie-based approach)"""
    def decorator(page_func):
        @wraps(page_func)
        async def wrapper(request: Request, *args, **kwargs):
            # Достаём session_id из cookie
            session_id = request.cookies.get("session_id")
            if not session_id or not SessionManager.is_authenticated(session_id):
                ui.notify('Please login to access this page', type='negative', position='top')
                ui.navigate.to('/login')
                return

            # Получаем данные пользователя
            user_data = SessionManager.get_current_user(session_id)
            if not user_data:
                ui.notify('Session expired. Please login again', type='negative', position='top')
                SessionManager.clear_session(session_id)
                ui.navigate.to('/login')
                return

            # Проверяем права доступа
            if not AuthService.has_permission(user_data, required_permission):
                ui.notify('You do not have permission to access this page', type='negative', position='top')
                ui.navigate.to('/dashboard')
                return

            # Передаём user_data и session_id в аргументы страницы
            kwargs['current_user'] = user_data
            kwargs['session_id'] = session_id

            # Запускаем оригинальную функцию страницы
            return await page_func(request, *args, **kwargs)

        return wrapper
    return decorator


def get_current_user_from_session(request: Request) -> dict | None:
    """Get current user data from session (cookie-based)"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    return SessionManager.get_current_user(session_id)


def logout_user(request: Request):
    """Logout current user (cookie-based)"""
    session_id = request.cookies.get("session_id")
    if session_id:
        SessionManager.clear_session(session_id)

    response = RedirectResponse(url='/login', status_code=303)
    response.delete_cookie("session_id")

    ui.notify('Logged out successfully', type='positive', position='top')
    return response
