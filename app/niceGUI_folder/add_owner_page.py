from nicegui import ui
from pydantic import ValidationError
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from datetime import date


async def add_owner_page_render():
    get_header('Add Owner Page')

    # Получаем список разрешений для выбора
    _, permissions = await AsyncOrm.get_owner_permission()
    permission_map = {
        p['owner_permission_id']: f'{p["owner_permission_name"]} - {p["owner_permission_description"]}'
        for p in permissions
    } if permissions else {1: "admin - admin"}

    with ui.column().classes('w-full items-center q-py-xl'):
        with ui.card().classes('w-full max-w-4xl q-pa-lg'):
            ui.label('Add a new owner').classes('text-h6 q-mb-md')

            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                # Основная информация
                firstname = ui.input(label='Owner Firstname *').props('outlined dense').classes('w-full')
                surname = ui.input(label='Owner Surname *').props('outlined dense').classes('w-full')
                
                email = ui.input(label='Owner Email *').props('outlined dense type=email').classes('w-full')
                phone = ui.input(label='Phone').props('outlined dense').classes('w-full')
                
                password = ui.input(label='Password *').props('outlined dense type=password').classes('w-full')
                permission = ui.select(
                    dict(permission_map), 
                    label='Permission Level'
                ).props('outlined dense').classes('w-full')
                
                # Адрес
                address = ui.input(label='Address').props('outlined dense').classes('w-full md:col-span-2')
                city = ui.input(label='City').props('outlined dense').classes('w-full')
                country = ui.input(label='Country').props('outlined dense').classes('w-full')
                zip_code = ui.input(label='ZIP Code').props('outlined dense').classes('w-full')
                
                # Дополнительная информация
                birthday = ui.input(label='Birthday').props('type=date outlined dense').classes('w-full')

            with ui.row().classes('justify-end q-pt-md'):
                submit_btn = ui.button('SUBMIT', color='primary').props('unelevated')

            async def handle_submit():
                try:
                    # Проверяем, что все обязательные поля заполнены
                    if not firstname.value or not surname.value or not email.value or not password.value:
                        ui.notify('Please fill in all required fields (*)', color='negative', position='top')
                        return

                    # Парсим дату рождения если указана
                    birthday_date = None
                    if birthday.value:
                        try:
                            birthday_date = date.fromisoformat(birthday.value)
                        except ValueError:
                            ui.notify('Invalid birthday format. Use YYYY-MM-DD', color='negative', position='top')
                            return

                    await AsyncOrm.add_owner(
                        owner_firstname=firstname.value,
                        owner_surname=surname.value,
                        owner_email=email.value,
                        owner_address=address.value if address.value else None,
                        owner_city=city.value if city.value else None,
                        owner_country=country.value if country.value else None,
                        owner_zip=zip_code.value if zip_code.value else None,
                        owner_birthday=birthday_date,
                        owner_phone=phone.value if phone.value else None,
                        owner_hashed_password=password.value,
                        owner_permission=permission.value if permission.value else 1
                    )
                    ui.notify('Owner added successfully!', color='positive')
                    ui.navigate.to('/owners')
                except ValidationError as e:
                    msg = '; '.join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
                    ui.notify(msg, color='negative', position='top')
                except Exception as e:
                    ui.notify(f'Error adding owner: {str(e)}', color='negative', position='top')

            submit_btn.on('click', handle_submit)
