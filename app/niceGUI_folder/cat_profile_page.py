from nicegui import ui
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from datetime import datetime


def render_family_tree_node(cat_data, depth=0):
    """Render a family tree node recursively"""
    if not cat_data:
        return None
    
    with ui.card().classes(f'q-pa-md m-2 max-w-xs'):
        ui.label(f'{cat_data["firstname"]} {cat_data["surname"]}').classes('text-h6')
        ui.label(f'Gender: {cat_data["gender"]}').classes('text-caption')
        if cat_data["birthday"]:
            ui.label(f'Born: {cat_data["birthday"]}').classes('text-caption')
        if cat_data["microchip"]:
            ui.label(f'Chip: {cat_data["microchip"]}').classes('text-caption')
        
        # Add click handler to navigate to this cat's profile
        def navigate_to_cat():
            ui.navigate.to(f'/cat_profile/{cat_data["id"]}')
        
        ui.button('View Profile', on_click=navigate_to_cat).props('size=sm flat')


def render_family_tree(family_tree, depth=0):
    """Render the complete family tree"""
    if not family_tree:
        return
    
    with ui.row().classes('items-start justify-center'):
        # Render dam (mother) if exists
        if family_tree.get('dam'):
            with ui.column().classes('items-center'):
                ui.label('Mother').classes('text-caption text-weight-bold')
                render_family_tree_node(family_tree['dam'], depth + 1)
                # Render grandparents under mother
                if depth < 2 and (family_tree['dam'].get('dam') or family_tree['dam'].get('sire')):
                    with ui.row().classes('items-start justify-center q-mt-sm'):
                        if family_tree['dam'].get('dam'):
                            with ui.column().classes('items-center'):
                                ui.label('Grandmother').classes('text-caption text-weight-bold')
                                render_family_tree_node(family_tree['dam']['dam'], depth + 2)
                        if family_tree['dam'].get('sire'):
                            with ui.column().classes('items-center'):
                                ui.label('Grandfather').classes('text-caption text-weight-bold')
                                render_family_tree_node(family_tree['dam']['sire'], depth + 2)
        
        # Render the main cat
        with ui.column().classes('items-center mx-4'):
            ui.label('Cat').classes('text-caption text-weight-bold')
            render_family_tree_node(family_tree, depth)
        
        # Render sire (father) if exists
        if family_tree.get('sire'):
            with ui.column().classes('items-center'):
                ui.label('Father').classes('text-caption text-weight-bold')
                render_family_tree_node(family_tree['sire'], depth + 1)
                # Render grandparents under father
                if depth < 2 and (family_tree['sire'].get('dam') or family_tree['sire'].get('sire')):
                    with ui.row().classes('items-start justify-center q-mt-sm'):
                        if family_tree['sire'].get('dam'):
                            with ui.column().classes('items-center'):
                                ui.label('Grandmother').classes('text-caption text-weight-bold')
                                render_family_tree_node(family_tree['sire']['dam'], depth + 2)
                        if family_tree['sire'].get('sire'):
                            with ui.column().classes('items-center'):
                                ui.label('Grandfather').classes('text-caption text-weight-bold')
                                render_family_tree_node(family_tree['sire']['sire'], depth + 2)


