from datetime import datetime
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.auth_middleware import require_auth
from app.niceGUI_folder.auth_service import AuthService
from nicegui import ui
from app.database_folder.orm import AsyncOrm


studbook_table_columns = [
    {'name': 'lfd_nr', 'label': 'Lfd Nr', 'field': 'lfd_nr', 'align': 'center', 'sortable': True},
    {'name': 'datum', 'label': 'Datum', 'field': 'datum', 'align': 'center', 'sortable': True},
    {'name': 'tiername', 'label': 'Tiername', 'field': 'tiername', 'align': 'left', 'sortable': True},
    {'name': 'zb_nummer', 'label': 'ZB-Nummer', 'field': 'zb_nummer', 'align': 'center', 'sortable': True},
    {'name': 'microchip', 'label': 'Microchip', 'field': 'microchip', 'align': 'center', 'sortable': True},
    {'name': 'geburtsdatum', 'label': 'Geburtsdatum', 'field': 'geburtsdatum', 'align': 'center', 'sortable': True},
    {'name': 'gender', 'label': 'w/m', 'field': 'gender', 'align': 'center', 'sortable': True},
    {'name': 'rasse', 'label': 'Rasse', 'field': 'rasse', 'align': 'left', 'sortable': True},
    {'name': 'ausgabe', 'label': 'Ausgabe', 'field': 'ausgabe', 'align': 'left', 'sortable': True},
    {'name': 'besitzer', 'label': 'Besitzer', 'field': 'besitzer', 'align': 'left', 'sortable': True},
    {'name': 'kommentar', 'label': 'Kommentar', 'field': 'kommentar', 'align': 'left', 'sortable': True},
    {'name': 'wcf_sticker', 'label': 'WCF Sticker', 'field': 'wcf_sticker', 'align': 'center', 'sortable': True},
]


