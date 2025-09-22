"""
Edit breed page for editing breed information
"""
from nicegui import ui
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.breed_service import BreedService
from fastapi import Request


async def edit_breed_page_render(request: Request, breed_id: int):
    """Render the edit breed page"""
    get_header('Edit Breed', request)
    
    # Load breed data
    breed_data = await BreedService.get_breed_data(breed_id)
    if not breed_data:
        ui.label('Breed not found').classes('text-red-500')
        return
    
    with ui.column().classes('w-full max-w-2xl mx-auto p-4'):
        ui.label('Edit Breed Information').classes('text-h4 mb-4')
        
        # Form fields
        with ui.card().classes('w-full p-4'):
            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                # Основная информация
                firstname = ui.input('First Name', value=breed_data.get('breed_firstname', '')).props('outlined dense').classes('w-full')
                lastname = ui.input('Last Name', value=breed_data.get('breed_lastname', '')).props('outlined dense').classes('w-full')
                email = ui.input('Email', value=breed_data.get('breed_email', '')).props('outlined dense type=email').classes('w-full')
                phone = ui.input('Phone', value=breed_data.get('breed_phone', '')).props('outlined dense').classes('w-full')
                
                gender = ui.select(['Male', 'Female'], value=breed_data.get('breed_gender', '')).props('outlined dense').classes('w-full')
                birthday_value = breed_data.get('breed_birthday', '')
                if birthday_value and hasattr(birthday_value, 'isoformat'):
                    birthday_value = birthday_value.isoformat()
                birthday = ui.input('Birthday', value=birthday_value).props('type=date outlined dense').classes('w-full')
                
                # Адрес
                address = ui.input('Address', value=breed_data.get('breed_address', '')).props('outlined dense').classes('w-full md:col-span-2')
                city = ui.input('City', value=breed_data.get('breed_city', '')).props('outlined dense').classes('w-full')
                country = ui.input('Country', value=breed_data.get('breed_country', '')).props('outlined dense').classes('w-full')
                zip_code = ui.input('ZIP Code', value=breed_data.get('breed_zip', '')).props('outlined dense').classes('w-full')
                
                # Описание
                description = ui.textarea('Description', value=breed_data.get('breed_description', '')).props('outlined dense').classes('w-full md:col-span-2')
            
            # Action buttons
            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                async def handle_save():
                    """Handle save button click"""
                    try:
                        # Collect form data
                        # Convert birthday string to date object if provided
                        birthday_date = None
                        if birthday.value:
                            try:
                                from datetime import date
                                birthday_date = date.fromisoformat(birthday.value)
                            except ValueError:
                                ui.notify('Invalid birthday format. Please use YYYY-MM-DD', type='negative')
                                return
                        
                        breed_update_data = {
                            'breed_firstname': firstname.value.strip() if firstname.value else None,
                            'breed_lastname': lastname.value.strip() if lastname.value else None,
                            'breed_email': email.value.strip() if email.value else None,
                            'breed_phone': phone.value.strip() if phone.value else None,
                            'breed_gender': gender.value,
                            'breed_birthday': birthday_date,
                            'breed_address': address.value.strip() if address.value else None,
                            'breed_city': city.value.strip() if city.value else None,
                            'breed_country': country.value.strip() if country.value else None,
                            'breed_zip': zip_code.value.strip() if zip_code.value else None,
                            'breed_description': description.value.strip() if description.value else None
                        }
                        
                        # Update breed
                        success, message = await BreedService.update_breed(breed_id, breed_update_data)
                        if success:
                            ui.notify('Breed updated successfully!', type='positive')
                            ui.navigate.to('/breeds')
                        else:
                            ui.notify(f'Error: {message}', type='negative')
                        
                    except Exception as e:
                        ui.notify(f'Error updating breed: {str(e)}', type='negative')
                
                def handle_cancel():
                    """Handle cancel button click"""
                    ui.navigate.to('/breeds')
                
                ui.button('Save', on_click=handle_save).props('color=primary').classes('px-6')
                ui.button('Cancel', on_click=handle_cancel).props('color=grey').classes('px-6')
