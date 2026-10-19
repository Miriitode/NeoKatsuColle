from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import json
from lxml import etree

BASE_DIR = Path(__file__).resolve().parents[2]

def Generate(link, series):
    webLink = f'https://www.aikatsu.com/planet/swinglist/?search=true&category={link}'
    game = 'データカードダスアイカツプラネット!'
    cardData = []

    if (BASE_DIR / "utils" / "scrapers" / "scrapedata" / "planet" / f"planet_Data-{series}.json").is_file():
        file = BASE_DIR / "utils" / "scrapers" / "scrapedata" / "planet" / f"planet_Data-{series}.json"

        if file.stat().st_size != 0:
            print("Database exists! Scraping next cardset...")
            return

    planet = BeautifulSoup(requests.get(webLink).content, 'html.parser')
        
    export = open(BASE_DIR / "utils" / "scrapers" / "scrapedata" / "planet" / f"planet_Data-{series}.json", 'w', encoding='utf-8')
    cardList = planet.find_all("div", class_=re.compile("data page"))
    title = planet.find("dl", {"class":"contentInner fade"}).dt.img.attrs.get('alt')
    print(f'({series}) Generating Card Database: {game} {title}')

    for card in cardList:
        #initialize and append base data values
        cardID = card.find("div", {"class":"cardNum"}).string
        cardName = card.find("div", {"class":"cardName"}).string
        cardLv = card.find("dl", {"class":"attributeCol"}).next_sibling.next_sibling.dd.string
        cardDesc = card.find("div", {"class":"dressiaTxt"}).string
        cardSkill = card.find("dl", {"class":"skillCol"}).dd.string
        cardType = []
        cardImg = []

        #data that needs to be filtered goes here
        typeList = card.find("dl", {"class":"typeCol"}).dd
        for type in typeList.find_all("img"):
                cardType.append(type.attrs.get("alt"))
        cardBase = re.split('[- ]', cardID)
        
        #image scraping section
        for im in card.find("div", {"class":"cardImgCol"}):
            cardLink = im.attrs.get("src")[3:]
            cardOut = f'https://www.aikatsu.com/planet/{cardLink}'
            cardImg.append(cardOut)

        cardExport = {
            'ID': cardID,
            'Series': cardBase[0],
            'CardNo': cardBase[1],
            'Rarity': cardBase[2],
            'Name': cardName,
            'Level': cardLv,
            'Description': cardDesc,
            'Skill': cardSkill,
            'Type': cardType,
            'frontLink': cardImg[0],
            'backLink': cardImg[1]
            }

        cardData.append(cardExport)

    #Write Operations
    outData = json.dumps(cardData,ensure_ascii=False, indent = 3)
    export.write(outData)
    export.close()