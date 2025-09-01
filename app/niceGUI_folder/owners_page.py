from app.niceGUI_folder.header import get_header
from nicegui import ui
from app.database_folder.orm import AsyncOrm


columns = [
    {'name': 'id',         'label': 'ID',         'field': 'id',         'align': 'left'},
    {'name': 'firstname',  'label': 'First Name', 'field': 'firstname',  'align': 'left'},
    {'name': 'surname',    'label': 'Surname',    'field': 'surname',    'align': 'left'},
    {'name': 'email',      'label': 'Email',      'field': 'email',      'align': 'left'},
    {'name': 'phone',      'label': 'Phone',      'field': 'phone',      'align': 'left'},
    {'name': 'city',       'label': 'City',       'field': 'city',       'align': 'left'},
    {'name': 'permission', 'label': 'Permission', 'field': 'permission', 'align': 'left'},
]


def owner_to_row(o):
    if isinstance(o, dict):
        return {
            'id': o.get('owner_id'),
            'firstname': o.get('owner_firstname'),
            'surname': o.get('owner_surname'),
            'email': o.get('owner_email'),
            'phone': o.get('owner_phone'),
            'city': o.get('owner_city'),
            'permission': o.get('owner_permission'),
        }
    return {
        'id': getattr(o, 'owner_id', None),
        'firstname': getattr(o, 'owner_firstname', None),
        'surname': getattr(o, 'owner_surname', None),
        'email': getattr(o, 'owner_email', None),
        'phone': getattr(o, 'owner_phone', None),
        'city': getattr(o, 'owner_city', None),
        'permission': getattr(o, 'owner_permission', None),
    }


@ui.page('/owners')
async def owners_page_render():
    len_owners, owners = await AsyncOrm.get_owner()
    get_header('👤 Owners')
    rows = [owner_to_row(o) for o in (owners if isinstance(owners, list) else [owners])]
    ui.table(columns=columns, rows=rows, row_key='id').classes('q-pa-md')

    with ui.row().classes('q-pa-md'):
        ui.button('Add Owner', on_click=lambda: ui.navigate.to('/add_owner')).classes('q-mr-sm')
