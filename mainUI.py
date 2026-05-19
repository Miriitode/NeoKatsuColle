from nicegui import ui
import json
from identifiers import load_identifiers

ogkatsuList, starsList, friendsList, paradeList, planetList, encoreList, brands, types = load_identifiers()

def mainUI(headerText):
    ui.add_head_html("""
        <style>
        html, body {
        overflow: hidden;
        height: 100%;
        margin: 0;
        }
        </style>
        """)
    
    with ui.header(elevated=True).style('position:relative; display:flex; justify-content:center; align-items:center') as mainHeader:
        ui.label(headerText)
        with ui.row().style('position:absolute; right:16px;') as headerButtons:
            with ui.button().props('elevated') as QrCode:
                ui.icon('qr_code')
                ui.tooltip('Scan QR Code').props('position-bottom')

            with ui.button().props('elevated') as profileButton:
                ui.icon('account_circle')
                ui.tooltip('View Profile').props('position-bottom')

            with ui.button().props('elevated') as settingsButton:
                ui.icon('settings')
                ui.tooltip('Settings').props('position-bottom')

    with ui.left_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as leftDrawer:
        with ui.row().classes('items-center').style('padding: 16px;'):
            ui.label('Card Database').style('font-size: 20px; font-weight: bold;')
            with ui.expansion('Aikatsu!').style('width: 220px;'):
                for i in ogkatsuList:
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

            with ui.expansion('Aikatsu Encore!').style('width: 220px;'):
                for i in encoreList:
                    clean_i = i.replace(' ', '-').lower()
