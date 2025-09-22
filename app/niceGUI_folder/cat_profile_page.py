from nicegui import ui
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.header import get_header
from app.niceGUI_folder.pdf_generator import generate_cat_pdf_file
from app.niceGUI_folder.photo_service import PhotoService
from app.niceGUI_folder.file_service import FileService
from app.niceGUI_folder.auth_service import AuthService
from fastapi import Request
from app.niceGUI_folder.auth_middleware import require_auth


def render_family_tree_node(cat_data, depth=0):
    """Render a family tree node recursively"""
    if not cat_data:
        return None
    
    with ui.card().classes('q-pa-sm m-1 max-w-40 min-h-32'):
        ui.label(f'{cat_data["firstname"]} {cat_data["surname"]}').classes('text-subtitle2 text-center q-mb-xs')
        ui.label(f'{cat_data["gender"]}').classes('text-caption text-center q-mb-xs')
        if cat_data["birthday"]:
            ui.label(f'{cat_data["birthday"]}').classes('text-caption text-center q-mb-xs')
        if cat_data["microchip"]:
            ui.label(f'{cat_data["microchip"]}').classes('text-caption text-center q-mb-xs')
        
        # Add click handler to navigate to this cat's profile
        def navigate_to_cat():
            ui.navigate.to(f'/cat_profile/{cat_data["id"]}')
        
        ui.button('View', on_click=navigate_to_cat).props('size=sm flat').classes('w-full')


