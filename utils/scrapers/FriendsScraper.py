from bs4 import BeautifulSoup
import requests
import os
import re
import json
from lxml import etree

def Generate(link, series):
    '''
    Generates a card database for the game Aikatsu Friends!

    Scrapes a given card list link for the specific series and compiles the data into two 'csv' files. One for the card list data, another for the card image links.

    Can be configured to only generate the card list, or card image links. (TODO)

    Args:
        link (string): A link to the card list to scrape
        series (int): The series identifier used in the output file

    Returns:
        None
    '''
    webLink = f'https://www.aikatsu.com/friends/cardlist/?search=true&category={link}'
    game = 'データカードダスアイカツフレンズ!'
    cardData = []
    imgData = []

    if os.path.isfile(os.path.join(os.getcwd(),f'Database/friends/CardList/Friends_Data-{series}.json')):
        file = os.path.join(os.getcwd(),f'Database/friends/CardList/Friends_Data-{series}.json')

        if os.stat(file).st_size != 0:
            print("Database exists! Scraping next cardset...")
            return
        
    #friends = BeautifulSoup(open(os.path.join(os.getcwd(), "Sample_Data/Friends/friends.html"), encoding="utf-8"), 'html.parser')
    friends = BeautifulSoup(requests.get(webLink).content, 'html.parser')
    export = open(os.path.join(os.getcwd(),f'Database/friends/CardList/Friends_Data-{series}.json'), 'w', encoding='utf-8')
    img = open(os.path.join(os.getcwd(),f'Database/friends/ImgList/Friends_Img-{series}.json'), 'w', encoding='utf-8')
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
            }
        
        imgExport = {
            'imgFile':cardID,
            'imgLink':cardOut,
            }

        cardData.append(cardExport)
        imgData.append(imgExport)

    #Write Operations
    outImg = json.dumps(imgData)
    outData = json.dumps(cardData,ensure_ascii=False)
    img.write(outImg)
    export.write(outData)
    export.close()
    img.close()

def GenerateIdolCard():
    '''
    Generates a card database for the Idol Cards in the game Aikatsu Friends!

    Can be configured to only generate the card list, or card image links. (TODO)

    Args:
        None

    Retuns:
        None
    '''
    webLink = 'https://www.aikatsu.com/friends/cardlist/idolcard.php?search=true&category=458004'
    game = 'データカードダスアイカツフレンズ!'
    cardData = []
    imgData = []

    #friends = BeautifulSoup(open(os.path.join(os.getcwd(), "Sample_Data/Friends/friends.html"), encoding="utf-8"), 'html.parser')
    friends = BeautifulSoup(requests.get(webLink).content, 'html.parser')
    export = open(os.path.join(os.getcwd(),f'Database/friends/CardList/Friends_Data-IdolCard.json'), 'w', encoding='utf-8')
    img = open(os.path.join(os.getcwd(),f'Database/friends/ImgList/Friends_Img-IdolCard.json'), 'w', encoding='utf-8')
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
            }
        
        imgExport = {
            'imgFile':cardID,
            'imgLink':cardOut,
            }

        cardData.append(cardExport)
        imgData.append(imgExport)

    #Write Operations
    outImg = json.dumps(imgData, indent = 3)
    outData = json.dumps(cardData,ensure_ascii=False, indent = 3)
    img.write(outImg)
    export.write(outData)
    export.close()
    img.close()
