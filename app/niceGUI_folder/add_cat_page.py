from nicegui import ui
from pydantic import ValidationError
# from app.niceGUI_folder.pydentic_models import CatCreate
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from datetime import datetime
# import geonamescache


async def add_cat_page_render():
    get_header('Add Cat Page')

    # gc = geonamescache.GeonamesCache()
    # cities = gc.get_cities()
    # city_list = [c['name'] for c in cities.values() if c['countrycode'] == 'DE'] 

    _, owners = await AsyncOrm.get_owner()
    owner_map = {
         o['owner_id']: f'{o["owner_firstname"]} {o["owner_surname"]}'
         for o in owners
    }
    _, cats_female = await AsyncOrm.get_cat(cat_gender="Female")
    cats_female = [
        f'{cat["cat_firstname"]} {cat["cat_surname"]} {cat["cat_gender"]} {cat["cat_microchip_number"]}' 
        for cat in cats_female
    ]
    _, cats_male = await AsyncOrm.get_cat(cat_gender="Male")
    cats_male = [
        f'{cat["cat_firstname"]} {cat["cat_surname"]} {cat["cat_gender"]} {cat["cat_microchip_number"]}' 
        for cat in cats_male
    ]

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
                breed = ui.input(label='Cat Breed').props('outlined dense').classes('w-full')
                colour = ui.input(label='Cat Colour').props('outlined dense').classes('w-full')

                litter = ui.input(label='Cat Litter').props('outlined dense').classes('w-full')
                haritage_number = ui.input(label='Cat Haritage Number').props('outlined dense').classes('w-full')
                owner = ui.select(dict(owner_map), label='Owner').props('outlined dense').classes('w-full')

            with ui.row().classes('justify-end q-pt-md'):
                submit_btn = ui.button('SUBMIT', color='primary').props('unelevated')

            async def handle_submit():
                try:
                    # Проверяем, что все обязательные поля заполнены
                    if not firstname.value or not surname.value or not microchip.value or not owner.value:
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
                                           owner_id=owner.value
                                           )
                    ui.notify('Cat added successfully!', color='positive', position='top')
                    ui.navigate.to('/cats')
                except ValidationError as e:
                    msg = '; '.join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
                    ui.notify(msg, color='negative', position='top')
                except Exception as e:
                    ui.notify(f'Error adding cat: {str(e)}', color='negative', position='top')

            submit_btn.on('click', handle_submit)
