from datetime import date, datetime
from app.niceGUI_folder.header import get_header
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
    {'name': 'ifc',        'label': 'IFC',        'field': 'ifc',        'align': 'left'},
    {'name': 'owner_firstname', 'label': 'Owner First Name', 'field': 'owner_firstname', 'align': 'left'},
    {'name': 'owner_surname',   'label': 'Owner Surname',   'field': 'owner_surname',   'align': 'left'},
    {'name': 'owner_mail',      'label': 'Owner Mail',      'field': 'owner_mail',      'align': 'left'},
    {'name': 'actions',    'label': 'Actions',    'field': 'actions',    'align': 'center'},
]


def get_edit_button_vue():
    return r'''
      <q-tr :props="props">
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
          <template v-if="col.name === 'actions'">
            <q-btn size="sm" color="primary" flat
                   :href="'/edit_cat/' + props.row.id"
                   label="Edit" />
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


async def update_table(search_value, table: ui.table):
    _, cats_rows = await AsyncOrm.get_cat_info_like(search_value)
    safe_rows = await get_cats_rows(cats_rows)
    table.rows = safe_rows
    table.update()


async def cats_page_render():
    ui.label('Cats Page')
    get_header('🐱 Cats')
    _, cats_rows = await AsyncOrm.get_cat_info()
    safe_rows = await get_cats_rows(cats_rows)
    search_bar = ui.input(label='Search').props('outlined dense').classes('w-full')
    table = ui.table(columns=cats_column, rows=safe_rows, row_key='id').classes('q-pa-md')
    table.add_slot('body', get_edit_button_vue())
    search_bar.on_value_change(lambda e: update_table(e.value, table))
    ui.button('Add Cat', on_click=lambda: ui.navigate.to('/add_cat')).classes('q-mr-sm')
