from nicegui import ui
from app.niceGUI_folder.auth_middleware import logout_user
from app.niceGUI_folder.session_manager import SessionManager


def get_header(label_text: str):
    with ui.header().classes('bg-blue-500 text-white'):
        ui.label(label_text).classes('text-h6 q-ml-md')
        
        # Get current user info
        current_user = SessionManager.get_current_user()
        
        with ui.row().classes('q-ml-auto q-mr-md items-center'):
            # Navigation buttons (only for authenticated users)
            if current_user:
                ui.button('Cats', on_click=lambda: ui.navigate.to('/cats')).classes('q-mr-sm')
                ui.button('Owners', on_click=lambda: ui.navigate.to('/owners')).classes('q-mr-sm')
                ui.button('Breeds', on_click=lambda: ui.navigate.to('/breeds')).classes('q-mr-sm')
                ui.button('History', on_click=lambda: ui.navigate.to('/history')).classes('q-mr-sm')
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes('q-mr-sm')
                
                # User info and logout
                user_name = f"{current_user.get('owner_firstname', '')} {current_user.get('owner_surname', '')}"
                permission_text = "Admin" if current_user.get('owner_permission') == 1 else "Owner"
                
                ui.label(f"👤 {user_name} ({permission_text})").classes('q-mr-sm text-sm')
                ui.button('Logout', on_click=logout_user, color='red').classes('q-mr-sm')
            else:
                # Login button for unauthenticated users
                ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes('q-mr-sm')