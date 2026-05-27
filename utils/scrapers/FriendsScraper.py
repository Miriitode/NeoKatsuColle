from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import json
from lxml import etree

BASE_DIR = Path(__file__).resolve().parents[2]

def Generate(link, series):
    webLink = f'https://www.aikatsu.com/friends/cardlist/?search=true&category={link}'
    game = 'データカードダスアイカツフレンズ!'
    cardData = []

    if (BASE_DIR / "Database" / "friends" / f"friends_Data-{series}.json").is_file():
        file = BASE_DIR / "Database" / "friends" / f"friends_Data-{series}.json"

        if file.stat().st_size != 0:
            print("Database exists! Scraping next cardset...")
            return
        
    friends = BeautifulSoup(requests.get(webLink).content, 'html.parser')
    export = open(BASE_DIR / "Database" / "friends" / f"friends_Data-{series}.json", 'w', encoding='utf-8')
    cardList = friends.find("div", {"class":"cardlistCol clearfix"}).find("div", {"id":"lists"}).find_all("div", class_=re.compile("data page"))
    title = friends.find("div", {"id":"titCol"}).h3.img.attrs.get('alt')
    print(f'({series}) Generating Card Database: {game} {title}')

    for card in cardList:
        #initialize and append base data values
        cardID = card.find("dd", {"class":"cardNum"}).string
        cardName = card.find("dd", {"class":"cardName"}).string
        cardCategory = [text for text in card.find("dl", {"class":"attributeCol"}).dd.stripped_strings]
        cardAP = card.find("dl", {"class":"appealPointCol"}).dd.string
        cardType = card.find("dl", {"class":"typeCol"}).dd.img.attrs.get("alt")
        cardRarity = list(card.find("dl", {"class":"rarelityCol"}).dd.stripped_strings)
        cardAppeal = card.find("dl", {"class":"dapEffectCol"}).dd.string
        cardLink = card.find("dl", {"class":"cardImgCol"}).dd.img.attrs.get("src")[3:]
        cardOut = f'https://www.aikatsu.com/friends/{cardLink}'

        #data that needs to be filtered goes here
        if card.find("dl", {"class":"brandCol"}).dd.img:
            cardBrand = card.find("dl", {"class":"brandCol"}).dd.img.attrs.get("alt") # SOME Common rarity cards do not have an image for their brand data
        else:
            cardBrand = card.find("dl", {"class":"brandCol"}).dd.string.split()

        if card.find("dl", {"class":"noteTxtCol"}):
            cardRemarks = card.find("dl", {"class":"noteTxtCol"}).dd.string #Only for Promotional Cards / Full Coordinate Cards
        else:
            cardRemarks = "None"

        #compile data as dictionary for json exporting
        cardExport = {
            'ID': cardID,
            'RarityFull': cardRarity[0],
            'RarityFig': cardRarity[1],
            'Category': cardCategory,
            'Name': cardName,
            'Brand': cardBrand,
            'Type': cardType,
            'Appeal': cardAppeal,
            'Points': cardAP,
            'Notes': cardRemarks,
            'imgLink': cardOut
            }

        cardData.append(cardExport)

    #Write Operations
    outData = json.dumps(cardData,ensure_ascii=False)
    export.write(outData)
    export.close()

def GenerateIdolCard():
    webLink = 'https://www.aikatsu.com/friends/cardlist/idolcard.php?search=true&category=458004'
    game = 'データカードダスアイカツフレンズ!'
    cardData = []

    #friends = BeautifulSoup(open(BASE_DIR / "Sample_Data" / "Friends" / "friends.html", encoding="utf-8"), 'html.parser')
    friends = BeautifulSoup(requests.get(webLink).content, 'html.parser')
    export = open(BASE_DIR / "Database" / "friends" / "friends_Data-IdolCard.json", 'w', encoding='utf-8')
    cardList = friends.find_all("div", class_=re.compile("data page"))
    title = friends.find("div", {"id":"titCol"}).h3.img.attrs.get('alt')
    print(f'Generating Card Database: {game} {title}')

    for card in cardList:
        #initialize and append base data values
        cardID = card.find("dd", {"class":"cardNum"}).string
        cardName = card.find("dd", {"class":"cardName"}).string
        cardCode = card.find("dd", {"class":"codeTxt"}).string
        cardNote = [text for text in card.find("dd", {"class":"noteTxt"}).stripped_strings]
        cardLink = card.find("dl", {"class":"cardImgCol"}).dd.img.attrs.get("src")[3:]
        cardOut = f'https://www.aikatsu.com/friends/{cardLink}'

        #compile data as dictionary for csv exporting
        cardExport = {
            'ID': cardID,
            'Name': cardName,
            'Code': cardCode,
            'Note': cardNote,
            'imgLink':cardOut
            }

        cardData.append(cardExport)

    #Write Operations
    outData = json.dumps(cardData,ensure_ascii=False, indent = 3)
    export.write(outData)
    export.close()
