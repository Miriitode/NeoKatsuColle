import json

def load_identifiers():
    with open('Database/Identifiers.json', 'r', encoding='utf-8') as series:
        seriesList = json.load(series)

        aikatsu = seriesList['Series']['Aikatsu!']
        stars = seriesList['Series']['Aikatsu Stars!']
        friends = seriesList['Series']['Aikatsu Friends!']
        parade = seriesList['Series']['Aikatsu on Parade!']
        planet = seriesList['Series']['Aikatsu Planet!']
        encore = seriesList['Series']['Aikatsu Encore!']

        brands = seriesList['Brands']
        types = seriesList['Types']

    return aikatsu, stars, friends, parade, planet, encore, brands, types