from nicegui import ui

from identifiers import load_identifiers
from uiCardColor import ui_cardcolor
from barcodeUtils import showQRBarcode

LIGHTWEIGHT_MODE = False

aikatsuList = load_identifiers('aikatsu')
starsList = load_identifiers('stars')
friendsList = load_identifiers('friends')
paradeList = load_identifiers('parade')
planetList = load_identifiers('planet')
encoreList = load_identifiers('encore')
brands = load_identifiers('brands')
types = load_identifiers('types')
planetype = load_identifiers('planettype')
filtercodes = load_identifiers('filtercode')


def headerDetail(card, route_prefix):
    if route_prefix != 'planet':
        headerStyle = f"background-color: {ui_cardcolor(card['Type'], 'fg')};"
    else:
        planet_colors = ui_cardcolor(card['Type'], 'fg', isPlanetType=True)
        headerStyle = f"background: linear-gradient(135deg, {planet_colors[0]} 0%, {planet_colors[1]} 100%);"

    with ui.card().classes('w-full no-shadow').style(f'{headerStyle} border-radius: 20px 20px 0px 0px;'):
        with ui.row().classes('w-full items-center gap-3') as idHeader:
            with ui.column().classes('gap-0'):
                if route_prefix == 'planet':
                    ui.label(f"{card['ID']}").style(f"font-size: 16px; color: {ui_cardcolor(card['Type'], 't3', isPlanetType = True)};")
                else:
                    ui.label(f"{card['ID']}").style(f"font-size: 16px; color: {ui_cardcolor(card['Type'], 't3')};")

                with ui.row().classes('items-end gap-2') as titleHeader:
                    if route_prefix == 'planet':
                        ui.label(card['Name']).style(f"font-size: 22px; font-weight: bold; color: {ui_cardcolor(card['Type'], 't1', isPlanetType=True)}")
                    else:
                        ui.label(card['Name']).style(f"font-size: 22px; font-weight: bold; color: {ui_cardcolor(card['Type'], 't1')}")

                    if route_prefix == 'planet':
                        ui.label(f"{card['Rarity']} ({card['Level']})").style(f"color: {ui_cardcolor(card['Type'], 't3', isPlanetType=True)};")
                    elif route_prefix != 'friends' and route_prefix != 'parade':
                        ui.label(f"{card['Rarity']}").style(f"color: {ui_cardcolor(card['Type'], 't3')};")
                    else:
                        ui.label(f"{card['RarityFull']} ({card['RarityFig']})").style(f"color: {ui_cardcolor(card['Type'], 't3')};")

            with ui.row().classes('items-center gap-2 ml-auto') as infoHeader:
                with ui.checkbox().props('disable') as owned:
                    if owned.value:
                        ui.tooltip('Card Owned').props('position-bottom')
                    else:
                        ui.tooltip('Card Not Owned').props('position-bottom')


def mainInfo(card, route_prefix, j):
    if route_prefix == 'aikatsu':
        columns = 9
        headers = ['Type', 'Brand', 'Category', 'Lucky Star', 'Points', 'Constellation', 'Romance', 'BOOM', 'Fever']
        values = [card['Type'], card['Brand'], card['Category'], card['LuckyStar'], card['Points'], card['Constellation'], card['Romance'], card['BOOM'], card['Fever']]

    elif route_prefix == 'stars':
        columns = 6
        headers = ['Type', 'Brand', 'Category', 'Points', 'Upgrade', 'Plus']
        values = [card['Type'], card['Brand'], card['Category'], card['Points'], card['Upgrade'], card['Plus']]

    elif route_prefix == 'friends':
        columns = 4
        headers = ['Type', 'Brand', 'Category', 'Points']
        values = [card['Type'], card['Brand'], card['Category'], card['Points']]

    elif route_prefix == 'parade':
        columns = 5
        headers = ['Type', 'Brand', 'Category', 'School', 'Points']
        values = [card['Type'], card['Brand'], card['Category'], card['School'], card['Points']]

    elif route_prefix == 'planet':
        columns = 2
        headers = ['Type', 'Skill']
        values = [card['Type'], card['Skill']]

    return columns, headers, values


