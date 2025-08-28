from app.niceGUI_folder.header import get_header
from nicegui import ui
from app.database_folder.orm import AsyncOrm


columns = [
    {'name': 'id',         'label': 'ID',         'field': 'id',         'align': 'left'},
    {'name': 'firstname',  'label': 'First Name', 'field': 'firstname',  'align': 'left'},
    {'name': 'surname',    'label': 'Surname',    'field': 'surname',    'align': 'left'},
    {'name': 'mail',       'label': 'Mail',       'field': 'mail',       'align': 'left'},
    {'name': 'permission', 'label': 'Permission', 'field': 'permission', 'align': 'left'},
]


def owner_to_row(o):
    return {
        'id': o.owner_id,
        'firstname': o.owner_firstname,
        'surname': o.owner_surname,
        'mail': o.owner_mail,
        'permission': o.owner_permission,
    }


@ui.page('/owners')
async def owners_page_render():
    len_owners, owners = await AsyncOrm.get_owner()
    get_header('👤 Owners')
    rows = [owner_to_row(o) for o in (owners if isinstance(owners, list) else [owners])]
    ui.table(columns=columns, rows=rows, row_key='id').classes('q-pa-md')