async def cat_profile_page_render(cat_id: int):
    get_header('Cat Profile')
    
    # Get cat information with parents
    cat_info = await AsyncOrm.get_cat_with_parents(cat_id)
    
    if not cat_info:
        ui.label('Cat not found').classes('text-h6 text-center q-py-xl')
        return
    
    cat = cat_info['cat']
    owner = cat_info['owner']
    breed = cat_info['breed']
    dam = cat_info['dam']
    sire = cat_info['sire']
    
    with ui.column().classes('w-full items-center q-py-xl'):
        # Main cat information card
        with ui.card().classes('w-full max-w-4xl q-pa-lg'):
            ui.label(f'{cat.cat_firstname} {cat.cat_surname}').classes('text-h4 q-mb-md')
            
            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                # Basic information
                with ui.column():
                    ui.label('Basic Information').classes('text-h6 q-mb-sm')
                    ui.label(f'Gender: {cat.cat_gender}').classes('q-mb-xs')
                    ui.label(f'Birthday: {cat.cat_birthday}').classes('q-mb-xs')
                    ui.label(f'Microchip: {cat.cat_microchip_number}').classes('q-mb-xs')
                    ui.label(f'Colour: {cat.cat_EMS_colour or "Not specified"}').classes('q-mb-xs')
                    ui.label(f'Litter: {cat.cat_litter or "Not specified"}').classes('q-mb-xs')
                    ui.label(f'Heritage Number: {cat.cat_haritage_number or "Not specified"}').classes('q-mb-xs')
                
                # Owner and breed information
                with ui.column():
                    ui.label('Owner & Breed Information').classes('text-h6 q-mb-sm')
                    if owner:
                        ui.label(f'Owner: {owner.owner_firstname} {owner.owner_surname}').classes('q-mb-xs')
                        ui.label(f'Email: {owner.owner_email}').classes('q-mb-xs')
                        if owner.owner_phone:
                            ui.label(f'Phone: {owner.owner_phone}').classes('q-mb-xs')
                    if breed:
                        ui.label(f'Breeder: {breed.breed_firstname} {breed.breed_surname}').classes('q-mb-xs')
                        ui.label(f'Breeder Email: {breed.breed_email}').classes('q-mb-xs')
                        if breed.breed_phone:
                            ui.label(f'Breeder Phone: {breed.breed_phone}').classes('q-mb-xs')
        
        # Parents information
        if dam or sire:
            with ui.card().classes('w-full max-w-4xl q-pa-lg q-mt-md'):
                ui.label('Parents').classes('text-h6 q-mb-md')
                
                with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                    # Mother information
                    with ui.column():
                        ui.label('Mother (Dam)').classes('text-subtitle1 q-mb-sm')
                        if dam:
                            ui.label(f'Name: {dam.cat_firstname} {dam.cat_surname}').classes('q-mb-xs')
                            ui.label(f'Gender: {dam.cat_gender}').classes('q-mb-xs')
                            ui.label(f'Birthday: {dam.cat_birthday}').classes('q-mb-xs')
                            ui.label(f'Microchip: {dam.cat_microchip_number}').classes('q-mb-xs')
                            
                            def navigate_to_dam():
                                ui.navigate.to(f'/cat_profile/{dam.cat_id}')
                            
                            ui.button('View Dam Profile', on_click=navigate_to_dam).props('size=sm')
                        else:
                            ui.label('Not specified').classes('text-grey')
                    
                    # Father information
                    with ui.column():
                        ui.label('Father (Sire)').classes('text-subtitle1 q-mb-sm')
                        if sire:
                            ui.label(f'Name: {sire.cat_firstname} {sire.cat_surname}').classes('q-mb-xs')
                            ui.label(f'Gender: {sire.cat_gender}').classes('q-mb-xs')
                            ui.label(f'Birthday: {sire.cat_birthday}').classes('q-mb-xs')
                            ui.label(f'Microchip: {sire.cat_microchip_number}').classes('q-mb-xs')
                            
                            def navigate_to_sire():
                                ui.navigate.to(f'/cat_profile/{sire.cat_id}')
                            
                            ui.button('View Sire Profile', on_click=navigate_to_sire).props('size=sm')
                        else:
                            ui.label('Not specified').classes('text-grey')
        
        # Family tree
        with ui.card().classes('w-full max-w-6xl q-pa-lg q-mt-md'):
            ui.label('Family Tree').classes('text-h6 q-mb-md')
            
            # Get family tree data
            family_tree = await AsyncOrm.get_cat_family_tree(cat_id, max_depth=2)
            
            if family_tree:
                render_family_tree(family_tree)
            else:
                ui.label('No family tree data available').classes('text-grey')
        
        # Navigation buttons
        with ui.row().classes('q-mt-md'):
            ui.button('Back to Cats List', on_click=lambda: ui.navigate.to('/cats')).props('outline')
            ui.button('Edit Cat', on_click=lambda: ui.navigate.to(f'/edit_cat/{cat_id}')).props('outline')
