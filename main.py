from nicegui import app, ui
from headerUI import mainUI
from pathlib import Path
import cardViewer
import scanCard

ui.add_head_html('''
    <style>
        @font-face {
            font-family: 'Rounded Mplus 1c';
            src: url('/Assets/Fonts/MPLUSRounded1c-Black.ttf') format('truetype');
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }
                 
        body {
            font-family: 'Rounded Mplus 1c', sans-serif !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
    </style>
''', shared=True)

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