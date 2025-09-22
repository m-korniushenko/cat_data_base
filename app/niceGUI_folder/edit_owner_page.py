"""
Edit owner page for editing owner information
"""
from nicegui import ui
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.owner_service import OwnerService
from fastapi import Request


async def edit_owner_page_render(request: Request, owner_id: int):
    """Render the edit owner page"""
    get_header('Edit Owner', request)
    
    # Load owner data
    owner_data = await OwnerService.get_owner_data(owner_id)
    if not owner_data:
        ui.label('Owner not found').classes('text-red-500')
        return
    
    with ui.column().classes('w-full max-w-2xl mx-auto p-4'):
        ui.label('Edit Owner Information').classes('text-h4 mb-4')
        
        # Form fields
        with ui.card().classes('w-full p-4'):
            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                # Основная информация
                firstname = ui.input('First Name', value=owner_data.get('owner_firstname', '')).props('outlined dense').classes('w-full')
                lastname = ui.input('Last Name', value=owner_data.get('owner_lastname', '')).props('outlined dense').classes('w-full')
                email = ui.input('Email', value=owner_data.get('owner_email', '')).props('outlined dense type=email').classes('w-full')
                phone = ui.input('Phone', value=owner_data.get('owner_phone', '')).props('outlined dense').classes('w-full')
                
                # Адрес
                address = ui.input('Address', value=owner_data.get('owner_address', '')).props('outlined dense').classes('w-full md:col-span-2')
                city = ui.input('City', value=owner_data.get('owner_city', '')).props('outlined dense').classes('w-full')
                country = ui.input('Country', value=owner_data.get('owner_country', '')).props('outlined dense').classes('w-full')
                zip_code = ui.input('ZIP Code', value=owner_data.get('owner_zip', '')).props('outlined dense').classes('w-full')
                
                # Дополнительная информация
                birthday_value = owner_data.get('owner_birthday', '')
                if birthday_value and hasattr(birthday_value, 'isoformat'):
                    birthday_value = birthday_value.isoformat()
                birthday = ui.input('Birthday', value=birthday_value).props('type=date outlined dense').classes('w-full')
                permission = ui.input('Permission', value=str(owner_data.get('owner_permission', ''))).props('outlined dense readonly').classes('w-full')
            
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
                        
                        owner_update_data = {
                            'owner_firstname': firstname.value.strip(),
                            'owner_lastname': lastname.value.strip(),
                            'owner_email': email.value.strip(),
                            'owner_phone': phone.value.strip(),
                            'owner_address': address.value.strip(),
                            'owner_city': city.value.strip(),
                            'owner_country': country.value.strip(),
                            'owner_zip': zip_code.value.strip(),
                            'owner_birthday': birthday_date
                        }
                        
                        # Update owner
                        success, message = await OwnerService.update_owner(owner_id, owner_update_data)
                        if success:
                            ui.notify('Owner updated successfully!', type='positive')
                            ui.navigate.to('/owners')
                        else:
                            ui.notify(f'Error: {message}', type='negative')
                        
                    except Exception as e:
                        ui.notify(f'Error updating owner: {str(e)}', type='negative')
                
                def handle_cancel():
                    """Handle cancel button click"""
                    ui.navigate.to('/owners')
                
                ui.button('Save', on_click=handle_save).props('color=primary').classes('px-6')
                ui.button('Cancel', on_click=handle_cancel).props('color=grey').classes('px-6')
