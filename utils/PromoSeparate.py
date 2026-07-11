import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

with open(BASE_DIR / "Database" / "aikatsu" / "aikatsu_Data-22.json", "r", encoding='utf-8') as f:
    promoList = json.load(f)

promos = ['13', '14', '15', '15 BC', '15 CD', '15 DS', '15 FB', '15 JINS', '15 MA', '15 MC', '15 MG', '15 MS', '15 PA', '15 PB', '15 PC', '15 PD', '15 PG', '15 PH', '15 PJ', '15 PM', '15 PN', '15 PP', '15 PR', '15 PS', '15 PT', '15 PV', '15 PZ', '15 SP', '16 CD', '16 FB', '16 LIVE', '16 MS', '16 PA', '16 PC', '16 PD', '16 PG', '16 PJ', '16 PM', '16 PN', '16 PR', '16 PT', '16 PZ', '16 SP', 'AM', 'BD', 'CD', 'DS', 'GC', 'LIVE', 'MC', 'PA', 'PB', 'PC', 'PD', 'PG', 'PJ', 'PL', 'PM', 'PN', 'PP', 'PR', 'PS', 'PV', 'PZ', 'SP', 'TV']
promoCategory = []

for i in promos:
    promoCategory.append([])

for card in promoList:
    promoIdentifier = card['ID'].split("-")[0]

    if promoIdentifier in ['01', '02', '03', '04', '05', '06']:
        promoCategory[0].append(card)
    elif promoIdentifier in ['14 01', '14 02', '14 03', '14 04', '14 05']:
        promoCategory[1].append(card)
    elif promoIdentifier in ['15 01', '15 02', '15 03', '15 04', '15 05', '15 06']:
        promoCategory[2].append(card)
    else:
        refnum = promos.index(promoIdentifier)
        promoCategory[refnum].append(card)

promoNum = 22
for i in promoCategory:
    with open(BASE_DIR / "utils" / "FilteredPromos" / "aikatsu" / f"aikatsu_Data-{promoNum}.json", "w", encoding='utf-8') as out:
        json.dump(i, out, ensure_ascii=False, indent=4)
    
    promoNum += 1