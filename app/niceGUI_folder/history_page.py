"""
History page for displaying user actions
"""
from nicegui import ui
from app.niceGUI_folder.header import get_header


async def history_page_render():
    """Render the history page"""
    get_header('History Page')
    
    with ui.column().classes('w-full p-4'):
        ui.label('User Action History').classes('text-h4 q-mb-md')
        
        # History table
        columns = [
            {'name': 'datetime', 'label': 'Date & Time', 'field': 'datetime', 'sortable': True, 'align': 'left'},
            {'name': 'user', 'label': 'User', 'field': 'user', 'sortable': True, 'align': 'left'},
            {'name': 'action', 'label': 'Action', 'field': 'action', 'sortable': True, 'align': 'left'},
        ]
        
        rows = [
            # Example row - will be replaced with real data in the future
            {
                'datetime': '2025-09-12 12:00:00',
                'user': 'Admin',
                'action': 'System initialized'
            }
        ]
        
        ui.table(columns=columns, rows=rows, row_key='datetime').classes('w-full')
