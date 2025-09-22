"""
Login page for user authentication
"""
from nicegui import ui
from fastapi import Request


def login_page_render(request: Request):
    """Render login page with HTML form"""
    ui.page_title('Login - Cat Database')
    
    # Check for error messages in URL parameters
    error_message = ""
    if hasattr(request, 'query_params'):
        if request.query_params.get('error') == 'invalid_credentials':
            error_message = "Invalid email or password"
        elif request.query_params.get('error') == 'server_error':
            error_message = "Server error. Please try again."
    
    # Center the login form
    with ui.column().classes('w-full h-screen flex items-center justify-center bg-gray-100'):
        with ui.card().classes('w-full max-w-md p-8 shadow-lg'):
            ui.label('🐱 Cat Database Login').classes('text-h4 text-center mb-6 text-blue-600')
            
            # Show error message if any
            if error_message:
                ui.label(error_message).classes('text-red-500 text-center mb-4')
            
            # HTML form with POST method
            with ui.html('''
                <form action="/login" method="post" class="w-full">
                    <div class="mb-4">
                        <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                        <input type="email" id="email" name="email" required 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                               placeholder="Enter your email">
                    </div>
                    <div class="mb-6">
                        <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                        <input type="password" id="password" name="password" required 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                               placeholder="Enter your password">
                    </div>
                    <button type="submit" 
                            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200">
                        Login
                    </button>
                </form>
            ''').classes('w-full mb-4'):
                pass
            
            # Info about permissions
            with ui.expansion('Permission Levels', icon='info').classes('w-full'):
                ui.label('• Admin (Permission 1): Full access to all features')
                ui.label('• Owner (Permission 2): View own cats only, download PDFs')
                ui.label('• Others: No access')
            
            # Footer
            ui.separator().classes('my-4')
            ui.label('Cat Database Management System').classes('text-caption text-center text-gray-500')
