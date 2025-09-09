from datetime import date, datetime
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.auth_middleware import require_auth
from app.niceGUI_folder.auth_service import AuthService
from nicegui import ui
from app.database_folder.orm import AsyncOrm

cats_column = [
    {'name': 'id',         'label': 'ID',         'field': 'id',         'align': 'left'},
    {'name': 'firstname',  'label': 'First Name', 'field': 'firstname',  'align': 'left'},
    {'name': 'surname',    'label': 'Surname',    'field': 'surname',    'align': 'left'},
    {'name': 'gender',     'label': 'Gender',     'field': 'gender',     'align': 'left'},
    {'name': 'birthday',   'label': 'Birthday',   'field': 'birthday',   'align': 'left'},
    {'name': 'microchip',  'label': 'Microchip',  'field': 'microchip',  'align': 'left'},
    {'name': 'breed',      'label': 'Breed',      'field': 'breed',      'align': 'left'},
    {'name': 'colour',     'label': 'Colour',     'field': 'colour',     'align': 'left'},
    {'name': 'litter',     'label': 'Litter',     'field': 'litter',     'align': 'left'},
    {'name': 'haritage_number', 'label': 'Haritage Number', 'field': 'haritage_number', 'align': 'left'},
    {'name': 'owner_firstname', 'label': 'Owner First Name', 'field': 'owner_firstname', 'align': 'left'},
    {'name': 'owner_surname',   'label': 'Owner Surname',   'field': 'owner_surname',   'align': 'left'},
    {'name': 'owner_email',      'label': 'Owner Mail',      'field': 'owner_email',      'align': 'left'},
    {'name': 'breed_firstname', 'label': 'Breed First Name', 'field': 'breed_firstname', 'align': 'left'},
    {'name': 'breed_surname',   'label': 'Breed Surname',   'field': 'breed_surname',   'align': 'left'},
    {'name': 'breed_email',     'label': 'Breed Email',     'field': 'breed_email',     'align': 'left'},
    {'name': 'dam',          'label': 'Dam',          'field': 'dam',          'align': 'left'},
    {'name': 'sire',         'label': 'Sire',         'field': 'sire',         'align': 'left'},
    {'name': 'actions',    'label': 'Actions',    'field': 'actions',    'align': 'center'},
]


def get_edit_button_vue(current_user):
    # Check if user can edit cats
    can_edit = current_user and current_user.get('owner_permission') == 1  # Only admins can edit
    
    if can_edit:
        return r'''
          <q-tr :props="props">
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
              <template v-if="col.name === 'actions'">
                <q-btn size="sm" color="primary" flat
                       :href="'/cat_profile/' + props.row.id"
                       label="View" class="q-mr-xs" />
                <q-btn size="sm" color="secondary" flat
                       :href="'/edit_cat/' + props.row.id"
                       label="Edit" />
              </template>
              <template v-else-if="col.name === 'firstname'">
                <q-btn flat no-caps color="primary"
                       :href="'/cat_profile/' + props.row.id"
                       :label="col.value" />
              </template>
              <template v-else>
                {{ col.value }}
              </template>
            </q-td>
          </q-tr>
        '''
    else:
        # Owners can only view
        return r'''
          <q-tr :props="props">
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
              <template v-if="col.name === 'actions'">
                <q-btn size="sm" color="primary" flat
                       :href="'/cat_profile/' + props.row.id"
                       label="View" />
              </template>
              <template v-else-if="col.name === 'firstname'">
                <q-btn flat no-caps color="primary"
                       :href="'/cat_profile/' + props.row.id"
                       :label="col.value" />
              </template>
              <template v-else>
                {{ col.value }}
              </template>
            </q-td>
          </q-tr>
        '''


async def get_cats_rows(cats_rows):
    safe_rows = []
    for r in cats_rows:
        row = dict(r)
        b = row.get('birthday')
        if isinstance(b, (date, datetime)):
            row['birthday'] = b.isoformat()
        row.setdefault('actions', '')
        safe_rows.append(row)
    return safe_rows


@require_auth(required_permission=2)  # Require at least owner permission
async def cats_page_render(current_user=None, session_id=None):
    ui.label('Cats Page')
    get_header('🐱 Cats')
    
    # Filter cats based on user permission
    owner_filter = AuthService.get_user_cats_filter(current_user)
    _, cats_rows = await AsyncOrm.get_cat_info()
    
    # Apply filter if needed
    if owner_filter is not None:
        if owner_filter == -1:  # No access
            cats_rows = []
        else:
            cats_rows = [cat for cat in cats_rows if cat.get('owner_id') == owner_filter]
    
    safe_rows = await get_cats_rows(cats_rows)
    
    search_bar = ui.input(label='Search').props('outlined dense').classes('w-full')
    
    # Create table container
    table_container = ui.column()
    
    async def update_table(search_value):
        print(f"Updating table with search: '{search_value}'")
        _, cats_rows = await AsyncOrm.get_cat_info_like(search_value)
        print(f"Found {len(cats_rows)} cats")
        safe_rows = await get_cats_rows(cats_rows)
        print(f"Safe rows: {len(safe_rows)}")
        
        # Clear and recreate table
        table_container.clear()
        with table_container:
            table = ui.table(columns=cats_column, rows=safe_rows, row_key='id').classes('q-pa-md')
            table.add_slot('body', get_edit_button_vue(current_user))
    
    # Create initial table
    await update_table('')
    
    # Set up search
    search_bar.on_value_change(lambda e: update_table(e.value))
    
    # Add Cat button only for admins
    if current_user and current_user.get('owner_permission') == 1:
        with ui.row().classes('q-pa-md'):
            ui.button('Add Cat', on_click=lambda: ui.navigate.to('/add_cat')).classes('q-mr-sm')
