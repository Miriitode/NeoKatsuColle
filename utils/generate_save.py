from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

import json
from identifiers import load_identifiers


aikatsuList = load_identifiers('aikatsu')
starsList = load_identifiers('stars')
friendsList = load_identifiers('friends')
paradeList = load_identifiers('parade')
planetList = load_identifiers('planet')
encoreList = load_identifiers('encore')

def countSeries():
    db = {
        'aikatsu': {
            'overallTotal': 0,
            'seriesTotal': [],
            'totalCute': [],
            'totalCool': [],
            'totalSexy': [],
            'totalPop': [],
            'totalN': [],
            'totalR': [],
            'totalPR': [],
            'totalCPR': [],
            'totalAcc': []
        },
        'stars': {
            'overallTotal': 0,
            'seriesTotal': [],
            'totalCute': [],
            'totalCool': [],
            'totalSexy': [],
            'totalPop': [],
            'totalN': [],
            'totalR': [],
            'totalPR': [],
            'totalCR': [],
            'totalSPR': []
        },
        'friends': {
            'overallTotal': 0,
            'seriesTotal': [],
            'totalCute': [],
            'totalCool': [],
            'totalSexy': [],
            'totalPop': [],
            'totalN': [],
            'totalR': [],
            'totalPR': [],
            'totalFR': [],
            'totalJR': [],
            'totalBFR': []
        },
        'parade': {
            'overallTotal': 0,
            'seriesTotal': [],
            'totalCute': [],
            'totalCool': [],
            'totalSexy': [],
            'totalPop': [],
            'totalN': [],
            'totalR': [],
            'totalPR': [],
            'totalCR': [],
            'totalLPR': []
        },
        'planet': {
            'overallTotal': 0,
            'seriesTotal': [],
            'totalFairy': [],
            'totalJewel': [],
            'totalHoroscope': [],
            'totalMusic': [],
            'totalStory': [],
            'totalSweets': [],
            'totalFlower': [],
            'totalCosme': [],
            'totalCafe': [],
            'totalFruits': [],
            'totalAquarium': [],
            'totalMeltyhouse': [],
            'totalN': [],
            'totalR': [],
            'totalPR': [],
            'totalCP': [],
            'totalSEC': []
        },
        'encore': {

        }
    }

    for series in [('aikatsu', aikatsuList), ('stars', starsList), ('friends', friendsList), ('parade', paradeList), ('planet', planetList), ('encore', encoreList)]:
        totalCount = 0
        for refnum, _ in enumerate(series[1]):
            for key in db[series[0]].keys():
                if key != 'overallTotal' and key != 'seriesTotal':
                    db[series[0]][key].append(0)

            with open(BASE_DIR / "Database" / series[0] / f'{series[0]}_Data-{refnum}.json', 'r', encoding='utf-8') as data:
                info = json.load(data)
                
                db[series[0]]['seriesTotal'].append(len(info))

                for card in info:
                    if series[0] != 'friends' or series[0] != 'parade':
                        rarity = card['Rarity']
                    else:
                        rarity = card['RarityFull']

                    if series[0] != 'planet':
                        cardType = [card['Type']]

                    match rarity:
                        case 'ノーマル' | 'N':
                            db[series[0]]['totalN'][-1] += 1
                        case 'レア' | 'R':
                            db[series[0]]['totalR'][-1] += 1
                        case 'プレミアムレア' | 'PR':
                            db[series[0]]['totalPR'][-1] += 1
                        case 'キャンペーンレア' | 'CP':
                            db[series[0]]['totalCPR'][-1] += 1
                        case '':
                            db[series[0]]['totalCR'][-1] += 1
                        case 'スタープレミアムレア':
                            db[series[0]]['totalSPR'][-1] += 1
                        case 'フレンズレア':
                            db[series[0]]['totalFR'][-1] += 1
                        case 'ジュエリングレア':
                            db[series[0]]['totalJR'][-1] += 1
                        case 'ベストフレンズレア':
                            db[series[0]]['totalBFR'][-1] += 1
                        case 'レジェンドプレミアムレア':
                            db[series[0]]['totalLPR'][-1] += 1
                        case 'SEC':
                            db[series[0]]['totalSEC'][-1] += 1
                        case _:
                            print(f"[WARN] No matching rarity {rarity}")
                
                    for cardEvalType in cardType:
                        match cardEvalType:
                            case 'キュート':
                                db[series[0]]['totalCute'][-1] += 1
                            case 'クール':
                                db[series[0]]['totalCool'][-1] += 1
                            case 'セクシー':
                                db[series[0]]['totalSexy'][-1] += 1
                            case 'ポップ':
                                db[series[0]]['totalPop'][-1] += 1
                            case '-':
                                db[series[0]]['totalAcc'][-1] += 1
                            case 'フェアリー':
                                db[series[0]]['totalFairy'][-1] += 1
                            case 'ジュエル':
                                db[series[0]]['totalJewel'][-1] += 1
                            case 'ホロスコープ':
                                db[series[0]]['totalHoroscope'][-1] += 1
                            case 'ミュージック':
                                db[series[0]]['totalMusic'][-1] += 1
                            case 'ストーリー':
                                db[series[0]]['totalStory'][-1] += 1
                            case 'スウィーツ':
                                db[series[0]]['totalSweets'][-1] += 1
                            case 'フラワー':
                                db[series[0]]['totalFlower'][-1] += 1
                            case 'コスメ':
                                db[series[0]]['totalCosme'][-1] += 1
                            case 'カフェ':
                                db[series[0]]['totalCafe'][-1] += 1
                            case 'フルーツ':
                                db[series[0]]['totalFruits'][-1] += 1
                            case 'アクアリウム':
                                db[series[0]]['totalAquarium'][-1] += 1
                            case 'メルティーハウス':
                                db[series[0]]['totalMeltyhouse'][-1] += 1
                            case '_':
                                print(f"[WARN] No matching type {card['Type']}")
                    
                        

def generateSave(name):
    save = {
        'profile': name,
        'cardsCollected': 0,
        'series': {
            'aikatsu': {
                'collected': [0]*len(aikatsuList),
                'overallTotal': 0,
            },
            'stars': {
                'collected': [0]*len(starsList),
                'overallTotal': 0,
            },
            'friends': {
                'collected': [0]*len(friendsList),
                'overallTotal': 0,
            },
            'parade': {
                'collected': [0]*len(paradeList),
                'overallTotal': 0,
            },
            'planet': {
                'collected': [0]*len(planetList),
                'overallTotal': 0,
            },
            'encore': {
                'collected': [0]*len(encoreList),
                'overallTotal': 0,
            }
        }

    }