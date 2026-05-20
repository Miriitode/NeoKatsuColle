from nicegui import app, ui
from mainUI import mainUI
from pathlib import Path
import cardDatabase
import scanCard

def homePage():
    with ui.element('div').style('height: calc(85vh - 64px);').classes('w-full flex justify-center items-center') as homePage:
        with ui.column().classes('items-center'):
            ui.label('NeoKatsuColle').style('font-size:160px; font-weight:bold;')
            ui.label('A card collection tracker and database for the Data Carddass Aikatsu! series.').style('font-size:24px; color:gray;')

@ui.page('/')
def Page():
    mainUI('Welcome to NeoKatsuColle!')
    homePage()

app.add_static_files('/Assets', Path('Assets'))
ui.run()