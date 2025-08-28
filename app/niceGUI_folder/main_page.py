from app.niceGUI_folder.header import get_header
from nicegui import ui
from app.database_folder.orm import AsyncOrm


async def main_page_render():
    len_owners, owners = await AsyncOrm.get_owner()
    len_cats, cats = await AsyncOrm.get_cat()
    # Header
    get_header('Cat Database Management System')

    with ui.column().classes('q-pa-md'):
        ui.label('Welcome to Cat Database Management System').classes('text-h4 q-mb-lg')
        with ui.row().classes('q-gutter-md'):
            with ui.card().classes('q-pa-md'):
                ui.label('🐱 Total Cats').classes('text-h6')
                ui.label(len_cats).classes('text-h4 text-blue')

            with ui.card().classes('q-pa-md'):
                ui.label('👤 Total Owners').classes('text-h6')
                ui.label(len_owners).classes('text-h4 text-green')

            with ui.card().classes('q-pa-md'):
                ui.label('📊 Database Status').classes('text-h6')
                ui.label('Connected').classes('text-h4 text-positive')
