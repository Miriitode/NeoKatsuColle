import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

for series in ['aikatsu', 'stars', 'friends', 'parade']:
    print(series)
    folder = BASE_DIR / "Database" / series
    for cardData in folder.iterdir():
        with open(cardData, 'r', encoding='utf-8') as cards:
            data = json.load(cards)

            try:
                for card in data:
                    raritySym = "-"

                    if series == 'friends' or series == 'parade':
                        rarityCheck = card["RarityFull"]
                    else:
                        rarityCheck = card["Rarity"]
                    
                    match rarityCheck:
                        case "ノーマル":
                            raritySym = "N"
                        case "レア":
                            raritySym = "R"
                        case "プレミアムレア":
                            raritySym = "PR"
                        case "キャンペーンレア" | "キャンペーンレア+":
                            if series == "aikatsu":
                                raritySym = "CPR"
                            elif series == "stars":
                                raritySym = "CP"
                        case "スタープレミアムレア":
                            raritySym = "SPR"
                        case "フレンズレア":
                            raritySym = "FR"
                        case "ジュエリングレア":
                            raritySym = "JR"
                        case "ベストフレンズレア":
                            raritySym = "BFR"
                        case "レジェンドプレミアムレア":
                            raritySym = "LPR"
                        case "-":
                            continue

                    card["RarityCode"] = raritySym

                with open(cardData, 'w', encoding='utf-8') as cards:
                    json.dump(data, cards, ensure_ascii=False, indent=4)

            except Exception as e:
                print("Error: ", e)
                continue