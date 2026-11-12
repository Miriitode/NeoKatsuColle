# updates information in the old card database before migrating everything to the database
# the following will be modified:
# - Data Carddass Aikatsu card IDs (to include their respective raritites to match the actual card)
# - All Image Links from stars to planet due to website updates (php moment)
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[0]

def rarity(cardID, cardRarity):
    match cardRarity:
        case "ノーマル":
            return f"{cardID} N"
        case "レア":
            return f"{cardID} R"
        case "プレミアムレア":
            if cardID[:2] in ["01", "02", "03", "04", "05", "06"]:
                return f"{cardID} P"
            else:
                return f"{cardID} PR"
        case _:
            return cardID
        
for series in ['aikatsu', 'stars', 'friends', 'parade']:
    print(series)
    folder = BASE_DIR / "scrapers" / "scrapedata" / series

    for cardData in folder.iterdir():
        with open(cardData, 'r', encoding='utf-8') as cards:
            data = json.load(cards)

            for card in data:
                if series == 'aikatsu':
                    modify = rarity(card['ID'], card['Rarity'])
                    card['ID'] = modify
                elif series == 'planet':
                    truncFront = card['frontLink'][23:]
                    truncBack = card['backLink'][23:]
                    modifyFront = f"https://card.aikatsu.net{truncFront}"
                    modifyBack = f"https://card.aikatsu.net{truncBack}"
                    card['frontLink'] = modifyFront
                    card['backLink'] = modifyBack
                else:
                    trunc = card['imgLink'][23:]
                    modify = f"https://card.aikatsu.net{trunc}"
                    card['imgLink'] = modify

            with open(cardData, 'w', encoding='utf-8') as cards:
                json.dump(data, cards, ensure_ascii=False, indent=4)