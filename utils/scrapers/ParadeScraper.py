from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import json
from lxml import etree

BASE_DIR = Path(__file__).resolve().parents[2]

def Generate(link, series):
    webLink = f'https://www.aikatsu.com/onparade/cardlist/index.php?search=true&category={link}'
    game = 'データカードダスアイカツオンパレード！'
    cardData = []

    if (BASE_DIR / "utils" / "scrapers" / "scrapedata" / "parade" / f"parade_Data-{series}.json").is_file():
        file = BASE_DIR / "utils" / "scrapers" / "scrapedata" / "parade" / f"parade_Data-{series}.json"

        if file.stat().st_size != 0:
            print("Database exists! Scraping next cardset...")
            return
        
    #parade = BeautifulSoup(open(BASE_DIR / "Sample_Data" / "Parade" / "parade.html", encoding="utf-8"), 'html.parser')
    parade = BeautifulSoup(requests.get(webLink).content, 'html.parser')
    export = open(BASE_DIR / "utils" / "scrapers" / "scrapedata" / "parade" / f"parade_Data-{series}.json", 'w', encoding='utf-8')
    cardList = parade.find("div", {"class":"cardlistCol"}).find("div", {"id":"lists"}).find_all("div", class_=re.compile("data page"))
    title = parade.find("div", {"class":"titCol titCol_cardlist"}).h3.img.attrs.get('alt')
    print(f'({series}) Generating Card Database: {game} {title}')

    for card in cardList:
        #initialize and append base data values
        cardID = card.find("dd", {"class":"cardNum"}).string
        cardName = card.find("dd", {"class":"cardName"}).string
        cardCategory = [text for text in card.find("dl", {"class":"attributeCol"}).dd.stripped_strings] #Some cards include more than 1 category in this field
        cardAP = card.find("dl", {"class":"appealPointCol"}).dd.string
        cardType = card.find("dl", {"class":"typeCol"}).dd.img.attrs.get("alt") 
        cardRarity = list(card.find("dl", {"class":"rarelityCol"}).dd.stripped_strings)
        cardAppeal = card.find("dl", {"class":"dapEffectCol"}).dd.string
        cardLink = card.find("dl", {"class":"cardImgCol"}).dd.img.attrs.get("src")[3:]
        #cardBase = re.split('[- ]', cardID) # unused. cardID is not consistent with some cards in card set 1
        cardOut = f'https://www.aikatsu.com/onparade/{cardLink}'

        #data that needs to be filtered goes here
        if card.find("dl", {"class":"noteTxtCol"}):
            cardRemarks = card.find("dl", {"class":"noteTxtCol"}).dd.string #Only for Promotional Cards / Full Coordinate Cards
        else:
            cardRemarks = "None"

        if card.find("dl", {"class":"schoolCol"}).dd.img:
            cardSchool = card.find("dl", {"class":"schoolCol"}).dd.img.attrs.get("alt")
        else:
            cardSchool = ''.join(card.find("dl", {"class":"schoolCol"}).dd.string.split())

        if card.find("dl", {"class":"brandCol"}).dd.img:
            cardBrand = card.find("dl", {"class":"brandCol"}).dd.img.attrs.get("alt") # SOME Common rarity cards do not have an image for their brand data
        else:
            cardBrand = card.find("dl", {"class":"brandCol"}).dd.string.split()

        #compile data as dictionary for csv exporting
        cardExport = {
            'ID': cardID,
            'RarityFull': cardRarity[0],
            'RarityFig': cardRarity[1],
            'Category': cardCategory,
            'Name': cardName,
            'Brand': cardBrand,
            'School': cardSchool,
            'Type': cardType,
            'Appeal': cardAppeal,
            'Points': cardAP,
            'Notes': cardRemarks,
            'imgLink':cardOut
            }

        cardData.append(cardExport)

    #Write Operations
    outData = json.dumps(cardData,ensure_ascii=False, indent = 3)
    export.write(outData)
    export.close()