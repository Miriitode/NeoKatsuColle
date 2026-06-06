import json

def load_identifiers(opt):
    with open('Database/Identifiers.json', 'r', encoding='utf-8') as series:
        seriesList = json.load(series)

        match opt:
            case 'aikatsu':
                aikatsu = seriesList['Series']['Aikatsu!']
                return aikatsu
            case 'stars':
                stars = seriesList['Series']['Aikatsu Stars!']
                return stars
            case 'friends':
                friends = seriesList['Series']['Aikatsu Friends!']
                return friends
            case 'parade':
                parade = seriesList['Series']['Aikatsu on Parade!']
                return parade
            case 'planet':
                planet = seriesList['Series']['Aikatsu Planet!']
                return planet
            case 'enccore':
                encore = seriesList['Series']['Aikatsu Encore!']
                return encore
            case 'brands':
                brands = seriesList['Brands']
                return brands
            case 'types':
                types = seriesList['Types']
                return types
            case 'planettype':
                planetype = seriesList['PlanetType']
                return planetype
            
            #for compatibility, remove once code has been properly refactored
            case None:
                aikatsu = seriesList['Series']['Aikatsu!']
                stars = seriesList['Series']['Aikatsu Stars!']
                friends = seriesList['Series']['Aikatsu Friends!']
                parade = seriesList['Series']['Aikatsu on Parade!']
                planet = seriesList['Series']['Aikatsu Planet!']
                encore = seriesList['Series']['Aikatsu Encore!']

                brands = seriesList['Brands']
                types = seriesList['Types']
                planetype = seriesList['PlanetType']
                return aikatsu, stars, friends, parade, planet, encore, brands, types, planetype