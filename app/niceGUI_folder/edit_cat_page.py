"""
Edit cat page following SOLID principles.
Single Responsibility: Handles UI for cat editing.
Dependency Inversion: Uses service layer for business logic.
"""

import os
from nicegui import ui
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.cat_service import CatService
from app.niceGUI_folder.photo_service import PhotoService
from app.database_folder.orm import AsyncOrm


class EditCatPage:
    """Edit cat page controller"""
    
    def __init__(self, cat_id: int):
        self.cat_id = cat_id
        self.cat_service = CatService(AsyncOrm)
        self.cat_data = None
        
        # UI components
        self.firstname_input = None
        self.surname_input = None
        self.gender_select = None
        self.birthday_input = None
        self.microchip_input = None
        self.colour_input = None
        self.litter_input = None
        self.haritage_input = None
        self.owner_select = None
        
        # Photo management
        self.uploaded_photos = []
        self.photo_container = None
        self.breeder_select = None
        self.dam_select = None
        self.sire_select = None
        
        # Options
        self.owner_options = []
        self.breeder_options = []
        self.dam_options = []
        self.sire_options = []
    
    async def load_data(self):
        """Load cat data and options"""
        try:
            # Load cat data
            self.cat_data = await self.cat_service.get_cat_for_edit(self.cat_id)
            if not self.cat_data:
                ui.notify("Cat not found", type='error')
                ui.navigate.to('/cats')
                return False
            
            # Load options
            self.owner_options, self.breeder_options = await self.cat_service.get_owners_and_breeders()
            self.dam_options, self.sire_options = await self.cat_service.get_available_parents(self.cat_id)
            
            # Debug info
            print(f"Owner options: {self.owner_options}")
            print(f"Breeder options: {self.breeder_options}")
            print(f"Dam options: {self.dam_options}")
            print(f"Sire options: {self.sire_options}")
            
            return True
        except Exception as e:
            ui.notify(f"Error loading data: {str(e)}", type='error')
            print(f"Error in load_data: {e}")
            return False
    
    def create_form(self):
        """Create the edit form"""
        if not self.cat_data:
            return
        
        cat = self.cat_data['cat']
        owner = self.cat_data['owner']
        breeder = self.cat_data['breed']
        dam = self.cat_data['dam']
        sire = self.cat_data['sire']
        
        # Debug info
        print(f"Cat: {cat.cat_firstname} {cat.cat_surname}")
        owner_name = owner.owner_firstname if owner else 'None'
        owner_id = owner.owner_id if owner else 'None'
        print(f"Owner: {owner_name} (ID: {owner_id})")
        print(f"Breeder: {breeder.breed_firstname if breeder else 'None'} (ID: {breeder.breed_id if breeder else 'None'})")
        print(f"Dam: {dam.cat_firstname if dam else 'None'} (ID: {dam.cat_id if dam else 'None'})")
        print(f"Sire: {sire.cat_firstname if sire else 'None'} (ID: {sire.cat_id if sire else 'None'})")
        
        # Debug the actual objects
        print(f"Owner object type: {type(owner)}")
        print(f"Breeder object type: {type(breeder)}")
        print(f"Dam object type: {type(dam)}")
        print(f"Sire object type: {type(sire)}")
        
        with ui.card().classes('w-full max-w-4xl mx-auto'):
            ui.label('✏️ Edit Cat Information').classes('text-h4 text-center mb-6')
            
            with ui.grid(columns=2).classes('gap-4'):
                # Basic Information
                with ui.card().classes('p-4'):
                    ui.label('🐱 Basic Information').classes('text-h6 mb-4')
                    
                    self.firstname_input = ui.input(
                        label='First Name',
                        value=cat.cat_firstname
                    ).classes('w-full')
                    
                    self.surname_input = ui.input(
                        label='Surname',
                        value=cat.cat_surname
                    ).classes('w-full')
                    
                    self.gender_select = ui.select(
                        options=['Male', 'Female'],
                        value=cat.cat_gender,
                        label='Gender'
                    ).classes('w-full')
                    
                    self.birthday_input = ui.input(
                        label='Birthday (YYYY-MM-DD)',
                        value=cat.cat_birthday.strftime('%Y-%m-%d') if cat.cat_birthday else ''
                    ).classes('w-full')
                
                # Additional Information
                with ui.card().classes('p-4'):
                    ui.label('📋 Additional Information').classes('text-h6 mb-4')
                    
                    self.microchip_input = ui.input(
                        label='Microchip Number',
                        value=cat.cat_microchip_number or ''
                    ).classes('w-full')
                    
                    self.colour_input = ui.input(
                        label='Color',
                        value=cat.cat_EMS_colour or ''
                    ).classes('w-full')
                    
                    self.litter_input = ui.input(
                        label='Litter',
                        value=cat.cat_litter or ''
                    ).classes('w-full')
                    
                    self.haritage_input = ui.input(
                        label='Heritage Number',
                        value=cat.cat_haritage_number or ''
                    ).classes('w-full')
            
            with ui.grid(columns=2).classes('gap-4 mt-4'):
                # Owner and Breeder
                with ui.card().classes('p-4'):
                    ui.label('👤 Owner & Breeder').classes('text-h6 mb-4')
                    
                    # Create owner select without default value
                    if self.owner_options:
                        # Convert to simple dict for ui.select
                        owner_dict = {opt['value']: opt['label'] for opt in self.owner_options}
                        self.owner_select = ui.select(
                            options=owner_dict,
                            label='Owner'
                        ).classes('w-full').props('clearable')
                        
                        # Set value after creation if we have a current owner
                        if owner and owner.owner_id:
                            owner_id_str = str(owner.owner_id)
                            print(f"Setting owner value to: {owner_id_str}")
                            # Try to set the value, but don't fail if it doesn't work
                            try:
                                self.owner_select.value = owner_id_str
                            except Exception as e:
                                print(f"Could not set owner value: {e}")
                    else:
                        ui.label('No owners available').classes('text-gray-500')
                        self.owner_select = None
                    
                    # Create breeder select without default value
                    if self.breeder_options:
                        # Convert to simple dict for ui.select
                        breeder_dict = {opt['value']: opt['label'] for opt in self.breeder_options}
                        self.breeder_select = ui.select(
                            options=breeder_dict,
                            label='Breeder'
                        ).classes('w-full').props('clearable')
                        
                        # Set value after creation if we have a current breeder
                        if breeder and breeder.breed_id:
                            breeder_id_str = str(breeder.breed_id)
                            print(f"Setting breeder value to: {breeder_id_str}")
                            # Try to set the value, but don't fail if it doesn't work
                            try:
                                self.breeder_select.value = breeder_id_str
                            except Exception as e:
                                print(f"Could not set breeder value: {e}")
                    else:
                        ui.label('No breeders available').classes('text-gray-500')
                        self.breeder_select = None
                
                # Parents
                with ui.card().classes('p-4'):
                    ui.label('👨‍👩‍👧‍👦 Parents').classes('text-h6 mb-4')
                    
                    # Create dam select without default value
                    if self.dam_options:
                        # Convert to simple dict for ui.select
                        dam_dict = {opt['value']: opt['label'] for opt in self.dam_options}
                        self.dam_select = ui.select(
                            options=dam_dict,
                            label='Mother (Dam)'
                        ).classes('w-full').props('clearable')
                        
                        # Set value after creation if we have a current dam
                        if dam and dam.cat_id:
                            dam_id_str = str(dam.cat_id)
                            print(f"Setting dam value to: {dam_id_str}")
                            # Try to set the value, but don't fail if it doesn't work
                            try:
                                self.dam_select.value = dam_id_str
                            except Exception as e:
                                print(f"Could not set dam value: {e}")
                    else:
                        ui.label('No female cats available').classes('text-gray-500')
                        self.dam_select = None
                    
                    # Create sire select without default value
                    if self.sire_options:
                        # Convert to simple dict for ui.select
                        sire_dict = {opt['value']: opt['label'] for opt in self.sire_options}
                        self.sire_select = ui.select(
                            options=sire_dict,
                            label='Father (Sire)'
                        ).classes('w-full').props('clearable')
                        
                        # Set value after creation if we have a current sire
                        if sire and sire.cat_id:
                            sire_id_str = str(sire.cat_id)
                            print(f"Setting sire value to: {sire_id_str}")
                            # Try to set the value, but don't fail if it doesn't work
                            try:
                                self.sire_select.value = sire_id_str
                            except Exception as e:
                                print(f"Could not set sire value: {e}")
                    else:
                        ui.label('No male cats available').classes('text-gray-500')
                        self.sire_select = None
            
            # Photos section
            ui.separator().classes('my-6')
            ui.label('📸 Photos').classes('text-h6 mb-4')
            
            # Load existing photos and filter out non-existent files
            existing_photos = list(cat.cat_photos) if cat.cat_photos else []
            self.uploaded_photos = []
            for photo_path in existing_photos:
                if photo_path and os.path.exists(photo_path):
                    self.uploaded_photos.append(photo_path)
                else:
                    print(f"Photo file does not exist, skipping: {photo_path}")
            
            print(f"Loaded {len(self.uploaded_photos)} existing photos out of {len(existing_photos)} in database")
            
            # Photo upload area
            self.photo_container = ui.column().classes('w-full')
            
            def handle_photo_upload(e):
                """Handle photo upload"""
                try:
                    # Validate photo (without size check since we'll compress if needed)
                    is_valid, error_msg = PhotoService.is_valid_photo(e.name)
                    if not is_valid:
                        ui.notify(error_msg, color='negative', position='top')
                        return
                    
                    # Save photo (with automatic compression)
                    photo_path = PhotoService.save_photo(e.content.read(), e.name)
                    if photo_path:
                        self.uploaded_photos.append(photo_path)
                        self.update_photo_gallery()
                        ui.notify(f'Photo "{e.name}" uploaded successfully!', color='positive', position='top')
                    else:
                        ui.notify('Failed to save photo', color='negative', position='top')
                        
                except Exception as ex:
                    ui.notify(f'Error uploading photo: {str(ex)}', color='negative', position='top')
            
            # Upload widget
            ui.upload(
                on_upload=handle_photo_upload,
                auto_upload=True,
                max_file_size=PhotoService.MAX_FILE_SIZE
            ).props('accept=image/*').classes('w-full q-mb-md')
            
            # Initial gallery display
            self.update_photo_gallery()

            # Action buttons
            with ui.row().classes('w-full justify-center mt-6 gap-4'):
                ui.button(
                    '💾 Save Changes',
                    on_click=self.handle_save
                ).classes('bg-green-500 text-white')
                
                ui.button(
                    '🗑️ Delete Cat',
                    on_click=self.handle_delete
                ).classes('bg-red-500 text-white')
                
                ui.button(
                    '❌ Cancel',
                    on_click=lambda: ui.navigate.to('/cats')
                ).classes('bg-gray-500 text-white')
    
    def update_photo_gallery(self):
        """Update photo gallery display"""
        if not self.photo_container:
            return
            
        self.photo_container.clear()
        with self.photo_container:
            if self.uploaded_photos:
                ui.label(f'Photos ({len(self.uploaded_photos)}):').classes('text-subtitle2 q-mb-sm')
                PhotoService.create_photo_gallery(self.uploaded_photos, "300px")
                
                # Add delete buttons for each photo
                for i, photo_path in enumerate(self.uploaded_photos):
                    def delete_photo(index=i):
                        if index < len(self.uploaded_photos):
                            photo_to_delete = self.uploaded_photos[index]
                            print(f"Deleting photo {index}: {photo_to_delete}")
                            
                            # Delete file from disk
                            if PhotoService.delete_photo(photo_to_delete):
                                # Remove from list
                                self.uploaded_photos.pop(index)
                                print(f"Photo deleted, remaining photos: {self.uploaded_photos}")
                                
                                # Update gallery
                                self.update_photo_gallery()
                                ui.notify('Photo deleted', color='info', position='top')
                            else:
                                ui.notify('Failed to delete photo file', color='negative', position='top')
                        else:
                            print(f"Invalid photo index: {index}")
                            ui.notify('Invalid photo index', color='negative', position='top')
                    
                    with ui.row().classes('items-center gap-2 q-mt-sm'):
                        ui.button('Delete', on_click=delete_photo, color='negative').props('dense size=sm')
            else:
                ui.label('No photos uploaded yet').classes('text-grey-6')

    async def handle_save(self):
        """Handle save button click"""
        try:
            # Collect form data
            def safe_int(value):
                """Safely convert value to int, return None if invalid"""
                if value is None or value == '' or value == 'None':
                    return None
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
            
            data = {
                'firstname': self.firstname_input.value,
                'surname': self.surname_input.value,
                'gender': self.gender_select.value,
                'birthday': self.birthday_input.value,
                'microchip': self.microchip_input.value.strip() if self.microchip_input.value else None,
                'colour': self.colour_input.value.strip() if self.colour_input.value else None,
                'litter': self.litter_input.value.strip() if self.litter_input.value else None,
                'haritage_number': self.haritage_input.value.strip() if self.haritage_input.value else None,
                'owner_id': safe_int(self.owner_select.value) if self.owner_select else None,
                'breed_id': safe_int(self.breeder_select.value) if self.breeder_select else None,
                'dam_id': safe_int(self.dam_select.value) if self.dam_select else None,
                'sire_id': safe_int(self.sire_select.value) if self.sire_select else None,
                'cat_photos': [photo for photo in self.uploaded_photos if photo and os.path.exists(photo)]
            }
            
            print(f"Saving cat with {len(data['cat_photos'])} photos: {data['cat_photos']}")
            
            # Validate and save
            success, message = await self.cat_service.update_cat(self.cat_id, data)
            
            if success:
                ui.notify(message, type='positive')
                ui.navigate.to(f'/cat_profile/{self.cat_id}')
            else:
                ui.notify(message, type='negative')
                
        except Exception as e:
            ui.notify(f"Error saving cat: {str(e)}", type='error')
    
    async def handle_delete(self):
        """Handle delete button click"""
        try:
            # Show confirmation dialog
            with ui.dialog() as dialog, ui.card():
                ui.label('⚠️ Confirm Deletion').classes('text-h6 mb-4')
                cat_name = f'{self.cat_data["cat"].cat_firstname} {self.cat_data["cat"].cat_surname}'
                ui.label(f'Are you sure you want to delete {cat_name}?')
                ui.label('This action cannot be undone!').classes('text-red-500')
                
                with ui.row().classes('w-full justify-end mt-4 gap-2'):
                    ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                    ui.button('Delete', on_click=lambda: self.confirm_delete(dialog)).classes('bg-red-500 text-white')
            
            dialog.open()
            
        except Exception as e:
            ui.notify(f"Error showing delete dialog: {str(e)}", type='error')
    
    async def confirm_delete(self, dialog):
        """Confirm cat deletion"""
        try:
            dialog.close()
            success, message = await self.cat_service.delete_cat(self.cat_id)
            
            if success:
                ui.notify(message, type='positive')
                ui.navigate.to('/cats')
            else:
                ui.notify(message, type='negative')
                
        except Exception as e:
            ui.notify(f"Error deleting cat: {str(e)}", type='error')


async def edit_cat_page_render(cat_id: int):
    """Render edit cat page"""
    get_header('✏️ Edit Cat')
    
    # Create page controller
    page = EditCatPage(cat_id)
    
    # Load data
    if await page.load_data():
        page.create_form()
    else:
        ui.label('Loading failed').classes('text-center text-red-500')
