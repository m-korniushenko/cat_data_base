from app.niceGUI_folder.header import get_header
from nicegui import ui
from app.database_folder.orm import AsyncOrm


columns = [
    {'name': 'id',         'label': 'ID',         'field': 'id',         'align': 'left'},
    {'name': 'firstname',  'label': 'First Name', 'field': 'firstname',  'align': 'left'},
    {'name': 'surname',    'label': 'Surname',    'field': 'surname',    'align': 'left'},
    {'name': 'email',      'label': 'Email',      'field': 'email',      'align': 'left'},
    {'name': 'phone',      'label': 'Phone',      'field': 'phone',      'align': 'left'},
    {'name': 'gender',     'label': 'Gender',     'field': 'gender',     'align': 'left'},
    {'name': 'birthday',   'label': 'Birthday',   'field': 'birthday',   'align': 'left'},
    {'name': 'address',    'label': 'Address',    'field': 'address',    'align': 'left'},
    {'name': 'city',       'label': 'City',       'field': 'city',       'align': 'left'},
    {'name': 'country',    'label': 'Country',    'field': 'country',    'align': 'left'},
    {'name': 'zip',        'label': 'ZIP',        'field': 'zip',        'align': 'left'},
    {'name': 'description', 'label': 'Description', 'field': 'description', 'align': 'left'},
]


def breed_to_row(b):
    if isinstance(b, dict):
        return {
            'id': b.get('breed_id'),
            'firstname': b.get('breed_firstname'),
            'surname': b.get('breed_surname'),
            'email': b.get('breed_email'),
            'phone': b.get('breed_phone'),
            'gender': b.get('breed_gender'),
            'birthday': b.get('breed_birthday'),
            'address': b.get('breed_address'),
            'city': b.get('breed_city'),
            'country': b.get('breed_country'),
            'zip': b.get('breed_zip'),
            'description': b.get('breed_description'),
        }
    return {
        'id': getattr(b, 'breed_id', None),
        'firstname': getattr(b, 'breed_firstname', None),
        'surname': getattr(b, 'breed_surname', None),
        'email': getattr(b, 'breed_email', None),
        'phone': getattr(b, 'breed_phone', None),
        'gender': getattr(b, 'breed_gender', None),
        'birthday': getattr(b, 'breed_birthday', None),
        'address': getattr(b, 'breed_address', None),
        'city': getattr(b, 'breed_city', None),
        'country': getattr(b, 'breed_country', None),
        'zip': getattr(b, 'breed_zip', None),
        'description': getattr(b, 'breed_description', None),
    }


@ui.page('/breeds')
async def breeds_page_render():
    len_breeds, breeds = await AsyncOrm.get_breed()
    get_header('🐱 Breeds')
    rows = [breed_to_row(b) for b in (breeds if isinstance(breeds, list) else [breeds])]
    ui.table(columns=columns, rows=rows, row_key='id').classes('q-pa-md')

    with ui.row().classes('q-pa-md'):
        ui.button('Add Breed', on_click=lambda: ui.navigate.to('/add_breed')).classes('q-mr-sm')
