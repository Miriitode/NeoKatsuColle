from nicegui import ui
import headerUI
import json

from identifiers import load_identifiers
from viewerUtils import headerDetail, mainInfo, cardOpt, renderValue, renderGrid
from uiCardColor import ui_cardcolor

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
            
def create_series_pages(series_list, route_prefix, series_title):
    filterState = {
        'Rarity': None,
        'Brand': None,
        'Type': None,
        'Category': None
    }
    for j, i in enumerate(series_list):
        clean_i = i.replace(' ', '-').lower()

        def create_page(i=i, clean_i=clean_i, j=j):
            with open(f'Database/{route_prefix}/{route_prefix}_Data-{j}.json', 'r', encoding='utf-8') as cardData:
                data = json.load(cardData)

            @ui.page(f'/{route_prefix}/{clean_i}')
            def card_page(i=i):

                with ui.right_drawer(fixed=False, value=False).style('background-color: #ebf1fa').props('bordered overlay') as rightDrawer:
                    ui.label('Filters').classes('text-h6')
                    rarity_select = ui.select(filtercodes[route_prefix],label='Rarity').classes('w-full')
                    brand_select = ui.select(sorted(brands.keys()),label='Brand').classes('w-full')
                    type_select = ui.select(sorted(types.keys()),label='Type').classes('w-full')

                    ui.button('Apply Filters',on_click=lambda: apply_filters())
                    ui.button('Clear Filters',on_click=lambda: clear_filters())

                # Main UI here
                headerUI.mainUI(f'NeoKatsuColle | {series_title} - {i}', isCardDB=True, drawer=rightDrawer)

                ITEMS_PER_PAGE = 35

                current_page = {'value': 1}
                total_pages = max(1, (len(data) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

                with ui.column().classes('w-full mt-0').style('margin-top: 0;'):
                    with ui.scroll_area().classes('w-full mt-0').style('height: calc(85vh - 72px); margin-top: 0;'):
                        card_container = ui.column().classes('w-full gap-2 p-2')

                    # pagination controls
                    with ui.row().classes('w-full justify-center p-2'):
                        pagination = ui.pagination(1,total_pages,direction_links=True,value=current_page['value'])

                    filtered_data = data.copy()

                    def apply_filters():
                        nonlocal filtered_data

                        filtered_data = data

                        if rarity_select.value:
                            if route_prefix != "planet":
                                filtered_data = [card for card in filtered_data if card.get('RarityCode') == rarity_select.value]
                            else:
                                filtered_data = [card for card in filtered_data if card.get('Rarity') == rarity_select.value]

                        if brand_select.value:
                            filtered_data = [card for card in filtered_data if card.get('Brand') == brand_select.value]

                        if type_select.value:
                            filtered_data = [card for card in filtered_data if card.get('Type') == type_select.value]
                        current_page['value'] = 1

                        pagination.max = max(1,(len(filtered_data) + ITEMS_PER_PAGE - 1)// ITEMS_PER_PAGE)

                        render_page()

                    def clear_filters():
                        nonlocal filtered_data

                        rarity_select.value = None
                        brand_select.value = None
                        type_select.value = None

                        filtered_data = data.copy()

                        current_page['value'] = 1

                        pagination.max = max(1,(len(filtered_data) + ITEMS_PER_PAGE - 1)// ITEMS_PER_PAGE)

                        render_page()

                    def render_page():

                        card_container.clear()

                        start = (current_page['value'] - 1) * ITEMS_PER_PAGE
                        end = start + ITEMS_PER_PAGE

                        visible_cards = filtered_data[start:end]

                        with card_container:

                            for card in visible_cards:

                                if route_prefix == 'planet':
                                    planet_colors = ui_cardcolor(card['Type'], 'bg', isPlanetType=True)
                                    cardColor = f"background: linear-gradient(135deg, {planet_colors[0]} 0%, {planet_colors[1]} 100%);"
                                else:
                                    cardColor = f'background-color: {ui_cardcolor(card["Type"], "bg")};'

                                with ui.card().classes('w-full p-0').style(f'{cardColor} border-radius: 20px 20px 20px 20px;') as mainCard:

                                    headerDetail(card, route_prefix)

                                    with ui.row().classes('w-full items-start gap-4 p-4') as cardImg_cardInfo:

                                        cardOpt(card, route_prefix, j)

                                        with ui.column().classes('w-full flex-1'):

                                            columns, headers, values = mainInfo(card, route_prefix, j)

                                            if route_prefix == 'aikatsu' or route_prefix == 'planet':
                                                split_index = (len(headers) + 1) // 2
                                                renderGrid(headers[:split_index],values[:split_index],route_prefix,card)
                                                renderGrid(headers[split_index:],values[split_index:],route_prefix,card)
                                            else:
                                                renderGrid(headers,values,route_prefix,card)

                                            if route_prefix != 'planet':
                                                with ui.card().classes('w-full no-shadow').style(f'height: auto; background-color: {ui_cardcolor(card['Type'], "a2")}; padding: 6px;'):
                                                    with ui.card().classes('w-full h-full no-shadow').style(f'background-color: {ui_cardcolor(card['Type'], "a1")}; padding: 6px;'):
                                                        ui.label('Appeal').classes('text-center w-full').style(f'color: {ui_cardcolor(card['Type'], "t1")}; font-size: 18px;')
                                                    
                                                    with ui.column().classes('w-full items-center justify-center flex-1'):
                                                        ui.label(f'{card["Appeal"]}').style(f'color: {ui_cardcolor(card['Type'], "t2")}; font-size: 22px;')

                                            if route_prefix != 'planet' and card['Notes'] != "None":
                                                with ui.card().classes('w-full no-shadow').style(f'height: auto; background-color: {ui_cardcolor(card['Type'], "a2")}; padding: 6px;'):
                                                    with ui.card().classes('w-full h-full no-shadow').style(f'background-color: {ui_cardcolor(card['Type'], "a1")}; padding: 6px;'):
                                                        ui.label('Notes').classes('text-center w-full').style(f'color: {ui_cardcolor(card['Type'], "t1")}; font-size: 18px;')

                                                    ui.label(card['Notes']).classes('text-center w-full').style(f'color: {ui_cardcolor(card['Type'], "t2")}; font-size: 18px;')
                                            elif route_prefix == 'planet':
                                                planetNotecolors = ui_cardcolor(card['Type'], 'a1', isPlanetType=True)
                                                with ui.card().classes('w-full no-shadow').style(f'height: auto; background-color: {ui_cardcolor(card['Type'], "a2", isPlanetType = True)}; padding: 6px;'):
                                                    with ui.card().classes('w-full h-full no-shadow').style(f'background: linear-gradient(135deg, {planetNotecolors[0]} 0%, {planetNotecolors[1]} 100%); padding: 6px;'):
                                                        ui.label('Notes').classes('text-center w-full').style(f'color: {ui_cardcolor(card['Type'], 't1', isPlanetType = True)}; font-size: 18px;')

                                                    ui.label(card['Description']).style(f'color: {ui_cardcolor(card['Type'], "t2")}; font-size: 16px;')

                    def change_page(e):
                        current_page['value'] = e.value
                        render_page()
                    pagination.on_value_change(change_page)
                    render_page()

        create_page()


# Data Carddass Aikatsu!
create_series_pages(
    aikatsuList,
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