from nicegui import ui
from pydantic import ValidationError
# from app.niceGUI_folder.pydentic_models import CatCreate
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.photo_service import PhotoService
from app.niceGUI_folder.file_service import FileService
from datetime import datetime
# import geonamescache


async def add_cat_page_render():
    get_header('Add Cat Page')
    
    # Store uploaded photos and files
    uploaded_photos = []
    uploaded_files = []

    # gc = geonamescache.GeonamesCache()
    # cities = gc.get_cities()
    # city_list = [c['name'] for c in cities.values() if c['countrycode'] == 'DE'] 

    _, owners = await AsyncOrm.get_owner()
    owner_map = {
         o['owner_id']: f'{o["owner_firstname"]} {o["owner_surname"]}'
         for o in owners
    }
    
    _, breeds = await AsyncOrm.get_breed()
    breed_map = {
         b['breed_id']: f'{b["breed_firstname"]} {b["breed_surname"]}'
         for b in breeds
    } if breeds else {}
    # Get female cats for dam selection
    _, cats_female = await AsyncOrm.get_cat(cat_gender="Female")
    dam_map = {
        cat["cat_id"]: f'{cat["cat_firstname"]} {cat["cat_surname"]} ({cat["cat_microchip_number"]})'
        for cat in cats_female
    } if cats_female else {}
    
    # Get male cats for sire selection
    _, cats_male = await AsyncOrm.get_cat(cat_gender="Male")
    sire_map = {
        cat["cat_id"]: f'{cat["cat_firstname"]} {cat["cat_surname"]} ({cat["cat_microchip_number"]})'
        for cat in cats_male
    } if cats_male else {}

    with ui.column().classes('w-full items-center q-py-xl'):
        with ui.card().classes('w-full max-w-2xl q-pa-lg'):
            ui.label('Add a new cat').classes('text-h6 q-mb-md')

            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                firstname = ui.input(label='Cat Firstname').props('outlined dense').classes('w-full')
                surname = ui.input(label='Cat Surname').props('outlined dense').classes('w-full')

                gender = ui.select(['Male', 'Female'], label='Cat Gender') \
                    .props('outlined dense') \
                    .classes('w-full')
                birthday = ui.input(label='Cat Birthday') \
                    .props('type=date outlined dense') \
                    .classes('w-full')
                microchip = ui.input(label='Cat Microchip Number') \
                    .props('outlined dense') \
                    .classes('w-full md:col-span-2')
                breed = ui.select(dict(breed_map), label='Cat Breed').props('outlined dense').classes('w-full')
                add_breed_btn = ui.button('Add New Breed', on_click=lambda: ui.navigate.to('/add_breed'))
                add_breed_btn.props('flat size=sm').classes('q-mt-xs')
                colour = ui.input(label='Cat Colour').props('outlined dense').classes('w-full')

                litter = ui.input(label='Cat Litter').props('outlined dense').classes('w-full')
                haritage_number = ui.input(label='Cat Haritage Number').props('outlined dense').classes('w-full')
                owner = ui.select(dict(owner_map), label='Owner').props('outlined dense').classes('w-full')
                add_owner_btn = ui.button('Add New Owner', on_click=lambda: ui.navigate.to('/add_owner'))
                add_owner_btn.props('flat size=sm').classes('q-mt-xs')
                
                # Parent selection fields
                dam = ui.select(dict(dam_map), label='Dam (Mother)') \
                    .props('outlined dense clearable').classes('w-full')
                sire = ui.select(dict(sire_map), label='Sire (Father)') \
                    .props('outlined dense clearable').classes('w-full')

            # Photos section
            ui.separator().classes('q-my-md')
            ui.label('Photos').classes('text-h6 q-mb-md')
            
            # Photo upload area
            photo_container = ui.column().classes('w-full')
            
            def handle_photo_upload(e):
                """Handle photo upload"""
                try:
                    # Validate photo (without size check since we'll compress if needed)
                    is_valid, error_msg = PhotoService.is_valid_photo(e.name)
                    if not is_valid:
                        ui.notify(error_msg, color='negative', position='top')
                        return
                    
                    # Save photo (with automatic compression)
                    microchip_value = microchip.value if microchip.value else None
                    photo_path = PhotoService.save_photo(e.content.read(), e.name, microchip_value)
                    if photo_path:
                        uploaded_photos.append(photo_path)
                        update_photo_gallery()
                        ui.notify(f'Photo "{e.name}" uploaded successfully!', color='positive', position='top')
                    else:
                        ui.notify('Failed to save photo', color='negative', position='top')
                        
                except Exception as ex:
                    ui.notify(f'Error uploading photo: {str(ex)}', color='negative', position='top')
            
            def update_photo_gallery():
                """Update photo gallery display"""
                photo_container.clear()
                with photo_container:
                    if uploaded_photos:
                        ui.label(f'Uploaded photos ({len(uploaded_photos)}):').classes('text-subtitle2 q-mb-sm')
                        PhotoService.create_photo_gallery(uploaded_photos, "300px")
                        
                        # Add delete buttons for each photo
                        for i, photo_path in enumerate(uploaded_photos):
                            def delete_photo(index=i):
                                if PhotoService.delete_photo(uploaded_photos[index]):
                                    uploaded_photos.pop(index)
                                    update_photo_gallery()
                                    ui.notify('Photo deleted', color='info', position='top')
                                else:
                                    ui.notify('Failed to delete photo', color='negative', position='top')
                            
                            with ui.row().classes('items-center gap-2 q-mt-sm'):
                                ui.button('Delete', on_click=delete_photo, color='negative').props('dense size=sm')
                    else:
                        ui.label('No photos uploaded yet').classes('text-grey-6')
            
            # Upload widget
            ui.upload(
                on_upload=handle_photo_upload,
                auto_upload=True,
                max_file_size=PhotoService.MAX_FILE_SIZE
            ).props('accept=image/*').classes('w-full q-mb-md')
            
            # Initial gallery display
            update_photo_gallery()
        
        # Files section
        with ui.card().classes('w-full q-pa-md'):
            ui.label('Files').classes('text-h6 q-mb-md')
            
            # File upload area
            file_container = ui.column().classes('w-full')
            
            def handle_file_upload(e):
                """Handle file upload"""
                try:
                    # Validate file
                    is_valid, error_msg = FileService.is_valid_file(e)
                    if not is_valid:
                        ui.notify(error_msg, color='negative', position='top')
                        return
                    
                    # Save file (we need microchip, but it might not be set yet)
                    if not microchip.value:
                        ui.notify('Please enter microchip number before uploading files', color='negative', position='top')
                        return
                    
                    success, message, file_path = FileService.save_file(microchip.value, e)
                    if success:
                        uploaded_files.append(file_path)
                        update_file_list()
                        ui.notify(f'File uploaded: {e.name}', color='positive', position='top')
                    else:
                        ui.notify(f'Error uploading file: {message}', color='negative', position='top')
                        
                except Exception as ex:
                    ui.notify(f'Error uploading file: {str(ex)}', color='negative', position='top')
            
            def update_file_list():
                """Update file list display"""
                file_container.clear()
                with file_container:
                    if uploaded_files:
                        ui.label(f'Uploaded files ({len(uploaded_files)}):').classes('text-subtitle2 q-mb-sm')
                        FileService.create_file_list(uploaded_files, "300px")
                        
                        # Add delete buttons for each file
                        for i, file_path in enumerate(uploaded_files):
                            def delete_file(index=i):
                                if FileService.delete_file(uploaded_files[index]):
                                    uploaded_files.pop(index)
                                    update_file_list()
                                    ui.notify('File deleted', color='info', position='top')
                                else:
                                    ui.notify('Failed to delete file', color='negative', position='top')
                            
                            with ui.row().classes('items-center gap-2 q-mt-sm'):
                                ui.button('Delete', on_click=delete_file, color='negative').props('dense size=sm')
                    else:
                        ui.label('No files uploaded yet').classes('text-grey-6')
            
            # Upload widget
            ui.upload(
                on_upload=handle_file_upload,
                auto_upload=True,
                max_file_size=FileService.MAX_FILE_SIZE
            ).props('accept=.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.zip,.rar').classes('w-full q-mb-md')
            
            # Initial file list display
            update_file_list()

            with ui.row().classes('justify-end q-pt-md'):
                submit_btn = ui.button('SUBMIT', color='primary').props('unelevated')

            async def handle_submit():
                try:
                    # Проверяем, что все обязательные поля заполнены
                    required_fields = [
                        firstname.value, surname.value, microchip.value, 
                        owner.value, breed.value
                    ]
                    if not all(required_fields):
                        ui.notify('Please fill in all required fields', color='negative', position='top')
                        return

                    # Проверяем формат даты
                    if not birthday.value:
                        ui.notify('Please select a birthday', color='negative', position='top')
                        return

                    await AsyncOrm.add_cat(cat_firstname=firstname.value,
                                           cat_surname=surname.value,
                                           cat_gender=gender.value,
                                           cat_birthday=datetime.strptime(birthday.value, '%Y-%m-%d').date(),
                                           cat_microchip_number=microchip.value,
                                           cat_breed_id=breed.value,
                                           cat_EMS_colour=colour.value,
                                           cat_litter=litter.value,
                                           cat_haritage_number=haritage_number.value,
                                           owner_id=owner.value,
                                           cat_dam_id=dam.value,
                                           cat_sire_id=sire.value,
                                           cat_photos=uploaded_photos,
                                           cat_files=uploaded_files
                                           )
                    ui.notify('Cat added successfully!', color='positive', position='top')
                    ui.navigate.to('/cats')
                except ValidationError as e:
                    msg = '; '.join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
                    ui.notify(msg, color='negative', position='top')
                except Exception as e:
                    ui.notify(f'Error adding cat: {str(e)}', color='negative', position='top')

            submit_btn.on('click', handle_submit)
