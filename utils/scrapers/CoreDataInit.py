from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
from lxml import etree

BASE_DIR = Path(__file__).resolve().parents[2]

def get_series_img():
    series = [
        "logo-aikatsu.png",
        "logo-aikatsustars.png",
        "logo-aikatsufriends.png",
        "logo-aikatsuonparade.png",
        "logo-aikatsuplanet.png"
    ]
    series_img_dir = BASE_DIR / 'Assets' / 'Core' / 'SeriesImg'
    if series_img_dir.is_dir():
        print("Series Image Directory Exists!")
    else:
        series_img_dir.mkdir(parents=True, exist_ok=True)

    for i in series:
        url = f'https://www.aikatsu.net/portal/img/{i}'
        data = requests.get(url).content
        with open(series_img_dir / i, 'wb') as file:
            file.write(data)

def get_planet_type_img():
    imglist = [
        'icon_AQUARIUM.png',
        'icon_CAFE.png',
        'icon_COSME.png',
        'icon_FAIRY.png',
        'icon_FLOWER.png',
        'icon_FRUITS.png',
        'icon_HOROSCOPE.png',
        'icon_JEWEL.png',
        'icon_MELTYHOUSE.png',
        'icon_MUSIC.png',
        'icon_STORY.png',
        'icon_SWEETS.png'
    ]

    core_types_dir = BASE_DIR / 'Assets' / 'Core' / 'Types'
    if core_types_dir.is_dir():
        print("Series Image Directory Exists!")
    else:
        core_types_dir.mkdir(parents=True, exist_ok=True)

    for i in imglist:
        url = f'https://card.aikatsu.net/planet/images/swinglist/dressia/{i}'
        data = requests.get(url).content
        with open(core_types_dir / i, 'wb') as file:
            file.write(data)

def get_series_brand(series):
    match series:
        case 'OGKatsu':
            imglist = [
                'angely-sugar_01',
                'futuring-girl_04',
                'spicy-ageha_08',
                'happy-rainbow_15',
                'loli-gothic_05',
                'aurora-fantasy_02',
                'magical-toy_16',
                'love-queen_09',
                'love-moonrise_10',
                'swing-rock_06',
                'bohemian-sky_11',
                'vivid-kiss_17',
                'dreamy-crown_03',
                'sangria-rosa_12',
                'dance-fusion_07',
                'sakurairo-kaden_13',
                'retroclover_18',
                'dolly-devil_14',
                'mecha-paniq_19'
            ]
        case 'Stars':
            imglist = [
                'rainbow-berry-parfait_02',
                'berry-parfait_01',
                'mylittle-heart_03',
                'spice-chord_04',
                'royal-sword_06',
                'gothic-victoria_05',      
                'prefect-queen_08',
                'romance-kiss_07',
                'fuwafuwa-deeam_10',
                'shiny-sumile_09'
            ]
        case 'Friends':
            imglist = [
                'sugar-melody_07',
                'classical-ange_08',
                'antiquesailor_09',
                'humming-leaf_10',
                'matelial_color_11',
                'luna-witch_12',
                'moon-maiden_13',
                'glorioussnow_14',
                'dancing-mirage_15',
                'heavnly-perfume_16',
                'silkyqcean_17',
                'colorful-shake_18',
                'milky-joker_19',
                'pure-palette_01',
                'love-metear_02',
                'honey-cat_04',
                'reflect-moon_03',
                'i-believe_05',
                'baby-pirates_06'
            ]
        case 'Parade':
            imglist = []
        case 'Planet':
            imglist = []

    brands_dir = BASE_DIR / 'Assets' / 'Brands'
    if brands_dir.is_dir():
        print("Series Image Directory Exists!")
    else:
        brands_dir.mkdir(parents=True, exist_ok=True)

    for i in imglist:
        url = f'https://www.aikatsu.net/portal/brand-type/img/{i}.png'
        data = requests.get(url).content
        with open(brands_dir / f'{i[:-3]}.png', 'wb') as file:
            file.write(data)

#get_series_img()

for i in ['OGKatsu', 'Stars', 'Friends', 'Parade', 'Plannet']:
    ...

get_planet_type_img()
#get_series_brand('Stars')