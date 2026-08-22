import json
import re
from pathlib import Path
from nicegui import ui
from identifiers import load_identifiers

BASE_DIR = Path(__file__).resolve().parents[0]

aikatsuList = load_identifiers('aikatsu')
starsList = load_identifiers('stars')
friendsList = load_identifiers('friends')
paradeList = load_identifiers('parade')
planetList = load_identifiers('planet')
encoreList = load_identifiers('encore')

def write_save(saveFile, savePath):
    json_string = json.dumps(saveFile, indent = 4)

    flattened_json = re.sub(
        r'\[[^\]]*?\]', 
        lambda m: m.group(0).replace("\n", "").replace(" ", ""), 
        json_string
    )
    with open(savePath, 'w') as f:
        f.write(flattened_json)

    ui.notify('Collection saved')

def mainUI(headerText, isSettings=False, isCardDB=False, drawer=None, editMode=False, refreshCallback=None, saveFile=None, savePath=None):
    ui.add_head_html("""
        <style>
        html, body {
        overflow: hidden;
        height: 100%;
        margin: 0;
        }
        </style>
        """)

    with ui.header(elevated=True).style('position:relative; display:flex; justify-content:center; align-items:center; min-height: 52px; padding: 0 16px;') as mainHeader:
        if ui.context.client.page.path != "/":
            with ui.row().style('position:absolute; left:16px; top:50%; transform:translateY(-50%); gap: 8px;') as homeButton:
                with ui.button(on_click=lambda: ui.navigate.to('/')).props('elevated') as home:
                    edit_icon = ui.icon('home')
                    edit_tooltip = ui.tooltip('Home').props('position-bottom')
        
        ui.label(headerText).style('font-size: 24px; margin: 0;')
        with ui.row().style('position:absolute; right:16px; top:50%; transform:translateY(-50%); gap: 8px;') as headerButtons:

            def toggle_edit_mode():
                was_editing = editMode['value']

                editMode['value'] = not editMode['value']

                if was_editing and not editMode['value']:
                    if editMode['dirty']:
                        write_save(saveFile, savePath)
                        editMode['dirty'] = False

                if editMode['value']:
                    edit_icon.name = 'save'
                    edit_tooltip.text = 'Turn off Edit Mode (Save changes)'
                else:
                    edit_icon.name = 'edit'
                    edit_tooltip.text = 'Turn on Edit Mode'

                if refreshCallback:
                    refreshCallback()

            if isCardDB:
                with ui.button(on_click=toggle_edit_mode).props('elevated') as edit:
                    edit_icon = ui.icon('edit')
                    edit_tooltip = ui.tooltip('Turn on Edit Mode').props('position-bottom')


                with ui.button(on_click=lambda: drawer.toggle()).props('elevated') as filter:
                    ui.icon('filter_list')
                    ui.tooltip('Filter Cards').props('position-bottom')

            with ui.button(on_click=lambda: ui.navigate.to('/scanCard')).props('elevated') as QrCode:
                ui.icon('qr_code_scanner')
                ui.tooltip('Scan QR Code').props('position-bottom')

            with ui.button().props('elevated') as profileButton:
                ui.icon('account_circle')
                ui.tooltip('View Profile').props('position-bottom')

            with ui.button().props('elevated') as settingsButton:
                ui.icon('settings')
                ui.tooltip('Settings').props('position-bottom')

    if not isSettings:
        with ui.left_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as leftDrawer:
            with ui.row().classes('items-center').style('padding: 16px;'):
                ui.label('Card Database').style('font-size: 20px; font-weight: bold;')
                with ui.expansion('Aikatsu!').style('width: 220px;'):
                    for i in aikatsuList:
                        clean_i = i.replace(' ', '-').lower()
                        ui.button(i, on_click=lambda clean_i=clean_i: ui.navigate.to(f'/aikatsu/{clean_i}')).props('flat').style('text-align: left;')

                with ui.expansion('Aikatsu Stars!').style('width: 220px;'):
                    for i in starsList:
                        clean_i = i.replace(' ', '-').lower()
                        ui.button(i, on_click=lambda clean_i=clean_i: ui.navigate.to(f'/stars/{clean_i}')).props('flat').style('text-align: left;')

                with ui.expansion('Aikatsu Friends!').style('width: 220px;'):
                    for i in friendsList:
                        clean_i = i.replace(' ', '-').lower()
                        ui.button(i, on_click=lambda clean_i=clean_i: ui.navigate.to(f'/friends/{clean_i}')).props('flat').style('text-align: left;')

                with ui.expansion('Aikatsu on Parade!').style('width: 220px;'):
                    for i in paradeList:
                        clean_i = i.replace(' ', '-').lower()
                        ui.button(i, on_click=lambda clean_i=clean_i: ui.navigate.to(f'/parade/{clean_i}')).props('flat').style('text-align: left;')

                with ui.expansion('Aikatsu Planet!').style('width: 220px;'):
                    for i in planetList:
                        clean_i = i.replace(' ', '-').lower()
                        ui.button(i, on_click=lambda clean_i=clean_i: ui.navigate.to(f'/planet/{clean_i}')).props('flat').style('text-align: left;')

                # with ui.expansion('Aikatsu Encore!').style('width: 220px;'):
                #     for i in encoreList:
                #         clean_i = i.replace(' ', '-').lower()
