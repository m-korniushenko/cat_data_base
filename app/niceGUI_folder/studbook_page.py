from datetime import datetime
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.auth_middleware import require_auth
from app.niceGUI_folder.auth_service import AuthService
from nicegui import ui
from app.database_folder.orm import AsyncOrm


studbook_columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left', 'sortable': True},
    {'name': 'birthday', 'label': 'Дата рождения', 'field': 'birthday', 'align': 'left', 'sortable': True},
    {'name': 'breeder', 'label': 'Заводчик', 'field': 'breeder', 'align': 'left', 'sortable': True},
    {'name': 'name', 'label': 'Имя кошки', 'field': 'name', 'align': 'left', 'sortable': True},
    {'name': 'registration', 'label': 'Регистрационный номер', 'field': 'registration', 'align': 'left', 'sortable': True},
    {'name': 'microchip', 'label': 'Микрочип', 'field': 'microchip', 'align': 'left', 'sortable': True},
    {'name': 'gender', 'label': 'Пол', 'field': 'gender', 'align': 'left', 'sortable': True},
    {'name': 'ems_color', 'label': 'EMS окрас', 'field': 'ems_color', 'align': 'left', 'sortable': True},
    {'name': 'record_type', 'label': 'Тип записи', 'field': 'record_type', 'align': 'left', 'sortable': True},
    {'name': 'owner', 'label': 'Владелец', 'field': 'owner', 'align': 'left', 'sortable': True},
    {'name': 'status', 'label': 'Статус', 'field': 'status', 'align': 'left', 'sortable': True},
    {'name': 'actions', 'label': 'Действия', 'field': 'actions', 'align': 'center'},
]