def cardOpt(card, route_prefix, j):
    if LIGHTWEIGHT_MODE:
        if route_prefix == 'planet':
            front_src = card['frontLink']
            back_src = card['backLink']
        else:
            img_src = card['imgLink']
    else:
        img_src = f'/Assets/Cards/{route_prefix}/cardimg-{j}/{card["ID"]}.png'
        front_src = f'/Assets/Cards/{route_prefix}/cardimg-{j}/{card["ID"]} Front.png'
        back_src = f'/Assets/Cards/{route_prefix}/cardimg-{j}/{card["ID"]} Back.png'

    column_width = '560px' if route_prefix == 'planet' else '240px'

    with ui.card().classes('h-full no-shadow').style(f"background-color: {ui_cardcolor(card['Type'], 'a2')}"):
        with ui.column().classes('items-center flex-1 gap-2').style(f'width: {column_width};'):
            if route_prefix != 'planet':
                ui.image(img_src).style('width: 100%;')
            else:
                with ui.row().classes('w-full no-wrap gap-2 justify-center'):
                    ui.image(front_src).style('width: 50%;')
                    ui.image(back_src).style('width: 50%;')

            with ui.row().classes('w-full justify-center gap-1'):
                with ui.button(icon='favorite').props('flat rouond dense color=red') as cardLike:
                    ui.tooltip('Add to favorites')

                if route_prefix != 'planet':
                    with ui.button(icon='qr_code', on_click=lambda: showQRBarcode(card)).props('flat round dense') as cardQR:
                        ui.tooltip('See QR Code')

                if route_prefix == 'aikatsu':
                    with ui.button(icon='rectangle', on_click=lambda: showQRBarcode(card, isAikatsu=True, isBarcode=True)).props('flat round dense') as cardBarcode:
                        ui.tooltip('See card Barcode')


def renderValue(header, value, route_prefix, card):
    if header == 'Brand':
        if type(value) != list and value in brands and value != 'ノーブランド':
            with ui.element('div').classes('w-full flex justify-center'):
                ui.image(f'/Assets/Brands/{brands[value]}').style('width: 60px;')
        else:
            ui.label(card['Brand']).classes('text-center w-full').style('color: gray;')
    elif header == 'Type':
        if value != '-':
            with ui.element('div').classes('w-full flex justify-center'):
                if route_prefix != 'planet':
                    ui.image(f'/Assets/Core/Types/{types[value]}').style('width: 50px;')
                else:
                    for i in value:
                        ui.image(f'/Assets/Core/Types/{planetype[i]}').style('width: 180px;')
        else:
            ui.label('None').classes('text-center w-full').style(f"color: {ui_cardcolor(card['Type'], 't2')}; font-size: 22px;")
    elif header == 'Category' and (route_prefix == 'friends' or route_prefix == 'parade'):
        with ui.column().classes('w-full') as categoryColumn:
            for cat in card['Category']:
                ui.label(cat).classes('text-center w-full').style(f"color: {ui_cardcolor(card['Type'], 't2')}; font-size: 22px;")
    else:
        if header == 'Skill':
            ui.label(str(value)).classes('text-center w-full').style(f"color: {ui_cardcolor(card['Type'], 't2')}; font-size: 16px;")
        else:
            ui.label(str(value)).classes('text-center w-full').style(f"color: {ui_cardcolor(card['Type'], 't2')}; font-size: 22px;")


def renderGrid(headers, values, route_prefix, card):
    with ui.grid(columns=len(headers)).style('grid-auto-rows: 130px;').classes('w-full'):
        for header, value in zip(headers, values):
            if route_prefix == 'planet':
                planetHeaderColors = ui_cardcolor(card['Type'], 'a1', isPlanetType=True)
                with ui.card().classes('w-full h-full no-shadow').style(f"background-color: {ui_cardcolor(card['Type'], 'a2')}; padding: 6px;"):
                    with ui.card().classes('w-full no-shadow').style(f"background: linear-gradient(135deg, {planetHeaderColors[0]} 0%, {planetHeaderColors[1]} 100%); padding: 4px;"):
                        ui.label(header).classes('text-center w-full').style(f"color: {ui_cardcolor(card['Type'], 't1', isPlanetType = True)}; font-size: 18px;")

                    with ui.column().classes('w-full items-center justify-center flex-1'):
                        renderValue(header, value, route_prefix, card)

            else:
                with ui.card().classes('w-full h-full no-shadow').style(f"background-color: {ui_cardcolor(card['Type'], 'a2')}; padding: 6px;"):
                    with ui.card().classes('w-full no-shadow').style(f"background-color: {ui_cardcolor(card['Type'], 'a1')}; padding: 4px;"):
                        ui.label(header).classes('text-center w-full').style(f"color: {ui_cardcolor(card['Type'], 't1')}; font-size: 18px;")

                    with ui.column().classes('w-full items-center justify-center flex-1'):
                        renderValue(header, value, route_prefix, card)