@require_auth(required_permission=2)
async def studbook_page_render(current_user=None, session_id=None):
    """Render the Studbook page with grouped structure by breeder and litter"""

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

    def group_cats_by_breeder_and_litter(filtered_cats):
        """Group cats by breeder and then by litter"""
        grouped = {}

        for cat in filtered_cats:
            breeder_name = f"{cat.get('breed_firstname', '')} {cat.get('breed_surname', '')}".strip()
            if not breeder_name:
                breeder_name = "Неизвестный заводчик"

            if breeder_name not in grouped:
                grouped[breeder_name] = {
                    "Zuchttiere": [],
                    "litters": {}
                }

            # Check if it's a breeding animal
            if cat.get('breeding_animal'):
                grouped[breeder_name]["Zuchttiere"].append(cat)
            else:
                # Group by litter
                litter = cat.get('litter', 'Без помёта')
                if litter not in grouped[breeder_name]["litters"]:
                    grouped[breeder_name]["litters"][litter] = []
                grouped[breeder_name]["litters"][litter].append(cat)

        return grouped

    def create_studbook_row(cat, lfd_nr):
        """Create a row for the studbook table"""
        # Format cat name
        tiername = f"{cat.get('firstname', '')} {cat.get('surname', '')}".strip()

        # Format registration numbers
        reg_numbers = []
        if cat.get('haritage_number'):
            reg_numbers.append(cat.get('haritage_number'))
        if cat.get('haritage_number_2'):
            reg_numbers.append(cat.get('haritage_number_2'))
        zb_nummer = ', '.join(reg_numbers) if reg_numbers else ''

        # Format birthday
        geburtsdatum = cat.get('birthday').strftime('%d.%m.%Y') if cat.get('birthday') else ''

        # Format gender (w/m)
        gender = 'w' if cat.get('gender') == 'Female' else 'm' if cat.get('gender') == 'Male' else ''

        # Format breed name
        rasse = f"{cat.get('breed_firstname', '')} {cat.get('breed_surname', '')}".strip()

        # Determine document type
        ausgabe = 'Stammbaum' if cat.get('breeding_animal') else 'Abschrift'

        # Format owner name
        besitzer = f"{cat.get('owner_firstname', '')} {cat.get('owner_surname', '')}".strip()

        # Get comments
        kommentar = cat.get('notes', '') or ''

        # WCF Sticker (placeholder for future implementation)
        wcf_sticker = '✓' if cat.get('wcf_sticker') else ''

        return {
            'lfd_nr': lfd_nr,
            'datum': datetime.now().strftime('%d.%m.%Y'),  # Current date as registration date
            'tiername': tiername or 'Не указано',
            'zb_nummer': zb_nummer or 'Не указан',
            'microchip': cat.get('microchip', '') or 'Не указан',
            'geburtsdatum': geburtsdatum or 'Не указана',
            'gender': gender,
            'rasse': rasse or 'Не указана',
            'ausgabe': ausgabe,
            'besitzer': besitzer or 'Не указан',
            'kommentar': kommentar,
            'wcf_sticker': wcf_sticker,
            'raw_data': cat  # Store full data for detail view
        }

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
                    ui.label(f"**Тип документа:** {'Stammbaum' if cat.get('breeding_animal') else 'Abschrift'}")
                    ui.label(f"**WCF Sticker:** {'✓' if cat.get('wcf_sticker') else 'Нет'}")

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
                    ui.markdown("### 📝 Комментарии")
                    ui.label(f"**Заметки:** {cat.get('notes', '')}")

            # Parents Information
            if cat.get('dam') or cat.get('sire'):
                with ui.card():
                    ui.markdown("### 👨‍👩‍👧‍👦 Родители")
                    ui.label(f"**Мать:** {cat.get('dam', 'Не указана')}")
                    ui.label(f"**Отец:** {cat.get('sire', 'Не указан')}")

            ui.button('Закрыть', on_click=dialog.close).props('color=primary')

        dialog.open()

    async def render_studbook_structure():
        """Render the grouped studbook structure"""
        filtered_cats = apply_filters()
        grouped_data = group_cats_by_breeder_and_litter(filtered_cats)

        lfd_nr_counter = 1

        for breeder_name, breeder_data in grouped_data.items():
            # Breeder expansion
            with ui.expansion(breeder_name, icon='person').classes('w-full'):

                # Zuchttiere section
                if breeder_data["Zuchttiere"]:
                    with ui.expansion("🐾 Zuchttiere", icon='pets').classes('w-full'):
                        table = ui.table(
                            columns=studbook_table_columns,
                            rows=[create_studbook_row(cat, lfd_nr_counter + i)
                                  for i, cat in enumerate(breeder_data["Zuchttiere"])]
                        ).classes('w-full')
                        lfd_nr_counter += len(breeder_data["Zuchttiere"])

                        # Set up table row click handler
                        table.on('rowClick', lambda e: show_cat_details(e.args[1]))

                # Litters sections
                for litter_name, litter_cats in breeder_data["litters"].items():
                    with ui.expansion(f"👶 {litter_name}", icon='child_care').classes('w-full'):
                        table = ui.table(
                            columns=studbook_table_columns,
                            rows=[create_studbook_row(cat, lfd_nr_counter + i) for i, cat in enumerate(litter_cats)]
                        ).classes('w-full')
                        lfd_nr_counter += len(litter_cats)

                        # Set up table row click handler
                        table.on('rowClick', lambda e: show_cat_details(e.args[1]))

    async def clear_all_filters():
        """Clear all filter inputs"""
        search_input.value = ''
        breeder_filter.value = None
        owner_filter_select.value = None
        ems_color_filter.value = None
        status_filter.value = None
        birthday_from.value = ''
        birthday_to.value = ''
        ui.clear()
        await render_page_content()

    async def render_page_content():
        """Render the main page content"""
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

        # Results counter
        filtered_cats = apply_filters()
        ui.label(f'Найдено записей: {len(filtered_cats)}')

        # Studbook structure
        await render_studbook_structure()

    # Set up event handlers
    search_input.on_value_change(lambda: ui.clear() or render_page_content())
    breeder_filter.on_value_change(lambda: ui.clear() or render_page_content())
    owner_filter_select.on_value_change(lambda: ui.clear() or render_page_content())
    ems_color_filter.on_value_change(lambda: ui.clear() or render_page_content())
    status_filter.on_value_change(lambda: ui.clear() or render_page_content())
    birthday_from.on_value_change(lambda: ui.clear() or render_page_content())
    birthday_to.on_value_change(lambda: ui.clear() or render_page_content())

    # Initial render
    await render_page_content()
