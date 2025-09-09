"""
Login page for user authentication
"""
from nicegui import ui
from app.niceGUI_folder.auth_service import AuthService
from app.niceGUI_folder.session_manager import SessionManager


def login_page_render():
    """Render login page"""
    ui.page_title('Login - Cat Database')
    
    # Center the login form
    with ui.column().classes('w-full h-screen flex items-center justify-center bg-gray-100'):
        with ui.card().classes('w-full max-w-md p-8 shadow-lg'):
            ui.label('🐱 Cat Database Login').classes('text-h4 text-center mb-6 text-blue-600')
            
            # Login form
            email_input = ui.input('Email', placeholder='Enter your email').props('outlined dense').classes('w-full mb-4')
            password_input = ui.input('Password', placeholder='Enter your password').props('outlined dense type=password').classes('w-full mb-6')
            
            # Login button
            async def handle_login():
                email = email_input.value.strip()
                password = password_input.value.strip()
                
                if not email or not password:
                    ui.notify('Please enter both email and password', type='negative', position='top')
                    return
                
                try:
                    # Authenticate user
                    user_data = await AuthService.authenticate_user(email, password)
                    
                    if user_data:
                        # Create session
                        session_id = AuthService.create_session(user_data)
                        
                        # Store session in SessionManager
                        SessionManager.set_current_user(user_data, session_id)
                        
                        # Store session in browser (using localStorage)
                        ui.run_javascript(f'localStorage.setItem("session_id", "{session_id}")')
                        
                        # Show success message
                        ui.notify(f'Welcome, {user_data["owner_firstname"]}!', type='positive', position='top')
                        
                        # Redirect to dashboard
                        ui.navigate.to('/dashboard')
                    else:
                        ui.notify('Invalid email or password', type='negative', position='top')
                        
                except Exception as e:
                    ui.notify(f'Login error: {str(e)}', type='negative', position='top')
            
            ui.button('Login', on_click=handle_login, color='primary').classes('w-full mb-4')
            
            # Info about permissions
            with ui.expansion('Permission Levels', icon='info').classes('w-full'):
                ui.label('• Admin (Permission 1): Full access to all features')
                ui.label('• Owner (Permission 2): View own cats only, download PDFs')
                ui.label('• Others: No access')
            
            # Footer
            ui.separator().classes('my-4')
            ui.label('Cat Database Management System').classes('text-caption text-center text-gray-500')
