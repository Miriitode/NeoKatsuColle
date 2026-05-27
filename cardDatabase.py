from nicegui import ui
import mainUI
import json
from identifiers import load_identifiers

LIGHTWEIGHT_MODE = True

ogkatsuList, starsList, friendsList, paradeList, planetList, encoreList, brands, types, planetype = load_identifiers()

def headerDetail(card, route_prefix):
    with ui.row().classes('w-full items-center gap-3') as idHeader:
        ui.label(f"{card['ID']}").style('font-size: 16px; color: gray;')

        with ui.row().classes('items-end gap-2') as titleHeader:
            ui.label(card['Name']).style('font-size: 22px; font-weight: bold;')
            if route_prefix == 'planet':
                ui.label(f"{card['Rarity']} ({card['Level']})").style('color: gray;')
            elif route_prefix != 'friends' and route_prefix != 'parade':
                ui.label(f"{card['Rarity']}").style('color: gray;')
            else:
                ui.label(f"{card['RarityFull']} ({card['RarityFig']})").style('color: gray;')

        with ui.row().classes('items-center gap-2 ml-auto') as infoHeader:
            if route_prefix != 'planet':
                ui.label(f'Appeal: {card["Appeal"]}').style('color: gray;')

            with ui.checkbox().props('disable') as owned:
                if owned.value:
                    ui.tooltip('Card Owned').props('position-bottom')
                else:
                    ui.tooltip('Card Not Owned').props('position-bottom')

def mainInfo(card, route_prefix, j):

    if route_prefix == 'aikatsu':
        columns = 9
        headers = ['Type','Brand','Category','Lucky Star','Points','Constellation','Romance','BOOM','Fever']
        values = [card['Type'],card['Brand'],card['Category'],card['LuckyStar'],card['Points'],card['Constellation'],card['Romance'],card['BOOM'],card['Fever']]

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

def card_opt(card, route_prefix, j):

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
    with ui.column().classes('items-center shrink-0 gap-2').style(f'width: {column_width};'):

        if route_prefix != 'planet':
            ui.image(
                img_src
            ).style('width: 100%;')

        else:
            with ui.row().classes('w-full no-wrap gap-2 justify-center'):
                ui.image(
                    front_src
                ).style('width: 50%;')

                ui.image(
                    back_src
                ).style('width: 50%;')

        with ui.row().classes('w-full justify-center gap-1'):

            with ui.button(icon='favorite').props('flat rouond dense color=red') as cardLike:
                ui.tooltip('Add to favorites')

            with ui.button(icon='qr_code').props('flat round dense') as cardQR:
                ui.tooltip('See QR Code')

            with ui.button(icon='rectangle').props('flat round dense') as cardBarcode:
                ui.tooltip('See card Barcode')

def render_value(header, value, route_prefix, card):
    # Brand
    if header == 'Brand':
        if type(value) != list and value in brands and value != 'ノーブランド':
            with ui.element('div').classes('w-full flex justify-center'):
                ui.image(f'/Assets/Brands/{brands[value]}').style('width: 80px;')
        else:
            ui.label(card["Brand"]).classes('text-center w-full').style('color: gray;')
    # Type
    elif header == 'Type':
        if value != '-':
            with ui.element('div').classes('w-full flex justify-center'):
                if route_prefix != 'planet':
                    ui.image(f'/Assets/Core/Types/{types[value]}').style('width: 80px;')
                else:
                    for i in value:
                        ui.image(f'/Assets/Core/Types/{planetype[i]}').style('width: 240px;')
        else:
            ui.label('None').classes('text-center w-full').style('color: gray;')

    # Friends category list
    elif header == 'Category' and route_prefix == 'friends':
        for cat in card['Category']:
            ui.label(cat).classes('text-center w-full').style('color: black;')

    # Default text
    else:
        ui.label(str(value)).classes('text-center w-full').style('color: black;')


