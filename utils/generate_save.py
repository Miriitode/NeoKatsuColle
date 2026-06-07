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
            'countCute': [],
            'countCool': [],
            'countSexy': [],
            'countPop': [],
            'countN': [],
            'countR': [],
            'countPR': [],
            'countCPR': [],
            'countAcc': []
        },
        'stars': {
            'overallTotal': 0,
            'seriesTotal': [],
            'countCute': [],
            'countCool': [],
            'countSexy': [],
            'countPop': [],
            'countN': [],
            'countR': [],
            'countPR': [],
            'countCR': [],
            'countSPR': []
        },
        'friends': {
            'overallTotal': 0,
            'seriesTotal': [],
            'countCute': [],
            'countCool': [],
            'countSexy': [],
            'countPop': [],
            'countN': [],
            'countR': [],
            'countPR': [],
            'countFR': [],
            'countJR': [],
            'countBFR': []
        },
        'parade': {
            'overallTotal': 0,
            'seriesTotal': [],
            'countCute': [],
            'countCool': [],
            'countSexy': [],
            'countPop': [],
            'countN': [],
            'countR': [],
            'countPR': [],
            'countCR': [],
            'countLPR': []
        },
        'planet': {
            'overallTotal': 0,
            'seriesTotal': [],
            'countFairy': [],
            'countJewel': [],
            'countHoroscope': [],
            'countMusic': [],
            'countStory': [],
            'countSweets': [],
            'countFlower': [],
            'countCosme': [],
            'countCafe': [],
            'countFruits': [],
            'countAquarium': [],
            'countMeltyhouse': [],
            'countN': [],
            'countR': [],
            'countPR': [],
            'countCP': [],
            'countSEC': []
        },
        'encore': {

        }
    }

    for series in [('aikatsu', aikatsuList), ('stars', starsList), ('friends', friendsList), ('parade', paradeList), ('planet', planetList), ('encore', encoreList)]:
        for refnum, _ in enumerate(series[1]):
            with open(BASE_DIR / "Database" / series[0] / f'{series[0]}_Data-{refnum}.json', 'r', encoding='utf-8') as data:
                info = json.load(data)
                
                for card in info:
                    ...

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