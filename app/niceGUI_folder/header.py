from nicegui import ui
from fastapi import Request
from app.niceGUI_folder.session_manager import SessionManager


def get_header(label_text: str, request: Request):
    with ui.header().classes('bg-blue-500 text-white'):
        ui.label(label_text).classes('text-h6 q-ml-md')
        
        # Get current user info from session
        session_id = request.cookies.get("session_id")
        current_user = None
        if session_id:
            current_user = SessionManager.get_current_user(session_id)
        
        with ui.row().classes('q-ml-auto q-mr-md items-center'):
            # Navigation buttons (only for authenticated users)
            if current_user:
                ui.button('Cats', on_click=lambda: ui.navigate.to('/cats')).classes('q-mr-sm')
                ui.button('Owners', on_click=lambda: ui.navigate.to('/owners')).classes('q-mr-sm')
                ui.button('Breeds', on_click=lambda: ui.navigate.to('/breeds')).classes('q-mr-sm')
                ui.button('Studbook', on_click=lambda: ui.navigate.to('/studbook')).classes('q-mr-sm')
                ui.button('History', on_click=lambda: ui.navigate.to('/history')).classes('q-mr-sm')
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes('q-mr-sm')
                
                # User info and logout
                user_name = f"{current_user.get('owner_firstname', '')} {current_user.get('owner_surname', '')}"
                permission_text = "Admin" if current_user.get('owner_permission') == 1 else "Owner"
                
                ui.label(f"👤 {user_name} ({permission_text})").classes('q-mr-sm text-sm')
                
                # Logout button with POST form
                with ui.html(f'''
                    <form action="/logout" method="post" style="display: inline;">
                        <button type="submit" 
                                class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-200">
                            Logout
                        </button>
                    </form>
                ''').classes('q-mr-sm'):
                    pass
            else:
                # Login button for unauthenticated users
                ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes('q-mr-sm')