@require_auth(required_permission=2)
async def studbook_page_render(current_user=None, session_id=None):
    """Render the Studbook page"""
    
    # Load data for filters
    _, cats_data = await AsyncOrm.get_cat_info()
    _, owners_data = await AsyncOrm.get_owner()
    _, breeds_data = await AsyncOrm.get_breed()

    # Apply user permission filter
    owner_filter = AuthService.get_user_cats_filter(current_user)
    if owner_filter is not None:
        if owner_filter == -1:
            cats_data = []
        else:
            cats_data = [cat for cat in cats_data if cat.get('owner_id') == owner_filter]

    # Create filter options
    breeder_options = {
        breed['breed_id']: f"{breed['breed_firstname']} {breed['breed_surname']}"
        for breed in breeds_data
        if breed['breed_firstname'] and breed['breed_surname']
    }
    owner_options = {
        owner['owner_id']: f"{owner['owner_firstname']} {owner['owner_surname']}"
        for owner in owners_data
        if owner['owner_firstname'] and owner['owner_surname']
    }
    ems_color_options = list(set([cat.get('colour') for cat in cats_data if cat.get('colour')]))
    status_options = list(set([cat.get('status') for cat in cats_data if cat.get('status')]))
    
    # Filter variables
    search_input = ui.input('Поиск', placeholder='По имени, микрочипу, номеру ZB...').style('width: 300px')
    breeder_filter = ui.select(breeder_options, label='Заводчик', clearable=True).style('width: 200px')
    owner_filter_select = ui.select(owner_options, label='Владелец', clearable=True).style('width: 200px')
    ems_color_filter = ui.select(ems_color_options, label='EMS окрас', clearable=True).style('width: 150px')
    status_filter = ui.select(status_options, label='Статус', clearable=True).style('width: 150px')
    birthday_from = ui.input('Дата рождения от').style('width: 150px')
    birthday_to = ui.input('Дата рождения до').style('width: 150px')

    
    def apply_filters():
        """Apply all filters to the data"""
        if not cats_data:
            return []
            
        filtered_cats = cats_data.copy()
        
        # Search filter
        search_term = search_input.value.lower() if search_input.value else ''
        if search_term:
            filtered_cats = [
                cat for cat in filtered_cats
                if (search_term in str(cat.get('firstname', '') or '').lower() or
                    search_term in str(cat.get('surname', '') or '').lower() or
                    search_term in str(cat.get('callname', '') or '').lower() or
                    search_term in str(cat.get('microchip', '') or '').lower() or
                    search_term in str(cat.get('haritage_number', '') or '').lower() or
                    search_term in str(cat.get('haritage_number_2', '') or '').lower())
            ]
        
        # Breeder filter
        if breeder_filter.value:
            selected_breeder_name = breeder_filter.value
            selected_breeder_id = next((k for k, v in breeder_options.items() if v == selected_breeder_name), None)
            if selected_breeder_id:
                filtered_cats = [cat for cat in filtered_cats if cat.get('breed') == selected_breeder_id]
        
        # Owner filter
        if owner_filter_select.value:
            selected_owner_name = owner_filter_select.value
            selected_owner_id = next((k for k, v in owner_options.items() if v == selected_owner_name), None)
            if selected_owner_id:
                filtered_cats = [cat for cat in filtered_cats if cat.get('owner_id') == selected_owner_id]
        
        # EMS color filter
        if ems_color_filter.value:
            filtered_cats = [cat for cat in filtered_cats if cat.get('colour') == ems_color_filter.value]
        
        # Status filter
        if status_filter.value:
            filtered_cats = [cat for cat in filtered_cats if cat.get('status') == status_filter.value]
        
        # Birthday range filter
        if birthday_from.value:
            try:
                from_date = datetime.strptime(birthday_from.value, '%Y-%m-%d').date()
                filtered_cats = [cat for cat in filtered_cats
                                if cat.get('birthday') and cat.get('birthday') >= from_date]
            except ValueError:
                pass
        
        if birthday_to.value:
            try:
                to_date = datetime.strptime(birthday_to.value, '%Y-%m-%d').date()
                filtered_cats = [cat for cat in filtered_cats
                                if cat.get('birthday') and cat.get('birthday') <= to_date]
            except ValueError:
                pass
        
        return filtered_cats

    def clear_all_filters():
        """Clear all filter inputs"""
        search_input.value = ''
        breeder_filter.value = None
        owner_filter_select.value = None
        ems_color_filter.value = None
        status_filter.value = None
        birthday_from.value = ''
        birthday_to.value = ''
        update_table()

    # Table and results counter
    table = None
    results_label = None

    async def update_table():
        """Update the table with filtered data"""
        nonlocal table, results_label
        
        if not cats_data:
            return
            
        filtered_cats = apply_filters()
        
        # Create empty table if no data
        if not filtered_cats:
            if table:
                table.options['rowData'] = []
                table.update()
            else:
                table = ui.table(
                    columns=studbook_columns,
                    rows=[]
                ).classes('w-full').style('height: 600px')
            return
        
        # Prepare rows for display
        display_rows = []
        for i, cat in enumerate(filtered_cats):
            if not cat or 'id' not in cat:
                continue
            # Format breeder name
            breeder_name = f"{cat.get('breed_firstname', '')} {cat.get('breed_surname', '')}".strip()
            
            # Format cat name
            cat_name = f"{cat.get('firstname', '')} {cat.get('surname', '')}".strip()
            
            # Format registration numbers
            reg_numbers = []
            if cat.get('haritage_number'):
                reg_numbers.append(cat.get('haritage_number'))
            if cat.get('haritage_number_2'):
                reg_numbers.append(cat.get('haritage_number_2'))
            registration = ', '.join(reg_numbers) if reg_numbers else ''
            
            # Format birthday
            birthday_display = cat.get('birthday').isoformat() if cat.get('birthday') else ''
            
            # Determine record type
            record_type = 'Племенное животное' if cat.get('breeding_animal') else 'Обычная запись'
            
            # Format owner name
            owner_name = f"{cat.get('owner_firstname', '')} {cat.get('owner_surname', '')}".strip()
            
            # Ensure we have an id field
            cat_id = cat.get('id') or 0
            if not cat_id:
                cat_id = i
            
            row = {
                'id': cat_id,
                'birthday': birthday_display,
                'breeder': breeder_name or 'Не указан',
                'name': cat_name or 'Не указано',
                'registration': registration or 'Не указан',
                'microchip': cat.get('microchip', '') or 'Не указан',
                'gender': cat.get('gender', '') or 'Не указан',
                'ems_color': cat.get('colour', '') or 'Не указан',
                'record_type': record_type,
                'owner': owner_name or 'Не указан',
                'status': cat.get('status', '') or 'Не указан',
                'raw_data': cat  # Store full data for detail view
            }
            display_rows.append(row)

        # Update or create table
        if table:
            table.options['rowData'] = display_rows
            table.update()
        else:
            table = ui.table(
                columns=studbook_columns,
                rows=display_rows
            ).classes('w-full').style('height: 600px')
            
            # Set up table row click handler
            table.on('rowClick', lambda e: show_cat_details(e.args[1]))

        # Update results counter
        if results_label:
            results_label.text = f'Найдено записей: {len(display_rows)}'
        else:
            results_label = ui.label(f'Найдено записей: {len(display_rows)}')

    async def show_cat_details(cat_data):
        """Show detailed cat information in modal"""
        if not cat_data or 'raw_data' not in cat_data:
            return
            
        cat = cat_data['raw_data']
        
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
            ui.markdown(f"## 📋 Племенная книга - {cat.get('firstname', '')} {cat.get('surname', '')}")
            
            with ui.grid(columns=2):
                # Basic Information
                with ui.card():
                    ui.markdown("### 🐱 Основная информация")
                    ui.label(f"**Имя:** {cat.get('firstname', 'Не указано')} {cat.get('surname', '')}")
                    ui.label(f"**Кличка:** {cat.get('callname', 'Не указана')}")
                    ui.label(f"**Пол:** {cat.get('gender', 'Не указан')}")
                    ui.label(f"**Дата рождения:** {cat.get('birthday', 'Не указана')}")
                    ui.label(f"**Микрочип:** {cat.get('microchip', 'Не указан')}")
                    ui.label(f"**EMS окрас:** {cat.get('colour', 'Не указан')}")
                    ui.label(f"**Помёт:** {cat.get('litter', 'Не указан')}")
                
                # Registration Information
                with ui.card():
                    ui.markdown("### 📜 Регистрационная информация")
                    ui.label(f"**Регистрационный номер 1:** {cat.get('haritage_number', 'Не указан')}")
                    ui.label(f"**Регистрационный номер 2:** {cat.get('haritage_number_2', 'Не указан')}")
                    ui.label(f"**Племенное животное:** {'Да' if cat.get('breeding_animal') else 'Нет'}")
                    ui.label(f"**Статус:** {cat.get('status', 'Не указан')}")
                    ui.label(f"**Тип записи:** {'Племенная книга' if cat.get('breeding_animal') else 'Обычная запись'}")
                
                # Breeder Information
                with ui.card():
                    ui.markdown("### 👨‍🌾 Информация о заводчике")
                    ui.label(f"**Заводчик:** {cat.get('breed_firstname', '')} {cat.get('breed_surname', '')}")
                    ui.label(f"**Email:** {cat.get('breed_email', 'Не указан')}")
                    ui.label(f"**Телефон:** {cat.get('breed_phone', 'Не указан')}")
                    ui.label(f"**Страна:** {cat.get('breed_country', 'Не указана')}")
                    ui.label(f"**Город:** {cat.get('breed_city', 'Не указан')}")
                
                # Owner Information
                with ui.card():
                    ui.markdown("### 👤 Информация о владельце")
                    ui.label(f"**Владелец:** {cat.get('owner_firstname', '')} {cat.get('owner_surname', '')}")
                    ui.label(f"**Email:** {cat.get('owner_email', 'Не указан')}")
                    ui.label(f"**Страна:** {cat.get('owner_country', 'Не указана')}")
                    ui.label(f"**Город:** {cat.get('owner_city', 'Не указан')}")
            
            # Additional Information
            if cat.get('notes'):
                with ui.card():
                    ui.markdown("### 📝 Дополнительная информация")
                    ui.label(f"**Заметки:** {cat.get('notes', '')}")
            
            # Parents Information
            if cat.get('dam') or cat.get('sire'):
                with ui.card():
                    ui.markdown("### 👨‍👩‍👧‍👦 Родители")
                    ui.label(f"**Мать:** {cat.get('dam', 'Не указана')}")
                    ui.label(f"**Отец:** {cat.get('sire', 'Не указан')}")
            
            ui.button('Закрыть', on_click=dialog.close).props('color=primary')
        
        dialog.open()

    # Set up event handlers
    search_input.on_value_change(update_table)
    breeder_filter.on_value_change(update_table)
    owner_filter_select.on_value_change(update_table)
    ems_color_filter.on_value_change(update_table)
    status_filter.on_value_change(update_table)
    birthday_from.on_value_change(update_table)
    birthday_to.on_value_change(update_table)

    # Render page
    get_header("Studbook")
    
    ui.markdown("## 📚 Племенная книга (Studbook)")
    ui.markdown("Официальный реестр зарегистрированных кошек и их помётов")
    
    # Filters section
    with ui.card():
        ui.markdown("### 🔍 Фильтры и поиск")
        with ui.grid(columns=4):
            search_input
            breeder_filter
            owner_filter_select
            ems_color_filter
            status_filter
            birthday_from
            birthday_to
            ui.button('Очистить все фильтры', on_click=clear_all_filters).props('color=secondary')
    
    # Results counter and table
    results_label
    table
    
    # Initial table update
    await update_table()