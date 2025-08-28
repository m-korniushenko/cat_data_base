from nicegui import ui
from pydantic import ValidationError
from app.niceGUI_folder.pydentic_models import CatCreate
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from datetime import datetime


async def add_cat_page_render():
    get_header('Add Cat Page')
    len, country_city = await AsyncOrm.get_country_city()
    cities = [city["country_city_name"] for city in country_city]
    len, owners = await AsyncOrm.get_owner()
    owner_map = {
         o['owner_id']: f'{o["owner_firstname"]} {o["owner_surname"]}'
         for o in owners
    }
    len, cats_female = await AsyncOrm.get_cat(cat_gender="Female")
    cats_female = [f'{cat["cat_firstname"]} {cat["cat_surname"]} {cat["cat_gender"]} {cat["cat_microchip_number"]}' for cat in cats_female]
    len, cats_male = await AsyncOrm.get_cat(cat_gender="Male")
    cats_male = [f'{cat["cat_firstname"]} {cat["cat_surname"]} {cat["cat_gender"]} {cat["cat_microchip_number"]}' for cat in cats_male]


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
                ifc = ui.input(label='Cat IFC').props('outlined dense').classes('w-full')
                country_city = ui.select(cities, label='Country, City').props('outlined dense').classes('w-full')
                owner = ui.select(dict(owner_map), label='Owner').props('outlined dense').classes('w-full')
                # cat_female = ui.select(cats_female, label='Cat Female').props('outlined dense').classes('w-full')
                # cat_male = ui.select(cats_male, label='Cat Male').props('outlined dense').classes('w-full')

            with ui.row().classes('justify-end q-pt-md'):
                submit_btn = ui.button('SUBMIT', color='primary').props('unelevated')

            async def handle_submit():
                try:
                    await AsyncOrm.add_cat(cat_firstname=firstname.value,
                                           cat_surname=surname.value,
                                           cat_gender=gender.value,
                                           cat_birthday=datetime.strptime(birthday.value, '%Y-%m-%d').date(),
                                           cat_microchip_number=microchip.value,
                                           cat_breed=breed.value,
                                           cat_colour=colour.value,
                                           cat_litter=litter.value,
                                           cat_ifc=ifc.value,
                                           owner_id=owner.value
                                           )
                    ui.notify('Cat added')
                    ui.navigate.to('/cats')
                except ValidationError as e:
                    msg = '; '.join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
                    ui.notify(msg, color='negative', position='top')

            submit_btn.on('click', handle_submit)
