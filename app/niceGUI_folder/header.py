from nicegui import ui


def get_header(label_text: str):
    with ui.header().classes('bg-blue-500 text-white'):
        ui.label(label_text).classes('text-h6 q-ml-md')
        with ui.row().classes('q-ml-auto q-mr-md'):
            ui.button('Cats', on_click=lambda: ui.navigate.to('/cats')).classes('q-mr-sm')
            ui.button('Owners', on_click=lambda: ui.navigate.to('/owners')).classes('q-mr-sm')
            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/')).classes('q-mr-sm')