def render_grid(headers, values, route_prefix, card):
    with ui.grid(columns=len(headers)).classes('w-full gap-x-6 gap-y-2 items-center justify-items-center text-center'):

        # headers
        for header in headers:
            ui.label(header).classes('text-center w-full').style('color: gray; font-size: 13px;')

        # values
        for idx, value in enumerate(values):
            render_value(headers[idx],value,route_prefix,card)

def create_series_pages(series_list, route_prefix, series_title):

    for j, i in enumerate(series_list):
        clean_i = i.replace(' ', '-').lower()

        def create_page(i=i, clean_i=clean_i, j=j):
            with open(f'Database/{route_prefix}/{route_prefix}_Data-{j}.json', 'r', encoding='utf-8') as cardData:
                data = json.load(cardData)

            @ui.page(f'/{route_prefix}/{clean_i}')
            def card_page(i=i):

                # Main UI here
                mainUI.mainUI(f'NeoKatsuColle | {series_title} - {i}')

                ITEMS_PER_PAGE = 35

                current_page = {'value': 1}
                total_pages = max(1, (len(data) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

                with ui.column().classes('w-full'):
                    # scrollable content container
                    with ui.scroll_area().classes('w-full').style('height: calc(85vh - 90px);'):
                        card_container = ui.column().classes('w-full gap-4 p-4')

                    # pagination controls
                    with ui.row().classes('w-full justify-center p-2'):
                        pagination = ui.pagination(1,total_pages,direction_links=True,value=current_page['value'])

                    def render_page():

                        card_container.clear()

                        start = (current_page['value'] - 1) * ITEMS_PER_PAGE
                        end = start + ITEMS_PER_PAGE

                        visible_cards = data[start:end]

                        with card_container:

                            for card in visible_cards:

                                with ui.card().classes('w-full') as mainCard:

                                    headerDetail(card, route_prefix)

                                    with ui.row().classes('w-full items-start gap-4 p-4') as cardImg_cardInfo:

                                        card_opt(card, route_prefix, j)

                                        with ui.column().classes('w-full flex-1 gap-2'):

                                            columns, headers, values = mainInfo(card, route_prefix, j)

                                            if route_prefix == 'aikatsu':
                                                split_index = (len(headers) + 1) // 2
                                                render_grid(headers[:split_index],values[:split_index],route_prefix,card)
                                                render_grid(headers[split_index:],values[split_index:],route_prefix,card)

                                            else:
                                                render_grid(headers,values,route_prefix,card)

                                            ui.label('Notes').style('color: gray; font-size: 13px;')

                                            with ui.card().classes('w-full').style('height: auto;'):
                                                if route_prefix != 'planet':
                                                    ui.label(card['Notes']).style('font-size: 16px; color: gray;')
                                                else:
                                                    ui.label(card['Description']).style('font-size: 16px; color: gray;')

                    def change_page(e):
                        current_page['value'] = e.value
                        render_page()
                    pagination.on_value_change(change_page)
                    render_page()

        create_page()


# Data Carddass Aikatsu!
create_series_pages(
    ogkatsuList,
    'aikatsu',
    'Data Carddass Aikatsu!'
)

# Data Carddass Aikatsu Stars!
create_series_pages(
    starsList,
    'stars',
    'Data Carddass Aikatsu Stars!'
)

# Data Carddass Aikatsu Friends!
create_series_pages(
    friendsList,
    'friends',
    'Data Carddass Aikatsu Friends!'
)

# Data Carddass Aikatsu on Parade!
create_series_pages(
    paradeList,
    'parade',
    'Data Carddass Aikatsu on Parade!'
)

# Data Carddass Aikatsu Planet!
create_series_pages(
    planetList,
    'planet',
    'Data Carddass Aikatsu Planet!'
)

# # Data Carddass Aikatsu Encore!
# create_series_pages(
#     encoreList,
#     'encore',
#     'Data Carddass Aikatsu Encore!'
# )