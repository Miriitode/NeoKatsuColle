from nicegui import ui
import mainUI
import json

with open('Database/SeriesIdentifiers.json', 'r', encoding='utf-8') as series:
    seriesList = json.load(series)

    ogkatsuList = seriesList['Series']['Aikatsu!']
    starsList = seriesList['Series']['Aikatsu Stars!']
    friendsList = seriesList['Series']['Aikatsu Friends!']
    paradeList = seriesList['Series']['Aikatsu on Parade!']
    planetList = seriesList['Series']['Aikatsu Planet!']
    encoreList = seriesList['Series']['Aikatsu Encore!']

    brands = seriesList['Brands']


def create_series_pages(series_list, route_prefix, series_title):

    for j, i in enumerate(series_list):
        clean_i = i.replace(' ', '-').lower()

        def create_page(i=i, clean_i=clean_i, j=j):
            with open(f'Database/{route_prefix}/CardList/{route_prefix}_Data-{j}.json', 'r', encoding='utf-8') as cardData:
                data = json.load(cardData)

            @ui.page(f'/{route_prefix}/{clean_i}')
            def card_page(i=i):
                # Main UI here
                mainUI.mainUI(f'NeoKatsuColle | {series_title} - {i}')

                # Card List UI here
                with ui.scroll_area().classes('w-full').style('height: calc(85vh - 28px);'):
                    with ui.column().classes('w-full gap-4 p-4'):

                        #individual cards
                        for card in data:
                            with ui.card().classes('w-full'):
                                with ui.row().classes('w-full items-center gap-3') as idHeader:
                                    ui.label(f"{card['ID']}").style('font-size: 16px; color: gray;')

                                    with ui.row().classes('items-end gap-2') as titleHeader:
                                        ui.label(card['Name']).style('font-size: 22px; font-weight: bold;')
                                        ui.label(f"{card['Rarity']}").style('color: gray;')

                                    with ui.row().classes('items-center gap-2 ml-auto') as infoHeader:
                                        ui.label(card['Type']).style('color: gray;')

                                        with ui.checkbox() as owned:
                                            ui.tooltip('Card Owned').props('position-bottom')

                                with ui.row().classes('w-full items-start gap-4 p-4'):

                                    ui.image(
                                        f'/Assets/Cards/{route_prefix}/cardimg-{j}/{card["ID"]}.png'
                                    ).style('width: 10%;')

                                    with ui.column().classes('w-full flex-1 gap-2'):
                                        with ui.grid(columns=9).classes('w-full gap-x-6 gap-y-2 items-center justify-items-center text-center'):
                                            headers = ['Type','Brand','Category','Lucky Star','Points','Constellation','Romance','BOOM','Fever']
                                            values = [card['Type'],card['Brand'],card['Category'],card['LuckyStar'],card['Points'],card['Constellation'],card['Romance'],card['BOOM'],card['Fever'],]

                                            for header in headers:
                                                ui.label(header).classes('text-center w-full').style('color: gray; font-size: 13px;')

                                            for idx, value in enumerate(values):
                                                if headers[idx] == 'Brand':
                                                    if value != '-':
                                                        with ui.element('div').classes('w-full flex justify-center'):
                                                            ui.image(f'/Assets/Brands/{brands[route_prefix][value]}').style('width: 80px;')
                                                    else:
                                                        ui.label('None').classes('text-center w-full').style('color: gray;')
                                                else:
                                                    ui.label(str(value)).classes('text-center w-full').style('color: black;')
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