def render_family_tree(family_tree, depth=0, max_depth=3, line_type="both"):
    """Render the family tree with configurable depth and line type"""
    if not family_tree:
        return
    
    # Create a container with proper alignment
    with ui.column().classes('w-full items-center'):
        with ui.row().classes('items-start justify-center w-full'):
            # Render maternal line
            if line_type in ["both", "maternal"] and family_tree.get('dam'):
                with ui.column().classes('items-center min-w-48'):
                    ui.label('Mother').classes('text-caption text-weight-bold q-mb-sm')
                    render_family_tree_node(family_tree['dam'], depth + 1)
                    
                    # Render maternal ancestors (grandparents)
                    if depth < max_depth and (family_tree['dam'].get('dam') or family_tree['dam'].get('sire')):
                        with ui.row().classes('items-start justify-center q-mt-sm gap-4'):
                            if family_tree['dam'].get('dam'):
                                with ui.column().classes('items-center min-w-32'):
                                    ui.label('Grandmother').classes('text-caption text-weight-bold q-mb-sm')
                                    render_family_tree_node(family_tree['dam']['dam'], depth + 2)
                                    
                                    # Render great-grandmother (3rd generation)
                                    if depth < max_depth - 1 and family_tree['dam']['dam'].get('dam'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandmother') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['dam']['dam']['dam'], depth + 3)
                                    
                                    # Render great-grandfather (3rd generation)
                                    if depth < max_depth - 1 and family_tree['dam']['dam'].get('sire'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandfather') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['dam']['dam']['sire'], depth + 3)
                            
                            if family_tree['dam'].get('sire'):
                                with ui.column().classes('items-center min-w-32'):
                                    ui.label('Grandfather').classes('text-caption text-weight-bold q-mb-sm')
                                    render_family_tree_node(family_tree['dam']['sire'], depth + 2)
                                    
                                    # Render great-grandmother (3rd generation)
                                    if depth < max_depth - 1 and family_tree['dam']['sire'].get('dam'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandmother') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['dam']['sire']['dam'], depth + 3)
                                    
                                    # Render great-grandfather (3rd generation)
                                    if depth < max_depth - 1 and family_tree['dam']['sire'].get('sire'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandfather') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['dam']['sire']['sire'], depth + 3)
            
            # Render the main cat
            with ui.column().classes('items-center mx-8 min-w-48'):
                ui.label('Cat').classes('text-caption text-weight-bold q-mb-sm')
                render_family_tree_node(family_tree, depth)
            
            # Render paternal line
            if line_type in ["both", "paternal"] and family_tree.get('sire'):
                with ui.column().classes('items-center min-w-48'):
                    ui.label('Father').classes('text-caption text-weight-bold q-mb-sm')
                    render_family_tree_node(family_tree['sire'], depth + 1)
                    
                    # Render paternal ancestors (grandparents)
                    if depth < max_depth and (family_tree['sire'].get('dam') or family_tree['sire'].get('sire')):
                        with ui.row().classes('items-start justify-center q-mt-sm gap-4'):
                            if family_tree['sire'].get('dam'):
                                with ui.column().classes('items-center min-w-32'):
                                    ui.label('Grandmother').classes('text-caption text-weight-bold q-mb-sm')
                                    render_family_tree_node(family_tree['sire']['dam'], depth + 2)
                                    
                                    # Render great-grandmother (3rd generation)
                                    if depth < max_depth - 1 and family_tree['sire']['dam'].get('dam'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandmother') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['sire']['dam']['dam'], depth + 3)
                                    
                                    # Render great-grandfather (3rd generation)
                                    if depth < max_depth - 1 and family_tree['sire']['dam'].get('sire'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandfather') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['sire']['dam']['sire'], depth + 3)
                            
                            if family_tree['sire'].get('sire'):
                                with ui.column().classes('items-center min-w-32'):
                                    ui.label('Grandfather').classes('text-caption text-weight-bold q-mb-sm')
                                    render_family_tree_node(family_tree['sire']['sire'], depth + 2)
                                    
                                    # Render great-grandmother (3rd generation)
                                    if depth < max_depth - 1 and family_tree['sire']['sire'].get('dam'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandmother') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['sire']['sire']['dam'], depth + 3)
                                    
                                    # Render great-grandfather (3rd generation)
                                    if depth < max_depth - 1 and family_tree['sire']['sire'].get('sire'):
                                        with ui.column().classes('items-center min-w-24 q-mt-sm'):
                                            ui.label('Great-Grandfather') \
                                                .classes('text-caption text-weight-bold q-mb-sm')
                                            render_family_tree_node(family_tree['sire']['sire']['sire'], depth + 3)


async def cat_profile_page_render(request: Request, cat_id: int):
    # Get user from session
    from app.niceGUI_folder.session_manager import SessionManager
    session_id = request.cookies.get("session_id")
    current_user = None
    if session_id:
        current_user = SessionManager.get_current_user(session_id)
    
    get_header('Cat Profile', request)
    
    # Get cat information with parents
    cat_info = await AsyncOrm.get_cat_with_parents(cat_id)
    
    if not cat_info:
        ui.label('Cat not found').classes('text-h6 text-center q-py-xl')
        return
    
    cat = cat_info['cat']
    
    # Check if user can view this cat
    if not AuthService.can_view_cat(current_user, cat.owner_id):
        ui.label('You do not have permission to view this cat').classes('text-h6 text-center q-py-xl text-red-500')
        return
    owner = cat_info['owner']
    breed = cat_info['breed']
    dam = cat_info['dam']
    sire = cat_info['sire']
    
    with ui.column().classes('w-full items-center q-py-xl'):
        # Main cat information card
        with ui.card().classes('w-full max-w-4xl q-pa-lg'):
            with ui.row().classes('justify-between items-center q-mb-md'):
                ui.label(f'{cat.cat_firstname} {cat.cat_surname}').classes('text-h4')
                
                # Quick PDF generation button
                async def quick_generate_pdf():
                    try:
                        ui.notify('Generating PDF...', color='info', position='top')
                        
                        # Get full family tree for PDF
                        full_tree = await AsyncOrm.get_cat_family_tree(cat_id, max_depth=10)
                        
                        # Generate PDF
                        output_path, filename = generate_cat_pdf_file(cat_info, full_tree)
                        
                        ui.notify(f'PDF generated successfully: {filename}', color='positive', position='top')
                        
                        # Create download link
                        with open(output_path, 'rb') as f:
                            pdf_content = f.read()
                        
                        ui.download(pdf_content, filename, 'application/pdf')
                        
                    except Exception as e:
                        ui.notify(f'Error generating PDF: {str(e)}', color='negative', position='top')
                
                ui.button('📄 Generate PDF', on_click=quick_generate_pdf, color='primary').props('icon=description')
            
            # Basic Information Section
            with ui.card().classes('w-full q-pa-md q-mb-md'):
                ui.label('🐱 Basic Information').classes('text-h6 q-mb-md')
                with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                    with ui.column():
                        ui.label(f'Name: {cat.cat_firstname} {cat.cat_surname}').classes('q-mb-xs')
                        ui.label(f'Callname: {cat.cat_callname or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Gender: {cat.cat_gender}').classes('q-mb-xs')
                        ui.label(f'Birthday: {cat.cat_birthday}').classes('q-mb-xs')
                        ui.label(f'Chip Number: {cat.cat_microchip_number or "Not specified"}').classes('q-mb-xs')
                    
                    with ui.column():
                        ui.label(f'Title: {cat.cat_title or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Studbook Number 1: {cat.cat_haritage_number or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Studbook Number 2: {cat.cat_haritage_number_2 or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Eye Color: {cat.cat_eye_colour or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Hair Type: {cat.cat_hair_type or "Not specified"}').classes('q-mb-xs')

            # Breed and Color Information
            with ui.card().classes('w-full q-pa-md q-mb-md'):
                ui.label('🎨 Breed & Color Information').classes('text-h6 q-mb-md')
                with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                    with ui.column():
                        ui.label(f'Color: {cat.cat_EMS_colour or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Litter: {cat.cat_litter or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Litter Size (Male): {cat.cat_litter_size_male or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Litter Size (Female): {cat.cat_litter_size_female or "Not specified"}').classes('q-mb-xs')
                    
                    with ui.column():
                        if breed:
                            ui.label(f'Breeder: {breed.breed_firstname} {breed.breed_surname}').classes('q-mb-xs')
                            ui.label(f'Breeder Email: {breed.breed_email}').classes('q-mb-xs')
                            if breed.breed_phone:
                                ui.label(f'Breeder Phone: {breed.breed_phone}').classes('q-mb-xs')
                        else:
                            ui.label('Breeder: Not specified').classes('q-mb-xs')

            # Health and Medical Information
            with ui.card().classes('w-full q-pa-md q-mb-md'):
                ui.label('🏥 Health & Medical Information').classes('text-h6 q-mb-md')
                with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                    with ui.column():
                        ui.label(f'Tests: {cat.cat_tests or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Blood Group: {cat.cat_blood_group or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Gencode: {cat.cat_gencode or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Weight: {cat.cat_weight or "Not specified"} kg').classes('q-mb-xs')
                        ui.label(f'Birth Weight: {cat.cat_birth_weight or "Not specified"} g').classes('q-mb-xs')
                    
                    with ui.column():
                        ui.label(f'Transfer Weight: {cat.cat_transfer_weight or "Not specified"} g').classes('q-mb-xs')
                        ui.label(f'Jaw Fault: {cat.cat_jaw_fault or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Hernia: {cat.cat_hernia or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Testicles: {cat.cat_testicles or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Faults/Deviations: {cat.cat_faults_deviations or "Not specified"}').classes('q-mb-xs')

            # Breeding Information
            with ui.card().classes('w-full q-pa-md q-mb-md'):
                ui.label('🐾 Breeding Information').classes('text-h6 q-mb-md')
                with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                    with ui.column():
                        ui.label(f'Breeding Lock: {"Yes" if cat.cat_breeding_lock else "No"}').classes('q-mb-xs')
                        ui.label(f'Breeding Lock Date: {cat.cat_breeding_lock_date or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Breeding Animal: {"Yes" if cat.cat_breeding_animal else "No"}').classes('q-mb-xs')
                        ui.label(f'Kitten Transfer: {"Yes" if cat.cat_kitten_transfer else "No"}').classes('q-mb-xs')
                    
                    with ui.column():
                        ui.label(f'WCF Sticker: {cat.wcf_sticker or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Birth Country: {cat.cat_birth_country or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Location: {cat.cat_location or "Not specified"}').classes('q-mb-xs')
                        ui.label(f'Association: {cat.cat_association or "Not specified"}').classes('q-mb-xs')

            # Death Information
            if cat.cat_death_date or cat.cat_death_cause or cat.cat_status:
                with ui.card().classes('w-full q-pa-md q-mb-md'):
                    ui.label('💀 Death Information').classes('text-h6 q-mb-md')
                    with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                        with ui.column():
                            ui.label(f'Death Date: {cat.cat_death_date or "Not specified"}').classes('q-mb-xs')
                            ui.label(f'Death Cause: {cat.cat_death_cause or "Not specified"}').classes('q-mb-xs')
                            ui.label(f'Status: {cat.cat_status or "Not specified"}').classes('q-mb-xs')

            # Owner Information
            with ui.card().classes('w-full q-pa-md q-mb-md'):
                ui.label('👤 Owner Information').classes('text-h6 q-mb-md')
                if owner:
                    with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                        with ui.column():
                            ui.label(f'Owner: {owner.owner_firstname} {owner.owner_surname}').classes('q-mb-xs')
                            ui.label(f'Email: {owner.owner_email}').classes('q-mb-xs')
                            if owner.owner_phone:
                                ui.label(f'Phone: {owner.owner_phone}').classes('q-mb-xs')
                        with ui.column():
                            if owner.owner_address:
                                ui.label(f'Address: {owner.owner_address}').classes('q-mb-xs')
                            if owner.owner_city:
                                ui.label(f'City: {owner.owner_city}').classes('q-mb-xs')
                            if owner.owner_country:
                                ui.label(f'Country: {owner.owner_country}').classes('q-mb-xs')
                            if owner.owner_zip:
                                ui.label(f'ZIP: {owner.owner_zip}').classes('q-mb-xs')
                else:
                    ui.label('Owner: Not specified').classes('q-mb-xs')

            # Additional Information
            if cat.cat_features or cat.cat_notes or cat.cat_show_results or cat.cat_description:
                with ui.card().classes('w-full q-pa-md q-mb-md'):
                    ui.label('📝 Additional Information').classes('text-h6 q-mb-md')
                    if cat.cat_features:
                        ui.label('Features:').classes('text-subtitle2 q-mb-xs')
                        ui.label(cat.cat_features).classes('q-mb-md')
                    if cat.cat_notes:
                        ui.label('Notes:').classes('text-subtitle2 q-mb-xs')
                        ui.label(cat.cat_notes).classes('q-mb-md')
                    if cat.cat_show_results:
                        ui.label('Show Results:').classes('text-subtitle2 q-mb-xs')
                        ui.label(cat.cat_show_results).classes('q-mb-md')
                    if cat.cat_description:
                        ui.label('Description:').classes('text-subtitle2 q-mb-xs')
                        ui.label(cat.cat_description).classes('q-mb-md')
        
        # Photos section
        if cat.cat_photos and len(cat.cat_photos) > 0:
            with ui.card().classes('w-full max-w-4xl q-pa-lg q-mt-md'):
                ui.label('📸 Photos').classes('text-h6 q-mb-md')
                print(f"Cat photos: {cat.cat_photos}")
                PhotoService.create_photo_gallery(cat.cat_photos, "400px")
        
        # Files section
        if cat.cat_files and len(cat.cat_files) > 0:
            with ui.card().classes('w-full max-w-4xl q-pa-lg q-mt-md'):
                ui.label('📁 Files').classes('text-h6 q-mb-md')
                print(f"Cat files: {cat.cat_files}")
                FileService.create_file_list(cat.cat_files, "400px")
        
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
            
            # Family tree controls
            with ui.row().classes('q-mb-md'):
                # Depth selector
                depth_selector = ui.select(
                    {1: '1 Generation', 2: '2 Generations', 3: '3 Generations', 
                     4: '4 Generations', 5: '5 Generations'},
                    value=3,
                    label='Tree Depth'
                ).props('outlined dense').classes('q-mr-md')
                
                # Line type selector
                line_selector = ui.select(
                    {'both': 'Both Lines', 'maternal': 'Maternal Line Only', 'paternal': 'Paternal Line Only'},
                    value='both',
                    label='Family Line'
                ).props('outlined dense').classes('q-mr-md')
                
                # Refresh button
                refresh_btn = ui.button('Refresh Tree', color='primary').props('outlined')
            
            # Family tree container
            tree_container = ui.column().classes('w-full')
            
            async def update_family_tree():
                tree_container.clear()
                with tree_container:
                    # Get family tree data with selected depth
                    max_depth = depth_selector.value
                    line_type = line_selector.value
                    family_tree = await AsyncOrm.get_cat_family_tree(cat_id, max_depth=max_depth)
                    
                    if family_tree:
                        render_family_tree(family_tree, max_depth=max_depth, line_type=line_type)
                    else:
                        ui.label('No family tree data available').classes('text-grey')
            
            # Set up event handlers
            depth_selector.on('change', update_family_tree)
            line_selector.on('change', update_family_tree)
            refresh_btn.on('click', update_family_tree)
            
            # Initial load
            await update_family_tree()
        
        # Ancestors list
        with ui.card().classes('w-full max-w-4xl q-pa-lg q-mt-md'):
            ui.label('Complete Ancestors List').classes('text-h6 q-mb-md')
            
            # Get full family tree for list view
            full_tree = await AsyncOrm.get_cat_family_tree(cat_id, max_depth=10)
            
            if full_tree:
                ancestors_dict = {}  # Use dict to avoid duplicates
                
                def collect_ancestors(node, generation=0):
                    if not node:
                        return
                    
                    # Only add if not already in dict (avoid duplicates)
                    if node['id'] not in ancestors_dict:
                        ancestors_dict[node['id']] = {
                            'generation': generation,
                            'name': f"{node['firstname']} {node['surname']}",
                            'gender': node['gender'],
                            'birthday': node['birthday'],
                            'microchip': node['microchip'],
                            'id': node['id']
                        }
                    
                    if node.get('dam'):
                        collect_ancestors(node['dam'], generation + 1)
                    if node.get('sire'):
                        collect_ancestors(node['sire'], generation + 1)
                
                collect_ancestors(full_tree)
                
                # Convert to list and sort by generation
                ancestors_list = list(ancestors_dict.values())
                ancestors_list.sort(key=lambda x: x['generation'])
                
                # Display ancestors by generation
                current_generation = -1
                for ancestor in ancestors_list:
                    if ancestor['generation'] != current_generation:
                        current_generation = ancestor['generation']
                        if current_generation == 0:
                            ui.label(f'Generation {current_generation + 1}: Main Cat') \
                                .classes('text-subtitle1 q-mt-md q-mb-sm')
                        else:
                            ui.label(f'Generation {current_generation + 1}: Ancestors') \
                                .classes('text-subtitle1 q-mt-md q-mb-sm')
                    
                    with ui.row().classes('q-mb-xs'):
                        def navigate_to_ancestor(ancestor_id=ancestor['id']):
                            ui.navigate.to(f'/cat_profile/{ancestor_id}')
                        
                        ui.button(
                            f"{ancestor['name']} ({ancestor['gender']}) - {ancestor['birthday']}",
                            on_click=navigate_to_ancestor
                        ).props('flat size=sm')
            else:
                ui.label('No ancestors data available').classes('text-grey')
        
        # Navigation buttons
        with ui.row().classes('q-mt-md'):
            ui.button('Back to Cats List', on_click=lambda: ui.navigate.to('/cats')).props('outline')
            
            # Edit button only for admins
            if current_user and current_user.get('owner_permission') == 1:
                ui.button('Edit Cat', on_click=lambda: ui.navigate.to(f'/edit_cat/{cat_id}')).props('outline')
            
            # PDF Generation button
            async def generate_pdf():
                try:
                    ui.notify('Generating PDF...', color='info', position='top')
                    
                    # Get full family tree for PDF
                    full_tree = await AsyncOrm.get_cat_family_tree(cat_id, max_depth=10)
                    
                    # Generate PDF
                    output_path, filename = generate_cat_pdf_file(cat_info, full_tree)
                    
                    ui.notify(f'PDF generated successfully: {filename}', color='positive', position='top')
                    
                    # Create download link
                    with open(output_path, 'rb') as f:
                        pdf_content = f.read()
                    
                    ui.download(pdf_content, filename, 'application/pdf')
                    
                except Exception as e:
                    ui.notify(f'Error generating PDF: {str(e)}', color='negative', position='top')
            
            ui.button('Generate PDF Report', on_click=generate_pdf, color='primary').props('outline')
