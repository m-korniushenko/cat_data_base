"""
Edit breed page for editing breed information
"""
from nicegui import ui
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.breed_service import BreedService


async def edit_breed_page_render(breed_id: int):
    """Render the edit breed page"""
    get_header('Edit Breed')
    
    # Load breed data
    breed_data = await BreedService.get_breed_data(breed_id)
    if not breed_data:
        ui.label('Breed not found').classes('text-red-500')
        return
    
    with ui.column().classes('w-full max-w-2xl mx-auto p-4'):
        ui.label('Edit Breed Information').classes('text-h4 mb-4')
        
        # Form fields
        with ui.card().classes('w-full p-4'):
            firstname = ui.input('First Name', value=breed_data.get('breed_firstname', '')).classes('w-full mb-2')
            lastname = ui.input('Last Name', value=breed_data.get('breed_lastname', '')).classes('w-full mb-2')
            email = ui.input('Email', value=breed_data.get('breed_email', '')).classes('w-full mb-2')
            phone = ui.input('Phone', value=breed_data.get('breed_phone', '')).classes('w-full mb-2')
            address = ui.input('Address', value=breed_data.get('breed_address', '')).classes('w-full mb-2')
            
            # Action buttons
            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                async def handle_save():
                    """Handle save button click"""
                    try:
                        # Collect form data
                        breed_update_data = {
                            'breed_firstname': firstname.value.strip(),
                            'breed_lastname': lastname.value.strip(),
                            'breed_email': email.value.strip(),
                            'breed_phone': phone.value.strip(),
                            'breed_address': address.value.strip()
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
