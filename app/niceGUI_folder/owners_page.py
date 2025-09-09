from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.auth_middleware import require_auth
from nicegui import ui
from app.database_folder.orm import AsyncOrm


columns = [
    {'name': 'id',         'label': 'ID',         'field': 'id',         'align': 'left'},
    {'name': 'firstname',  'label': 'First Name', 'field': 'firstname',  'align': 'left'},
    {'name': 'surname',    'label': 'Surname',    'field': 'surname',    'align': 'left'},
    {'name': 'email',      'label': 'Email',      'field': 'email',      'align': 'left'},
    {'name': 'phone',      'label': 'Phone',      'field': 'phone',      'align': 'left'},
    {'name': 'address',    'label': 'Address',    'field': 'address',    'align': 'left'},
    {'name': 'city',       'label': 'City',       'field': 'city',       'align': 'left'},
    {'name': 'country',    'label': 'Country',    'field': 'country',    'align': 'left'},
    {'name': 'zip',        'label': 'ZIP',        'field': 'zip',        'align': 'left'},
    {'name': 'birthday',   'label': 'Birthday',   'field': 'birthday',   'align': 'left'},
    {'name': 'permission', 'label': 'Permission', 'field': 'permission', 'align': 'left'},
    {'name': 'actions',    'label': 'Actions',    'field': 'actions',    'align': 'center'},
]


def get_edit_button_vue():
    return r'''
      <q-tr :props="props">
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
          <template v-if="col.name === 'actions'">
            <q-btn size="sm" color="primary" flat
                   :href="'/edit_owner/' + props.row.id"
                   label="Edit" />
          </template>
          <template v-else>
            {{ col.value }}
          </template>
        </q-td>
      </q-tr>
    '''


def owner_to_row(o):
    if isinstance(o, dict):
        return {
            'id': o.get('owner_id'),
            'firstname': o.get('owner_firstname'),
            'surname': o.get('owner_surname'),
            'email': o.get('owner_email'),
            'phone': o.get('owner_phone'),
            'address': o.get('owner_address'),
            'city': o.get('owner_city'),
            'country': o.get('owner_country'),
            'zip': o.get('owner_zip'),
            'birthday': o.get('owner_birthday'),
            'permission': o.get('owner_permission'),
        }
    return {
        'id': getattr(o, 'owner_id', None),
        'firstname': getattr(o, 'owner_firstname', None),
        'surname': getattr(o, 'owner_surname', None),
        'email': getattr(o, 'owner_email', None),
        'phone': getattr(o, 'owner_phone', None),
        'address': getattr(o, 'owner_address', None),
        'city': getattr(o, 'owner_city', None),
        'country': getattr(o, 'owner_country', None),
        'zip': getattr(o, 'owner_zip', None),
        'birthday': getattr(o, 'owner_birthday', None),
        'permission': getattr(o, 'owner_permission', None),
    }


@ui.page('/owners')
@require_auth(required_permission=1)  # Only admins can view owners
async def owners_page_render(current_user=None, session_id=None):
    len_owners, owners = await AsyncOrm.get_owner()
    get_header('👤 Owners')
    
    # Convert owners to rows
    rows = [owner_to_row(o) for o in (owners if isinstance(owners, list) else [owners])]
    
    # Add actions field to each row
    for row in rows:
        row['actions'] = ''
    
    # Create table with Vue slot for custom buttons
    table = ui.table(columns=columns, rows=rows, row_key='id').classes('q-pa-md')
    table.add_slot('body', get_edit_button_vue())
    
    # Add action buttons below the table
    with ui.row().classes('q-pa-md'):
        ui.button('Add Owner', on_click=lambda: ui.navigate.to('/add_owner')).classes('q-mr-sm')
