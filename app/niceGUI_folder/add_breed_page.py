from nicegui import ui
from pydantic import ValidationError
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from datetime import date
from fastapi import Request


async def add_breed_page_render(request: Request):
    get_header('Add Breed Page', request)

    with ui.column().classes('w-full items-center q-py-xl'):
        with ui.card().classes('w-full max-w-4xl q-pa-lg'):
            ui.label('Add a new breed').classes('text-h6 q-mb-md')

            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                # Основная информация
                firstname = ui.input(label='Breed Firstname *').props('outlined dense').classes('w-full')
                surname = ui.input(label='Breed Surname *').props('outlined dense').classes('w-full')
                
                email = ui.input(label='Breed Email *').props('outlined dense type=email').classes('w-full')
                phone = ui.input(label='Phone').props('outlined dense').classes('w-full')
                
                gender = ui.select(['Male', 'Female'], label='Gender').props('outlined dense').classes('w-full')
                birthday = ui.input(label='Birthday').props('type=date outlined dense').classes('w-full')
                
                # Адрес (по аналогии с Owner)
                address = ui.input(label='Address').props('outlined dense').classes('w-full md:col-span-2')
                city = ui.input(label='City').props('outlined dense').classes('w-full')
                country = ui.input(label='Country').props('outlined dense').classes('w-full')
                zip_code = ui.input(label='ZIP Code').props('outlined dense').classes('w-full')
                
                # Описание
                description = ui.textarea(label='Description').props('outlined dense').classes('w-full md:col-span-2')

            with ui.row().classes('justify-end q-pt-md'):
                submit_btn = ui.button('SUBMIT', color='primary').props('unelevated')

            async def handle_submit():
                try:
                    # Проверяем, что все обязательные поля заполнены
                    if not firstname.value or not surname.value or not email.value:
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

                    # Валидация email
                    if '@' not in email.value:
                        ui.notify('Please enter a valid email address', color='negative', position='top')
                        return

                    await AsyncOrm.add_breed(
                        breed_firstname=firstname.value,
                        breed_surname=surname.value,
                        breed_gender=gender.value if gender.value else None,
                        breed_birthday=birthday_date,
                        breed_address=address.value if address.value else None,
                        breed_city=city.value if city.value else None,
                        breed_country=country.value if country.value else None,
                        breed_zip=zip_code.value if zip_code.value else None,
                        breed_phone=phone.value if phone.value else None,
                        breed_email=email.value,
                        breed_description=description.value if description.value else None
                    )
                    ui.notify('Breed added successfully!', color='positive', position='top')
                    ui.navigate.to('/breeds')
                except ValidationError as e:
                    msg = '; '.join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
                    ui.notify(msg, color='negative', position='top')
                except Exception as e:
                    ui.notify(f'Error adding breed: {str(e)}', color='negative', position='top')

            submit_btn.on('click', handle_submit)
