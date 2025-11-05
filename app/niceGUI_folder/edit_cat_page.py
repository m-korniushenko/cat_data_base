"""
Edit cat page following SOLID principles.
Single Responsibility: Handles UI for cat editing.
Dependency Inversion: Uses service layer for business logic.
"""

import os
from datetime import datetime
from nicegui import ui
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.cat_service import CatService
from app.niceGUI_folder.photo_service import PhotoService
from app.niceGUI_folder.file_service import FileService
from app.database_folder.orm import AsyncOrm
from fastapi import Request


class EditCatPage:
    """Edit cat page controller"""

    def __init__(self, cat_id: int):
        self.cat_id = cat_id
        self.cat_service = CatService(AsyncOrm)
        self.cat_data = None
        self.firstname_input = None
        self.surname_input = None
        self.gender_select = None
        self.birthday_input = None
        self.microchip_input = None
        self.colour_input = None
        self.litter_input = None
        self.haritage_input = None
        self.owner_select = None

        self.uploaded_photos = []
        self.uploaded_files = []
        self.photo_container = None
        self.file_container = None
        self.breeder_select = None
        self.dam_select = None
        self.sire_select = None

        self.owner_options = []
        self.breeder_options = []
        self.dam_options = []
        self.sire_options = []

    async def load_data(self):
        """Load cat data and options"""
        try:
            self.cat_data = await self.cat_service.get_cat_for_edit(self.cat_id)
            if not self.cat_data:
                ui.notify("Cat not found", type='error')
                ui.navigate.to('/cats')
                return False

            self.owner_options, self.breeder_options = await self.cat_service.get_owners_and_breeders()
            self.dam_options, self.sire_options = await self.cat_service.get_available_parents(self.cat_id)

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

        print(f"Cat: {cat.cat_firstname} {cat.cat_surname}")
        owner_name = owner.owner_firstname if owner else 'None'
        owner_id = owner.owner_id if owner else 'None'
        print(f"Owner: {owner_name} (ID: {owner_id})")
        print(f"Breeder: {breeder.breed_firstname if breeder else 'None'} (ID: {breeder.breed_id if breeder else 'None'})")
        print(f"Dam: {dam.cat_firstname if dam else 'None'} (ID: {dam.cat_id if dam else 'None'})")
        print(f"Sire: {sire.cat_firstname if sire else 'None'} (ID: {sire.cat_id if sire else 'None'})")

        print(f"Owner object type: {type(owner)}")
        print(f"Breeder object type: {type(breeder)}")
        print(f"Dam object type: {type(dam)}")
        print(f"Sire object type: {type(sire)}")

        with ui.card().classes('w-full max-w-4xl mx-auto'):
            ui.label('✏️ Edit Cat Information').classes('text-h4 text-center mb-6')

            # Basic Information Section
            with ui.card().classes('p-4 mb-4'):
                ui.label('🐱 Basic Information').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.firstname_input = ui.input(
                        label='Name *',
                        value=cat.cat_firstname
                    ).classes('w-full')

                    self.surname_input = ui.input(
                        label='Surname',
                        value=cat.cat_surname or ''
                    ).classes('w-full')

                    self.callname_input = ui.input(
                        label='Callname',
                        value=cat.cat_callname or ''
                    ).classes('w-full')

                    self.gender_select = ui.select(
                        options=['Male', 'Female'],
                        value=cat.cat_gender,
                        label='Gender *'
                    ).classes('w-full')

                    self.birthday_input = ui.input(
                        label='Birthday *',
                        value=cat.cat_birthday.strftime('%Y-%m-%d') if cat.cat_birthday else ''
                    ).props('type=date outlined dense').classes('w-full')

                    self.microchip_input = ui.input(
                        label='Chip Number',
                        value=cat.cat_microchip_number or ''
                    ).classes('w-full')

                    self.original_microchip = cat.cat_microchip_number

                    self.title_select = ui.select(
                        options=['', 'Champion', 'Grand Champion', 'Supreme Grand Champion'],
                        value=cat.cat_title[0] if cat.cat_title else '',
                        label='Title'
                    ).classes('w-full')

                    self.haritage_input = ui.input(
                        label='Studbook Number 1',
                        value=cat.cat_haritage_number or ''
                    ).classes('w-full')

                    self.haritage_2_input = ui.input(
                        label='Studbook Number 2',
                        value=cat.cat_haritage_number_2 or ''
                    ).classes('w-full')

            # Breed and Color Information
            with ui.card().classes('p-4 mb-4'):
                ui.label('🎨 Breed & Color Information').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.colour_input = ui.input(
                        label='Color',
                        value=cat.cat_EMS_colour or ''
                    ).classes('w-full')

                    self.eye_colour_select = ui.select(
                        options=['', 'Blue', 'Green', 'Yellow', 'Orange', 'Heterochromatic'],
                        value=cat.cat_eye_colour or '',
                        label='Eye Color'
                    ).classes('w-full')

                    self.hair_type_select = ui.select(
                        options=['', 'Short Hair', 'Long Hair', 'Semi-Long Hair'],
                        value=cat.cat_hair_type or '',
                        label='Hair Type'
                    ).classes('w-full')

                    self.litter_input = ui.input(
                        label='Litter',
                        value=cat.cat_litter or ''
                    ).classes('w-full')

                    self.litter_size_male_input = ui.number(
                        label='Litter Size (Male)',
                        value=cat.cat_litter_size_male or 0,
                        min=0, max=20
                    ).props('outlined dense').classes('w-full')

                    self.litter_size_female_input = ui.number(
                        label='Litter Size (Female)',
                        value=cat.cat_litter_size_female or 0,
                        min=0, max=20
                    ).props('outlined dense').classes('w-full')

            # Health and Medical Information
            with ui.card().classes('p-4 mb-4'):
                ui.label('🏥 Health & Medical Information').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.tests_input = ui.input(
                        label='Tests',
                        value=cat.cat_tests or ''
                    ).classes('w-full')

                    self.blood_group_input = ui.input(
                        label='Blood Group',
                        value=cat.cat_blood_group or ''
                    ).classes('w-full')

                    self.gencode_input = ui.input(
                        label='Gencode',
                        value=cat.cat_gencode or ''
                    ).classes('w-full')

                    self.weight_input = ui.number(
                        label='Weight (kg)',
                        value=cat.cat_weight or 0.0,
                        min=0.0, max=50.0, step=0.1
                    ).props('outlined dense').classes('w-full')

                    self.birth_weight_input = ui.number(
                        label='Birth Weight (g)',
                        value=cat.cat_birth_weight or 0.0,
                        min=0.0, max=200.0, step=0.1
                    ).props('outlined dense').classes('w-full')

                    self.transfer_weight_input = ui.number(
                        label='Transfer Weight (g)',
                        value=cat.cat_transfer_weight or 0.0,
                        min=0.0, max=200.0, step=0.1
                    ).props('outlined dense').classes('w-full')

            # Breeding Information
            with ui.card().classes('p-4 mb-4'):
                ui.label('🐾 Breeding Information').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.breeding_lock_checkbox = ui.checkbox(
                        'Breeding Lock',
                        value=cat.cat_breeding_lock or False
                    )

                    self.breeding_lock_date_input = ui.input(
                        label='Breeding Lock Date',
                        value=cat.cat_breeding_lock_date.strftime('%Y-%m-%d') if cat.cat_breeding_lock_date else ''
                    ).props('type=date outlined dense').classes('w-full')

                    self.breeding_animal_checkbox = ui.checkbox(
                        'Breeding Animal',
                        value=cat.cat_breeding_animal or False
                    )

                    self.kitten_transfer_checkbox = ui.checkbox(
                        'Kitten Transfer',
                        value=cat.cat_kitten_transfer or False
                    )

                    self.wcf_sticker_input = ui.input(
                        label='WCF Sticker',
                        value=cat.wcf_sticker or ''
                    ).props('outlined dense').classes('w-full')

            # Location and Association
            with ui.card().classes('p-4 mb-4'):
                ui.label('📍 Location & Association').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.birth_country_input = ui.input(
                        label='Birth Country',
                        value=cat.cat_birth_country or ''
                    ).classes('w-full')

                    self.location_input = ui.input(
                        label='Location',
                        value=cat.cat_location or ''
                    ).classes('w-full')

                    self.association_input = ui.input(
                        label='Association',
                        value=cat.cat_association or ''
                    ).classes('w-full')

            # Health Issues
            with ui.card().classes('p-4 mb-4'):
                ui.label('⚠️ Health Issues').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.faults_deviations_input = ui.input(
                        label='Faults / Deviations',
                        value=cat.cat_faults_deviations or ''
                    ).classes('w-full')

                    self.jaw_fault_select = ui.select(
                        options=['', 'None', 'Overbite', 'Underbite', 'Crossbite'],
                        value=cat.cat_jaw_fault or '',
                        label='Jaw Fault'
                    ).classes('w-full')

                    self.hernia_select = ui.select(
                        options=['', 'None', 'Umbilical', 'Inguinal', 'Diaphragmatic'],
                        value=cat.cat_hernia or '',
                        label='Hernia'
                    ).classes('w-full')

                    self.testicles_select = ui.select(
                        options=['', 'Normal', 'Cryptorchid', 'Monorchid'],
                        value=cat.cat_testicles or '',
                        label='Testicles'
                    ).classes('w-full')

            # Death Information
            with ui.card().classes('p-4 mb-4'):
                ui.label('💀 Death Information').classes('text-h6 mb-4')
                with ui.grid(columns=2).classes('gap-4'):
                    self.death_date_input = ui.input(
                        label='Death Date',
                        value=cat.cat_death_date.strftime('%Y-%m-%d') if cat.cat_death_date else ''
                    ).props('type=date outlined dense').classes('w-full')

                    self.death_cause_input = ui.input(
                        label='Death Cause',
                        value=cat.cat_death_cause or ''
                    ).classes('w-full')

                    self.status_select = ui.select(
                        options=['', 'Alive', 'Deceased', 'Missing', 'Transferred'],
                        value=cat.cat_status or '',
                        label='Status'
                    ).classes('w-full')

            # Additional Information
            with ui.card().classes('p-4 mb-4'):
                ui.label('📝 Additional Information').classes('text-h6 mb-4')
                with ui.grid(columns=1).classes('gap-4'):
                    self.features_textarea = ui.textarea(
                        label='Features',
                        value=cat.cat_features or ''
                    ).props('outlined dense').classes('w-full')

                    self.notes_textarea = ui.textarea(
                        label='Notes',
                        value=cat.cat_notes or ''
                    ).props('outlined dense').classes('w-full')

                self.show_results_textarea = ui.textarea(
                    label='Show Results',
                    value=cat.cat_show_results or ''
                ).props('outlined dense').classes('w-full')

                self.description_textarea = ui.textarea(
                    label='Description',
                    value=cat.cat_description or ''
                ).props('outlined dense').classes('w-full')

            with ui.grid(columns=2).classes('gap-4 mt-4'):
                with ui.card().classes('p-4'):
                    ui.label('👤 Owner & Breeder').classes('text-h6 mb-4')
                    if self.owner_options:
                        owner_dict = {opt['value']: opt['label'] for opt in self.owner_options}
                        self.owner_select = ui.select(
                            options=owner_dict,
                            label='Owner'
                        ).classes('w-full').props('clearable use-input')
                        if owner and owner.owner_id:
                            owner_id_str = str(owner.owner_id)
                            print(f"Setting owner value to: {owner_id_str}")
                            try:
                                self.owner_select.value = owner_id_str
                            except Exception as e:
                                print(f"Could not set owner value: {e}")
                    else:
                        ui.label('No owners available').classes('text-gray-500')
                        self.owner_select = None
                    if self.breeder_options:
                        breeder_dict = {opt['value']: opt['label'] for opt in self.breeder_options}
                        self.breeder_select = ui.select(
                            options=breeder_dict,
                            label='Breeder'
                        ).classes('w-full').props('clearable use-input')
                        if breeder and breeder.breed_id:
                            breeder_id_str = str(breeder.breed_id)
                            print(f"Setting breeder value to: {breeder_id_str}")
                            try:
                                self.breeder_select.value = breeder_id_str
                            except Exception as e:
                                print(f"Could not set breeder value: {e}")
                    else:
                        ui.label('No breeders available').classes('text-gray-500')
                        self.breeder_select = None
                with ui.card().classes('p-4'):
                    ui.label('👨‍👩‍👧‍👦 Parents').classes('text-h6 mb-4')
                    if self.dam_options:
                        dam_dict = {opt['value']: opt['label'] for opt in self.dam_options}
                        self.dam_select = ui.select(
                            options=dam_dict,
                            label='Mother (Dam)'
                        ).classes('w-full').props('clearable use-input')
                        if dam and dam.cat_id:
                            dam_id_str = str(dam.cat_id)
                            print(f"Setting dam value to: {dam_id_str}")
                            try:
                                self.dam_select.value = dam_id_str
                            except Exception as e:
                                print(f"Could not set dam value: {e}")
                    else:
                        ui.label('No female cats available').classes('text-gray-500')
                        self.dam_select = None
                    if self.sire_options:
                        sire_dict = {opt['value']: opt['label'] for opt in self.sire_options}
                        self.sire_select = ui.select(
                            options=sire_dict,
                            label='Father (Sire)'
                        ).classes('w-full').props('clearable use-input')
                        if sire and sire.cat_id:
                            sire_id_str = str(sire.cat_id)
                            print(f"Setting sire value to: {sire_id_str}")
                            try:
                                self.sire_select.value = sire_id_str
                            except Exception as e:
                                print(f"Could not set sire value: {e}")
                    else:
                        ui.label('No male cats available').classes('text-gray-500')
                        self.sire_select = None
            ui.separator().classes('my-6')
            ui.label('📸 Photos').classes('text-h6 mb-4')
            existing_photos = list(cat.cat_photos) if cat.cat_photos else []
            self.uploaded_photos = []
            for photo_path in existing_photos:
                if photo_path and os.path.exists(photo_path):
                    self.uploaded_photos.append(photo_path)
                else:
                    print(f"Photo file does not exist, skipping: {photo_path}")
            print(f"Loaded {len(self.uploaded_photos)} existing photos out of {len(existing_photos)} in database")
            existing_files = list(cat.cat_files) if cat.cat_files else []
            self.uploaded_files = []
            for file_path in existing_files:
                if file_path and os.path.exists(file_path):
                    self.uploaded_files.append(file_path)
                else:
                    print(f"File does not exist, skipping: {file_path}")
            print(f"Loaded {len(self.uploaded_files)} existing files out of {len(existing_files)} in database")
            self.photo_container = ui.column().classes('w-full')

            def handle_photo_upload(e):
                """Handle photo upload"""
                try:
                    is_valid, error_msg = PhotoService.is_valid_photo(e.name)
                    if not is_valid:
                        ui.notify(error_msg, color='negative', position='top')
                        return
                    microchip = self.microchip_input.value if self.microchip_input.value else None
                    photo_path = PhotoService.save_photo(e.content.read(), e.name, microchip)
                    if photo_path:
                        self.uploaded_photos.append(photo_path)
                        self.update_photo_gallery()
                        ui.notify(f'Photo "{e.name}" uploaded successfully!', color='positive', position='top')
                    else:
                        ui.notify('Failed to save photo', color='negative', position='top')

                except Exception as ex:
                    ui.notify(f'Error uploading photo: {str(ex)}', color='negative', position='top')
            ui.upload(
                on_upload=handle_photo_upload,
                auto_upload=True,
                max_file_size=PhotoService.MAX_FILE_SIZE
            ).props('accept=image/*').classes('w-full q-mb-md')
            self.update_photo_gallery()
        ui.separator().classes('my-6')
        ui.label('📁 Files').classes('text-h6 mb-4')
        self.file_container = ui.column().classes('w-full')

        def handle_file_upload(e):
            """Handle file upload"""
            try:
                is_valid, error_msg = FileService.is_valid_file(e)
                if not is_valid:
                    ui.notify(error_msg, color='negative', position='top')
                    return
                microchip = self.microchip_input.value if self.microchip_input.value else None
                success, message, file_path = FileService.save_file(microchip, e)
                if success:
                    self.uploaded_files.append(file_path)
                    self.update_file_list()
                    ui.notify(f'File "{e.name}" uploaded successfully!', color='positive', position='top')
                else:
                    ui.notify(f'Error uploading file: {message}', color='negative', position='top')

            except Exception as ex:
                ui.notify(f'Error uploading file: {str(ex)}', color='negative', position='top')

        def update_file_list():
            """Update file list display"""
            self.file_container.clear()
            with self.file_container:
                if self.uploaded_files:
                    ui.label(f'Files ({len(self.uploaded_files)}):').classes('text-subtitle2 q-mb-sm')
                    FileService.create_file_list(self.uploaded_files, "300px")
                    for i, file_path in enumerate(self.uploaded_files):
                        def delete_file(index=i):
                            if index < len(self.uploaded_files):
                                file_to_delete = self.uploaded_files[index]
                                print(f"Deleting file {index}: {file_to_delete}")
                                if FileService.delete_file(file_to_delete):
                                    self.uploaded_files.pop(index)
                                    print(f"File deleted, remaining files: {self.uploaded_files}")
                                    self.update_file_list()
                                    ui.notify('File deleted successfully!', color='positive', position='top')
                                else:
                                    ui.notify('Failed to delete file', color='negative', position='top')

                        with ui.row().classes('items-center gap-2 q-mt-sm'):
                            ui.button('Delete', on_click=delete_file, color='negative').props('dense size=sm')
                else:
                    ui.label('No files uploaded yet').classes('text-grey-6')
        ui.upload(
            on_upload=handle_file_upload,
            auto_upload=True,
            max_file_size=FileService.MAX_FILE_SIZE
        ).props('accept=.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.zip,.rar').classes('w-full q-mb-md')
        self.update_file_list = update_file_list
        self.update_file_list()
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
                for i, photo_path in enumerate(self.uploaded_photos):
                    def delete_photo(index=i):
                        if index < len(self.uploaded_photos):
                            photo_to_delete = self.uploaded_photos[index]
                            print(f"Deleting photo {index}: {photo_to_delete}")
                            self.uploaded_photos.pop(index)
                            print(f"Photo deleted, remaining photos: {self.uploaded_photos}")
                            self.update_photo_gallery()
                            ui.notify('Photo deleted', color='info', position='top')
                        else:
                            ui.notify('Failed to delete photo file', color='negative', position='top')

                    with ui.row().classes('items-center gap-2 q-mt-sm'):
                        ui.button('Delete', on_click=delete_photo, color='negative').props('dense size=sm')
            else:
                ui.label('No photos uploaded yet').classes('text-grey-6')

    async def handle_save(self):
        """Handle save button click"""
        try:
            def safe_int(value):
                """Safely convert value to int, return None if invalid"""
                if value is None or value == '' or value == 'None':
                    return None
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None

            # Convert date strings to date objects
            birthday_date = None
            if self.birthday_input.value:
                birthday_date = datetime.strptime(self.birthday_input.value, '%Y-%m-%d').date()
            
            breeding_lock_date_obj = None
            if self.breeding_lock_date_input.value:
                breeding_lock_date_obj = datetime.strptime(
                    self.breeding_lock_date_input.value, '%Y-%m-%d').date()
            
            death_date_obj = None
            if self.death_date_input.value:
                death_date_obj = datetime.strptime(self.death_date_input.value, '%Y-%m-%d').date()

            data = {
                'firstname': self.firstname_input.value,
                'surname': self.surname_input.value,
                'callname': self.callname_input.value.strip() if self.callname_input.value else None,
                'gender': self.gender_select.value,
                'birthday': birthday_date,
                'microchip': self.microchip_input.value.strip() if self.microchip_input.value else None,
                'colour': self.colour_input.value.strip() if self.colour_input.value else None,
                'litter': self.litter_input.value.strip() if self.litter_input.value else None,
                'haritage_number': self.haritage_input.value.strip() if self.haritage_input.value else None,
                'haritage_number_2': self.haritage_2_input.value.strip() if self.haritage_2_input.value else None,
                'eye_colour': self.eye_colour_select.value if self.eye_colour_select.value else None,
                'hair_type': self.hair_type_select.value if self.hair_type_select.value else None,
                'tests': self.tests_input.value.strip() if self.tests_input.value else None,
                'litter_size_male': (int(self.litter_size_male_input.value) 
                                    if self.litter_size_male_input.value else None),
                'litter_size_female': (int(self.litter_size_female_input.value) 
                                     if self.litter_size_female_input.value else None),
                'blood_group': self.blood_group_input.value.strip() if self.blood_group_input.value else None,
                'gencode': self.gencode_input.value.strip() if self.gencode_input.value else None,
                'features': self.features_textarea.value.strip() if self.features_textarea.value else None,
                'notes': self.notes_textarea.value.strip() if self.notes_textarea.value else None,
                'show_results': self.show_results_textarea.value.strip() if self.show_results_textarea.value else None,
                'description': self.description_textarea.value.strip() if self.description_textarea.value else None,
                'breeding_lock': self.breeding_lock_checkbox.value,
                'breeding_lock_date': breeding_lock_date_obj,
                'breeding_animal': self.breeding_animal_checkbox.value,
                'birth_country': self.birth_country_input.value.strip() if self.birth_country_input.value else None,
                'location': self.location_input.value.strip() if self.location_input.value else None,
                'weight': (float(self.weight_input.value) 
                          if self.weight_input.value else None),
                'birth_weight': (float(self.birth_weight_input.value) 
                               if self.birth_weight_input.value else None),
                'transfer_weight': (float(self.transfer_weight_input.value) 
                                  if self.transfer_weight_input.value else None),
                'faults_deviations': (self.faults_deviations_input.value.strip() 
                                     if self.faults_deviations_input.value else None),
                'association': (self.association_input.value.strip() 
                               if self.association_input.value else None),
                'jaw_fault': (self.jaw_fault_select.value 
                             if self.jaw_fault_select.value else None),
                'hernia': (self.hernia_select.value 
                          if self.hernia_select.value else None),
                'testicles': (self.testicles_select.value 
                             if self.testicles_select.value else None),
                'death_date': death_date_obj,
                'death_cause': (self.death_cause_input.value.strip() 
                               if self.death_cause_input.value else None),
                'status': (self.status_select.value 
                          if self.status_select.value else None),
                'kitten_transfer': self.kitten_transfer_checkbox.value,
                'wcf_sticker': self.wcf_sticker_input.value.strip() if self.wcf_sticker_input.value else None,
                'owner_id': (safe_int(self.owner_select.value) 
                            if self.owner_select else None),
                'breed_id': (safe_int(self.breeder_select.value) 
                           if self.breeder_select else None),
                'dam_id': (safe_int(self.dam_select.value) 
                          if self.dam_select else None),
                'sire_id': (safe_int(self.sire_select.value) 
                           if self.sire_select else None),
                'cat_photos': [photo for photo in self.uploaded_photos 
                              if photo and os.path.exists(photo)],
                'cat_files': [file for file in self.uploaded_files 
                             if file and os.path.exists(file)]
            }
            old_microchip = self.original_microchip
            new_microchip = data['microchip']
            print(f"Original microchip: '{old_microchip}'")
            print(f"New microchip: '{new_microchip}'")
            print(f"Microchip changed: {old_microchip != new_microchip}")
            print(f"Number of photos: {len(data['cat_photos'])}")
            if old_microchip != new_microchip and data['cat_photos']:
                print(f"Microchip changed from '{old_microchip}' to '{new_microchip}', updating photo paths in database")
                data['cat_photos'] = PhotoService.update_photo_paths_in_database(
                    data['cat_photos'], old_microchip, new_microchip
                )
            else:
                print("No photo path update needed")
            print(f"Saving cat with {len(data['cat_photos'])} photos: {data['cat_photos']}")
            success, message = await self.cat_service.update_cat(self.cat_id, data)
            if success:
                if old_microchip != new_microchip:
                    print(f"Microchip changed, ensuring photo directory is properly renamed")
                    PhotoService.ensure_photo_directory_renamed(old_microchip, new_microchip)
                    if self.uploaded_photos:
                        print(f"Updating uploaded_photos list with new paths")
                        self.uploaded_photos = PhotoService.update_photo_paths_in_database(
                            self.uploaded_photos, old_microchip, new_microchip
                        )
                        print(f"Updated uploaded_photos: {self.uploaded_photos}")
                    if self.uploaded_files:
                        print(f"Updating file paths in database")
                        self.uploaded_files = FileService.update_file_paths_in_database(
                            self.uploaded_files, old_microchip, new_microchip)
                        print(f"Updated uploaded_files: {self.uploaded_files}")
                    print(f"Microchip changed, ensuring file directory is properly renamed")
                    FileService.ensure_file_directory_renamed(old_microchip, new_microchip)
                ui.notify(message, type='positive')
                ui.navigate.to(f'/cat_profile/{self.cat_id}')
            else:
                ui.notify(message, type='negative')
        except Exception as e:
            ui.notify(f"Error saving cat: {str(e)}", type='error')

    async def handle_delete(self):
        """Handle delete button click"""
        try:
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


async def edit_cat_page_render(request: Request, cat_id: int):
    """Render edit cat page"""
    get_header('✏️ Edit Cat', request)
    page = EditCatPage(cat_id)
    if await page.load_data():
        page.create_form()
    else:
        ui.label('Loading failed').classes('text-center text-red-500')
