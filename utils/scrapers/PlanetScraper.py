from bs4 import BeautifulSoup
import requests
import os
import re
import json
from lxml import etree

def Generate(link, series):
    '''
    Generates a card database for the game Aikatsu Planet!

    Scrapes a given card list link for the specific series and compiles the data into two 'csv' files. One for the card list data, another for the card image links.

    Can be configured to only generate the card list, or card image links. (TODO)

    Args:
        link (string): A link to the card list to scrape
        series (int): The series identifier used in the output file

    Returns:
        None
    '''

    webLink = f'https://www.aikatsu.com/planet/swinglist/?search=true&category={link}'
    game = 'データカードダスアイカツプラネット!'
    cardData = []
    imgData = []
    #TODO: maybe replace some elements that make use of the alt tag from <img> with their image counterparts instead
    #though this might increase the workload in obtaining assets, but would make the UX Design of the application way better.

    if os.path.isfile(os.path.join(os.getcwd(),f'Database/planet/CardList/Planet_Data-{series}.json')):
        file = os.path.join(os.getcwd(),f'Database/planet/CardList/Planet_Data-{series}.json')

        if os.stat(file).st_size != 0:
            print("Database exists! Scraping next cardset...")
            return

    #planet = BeautifulSoup(open(os.path.join(os.getcwd(), "Sample_Data/Planet/planet.html"), encoding="utf-8"), 'html.parser') #temporary
    planet = BeautifulSoup(requests.get(webLink).content, 'html.parser')
        
    export = open(os.path.join(os.getcwd(),f'Database/planet/CardList/Planet_Data-{series}.json'), 'w', encoding='utf-8')
    img = open(os.path.join(os.getcwd(),f'Database/planet/ImgList/Planet_Img-{series}.json'), 'w', encoding='utf-8')
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
        
        #compile data as dictionary for json exporting
        imgExport = {
             'imgFront': f'{cardID} Front',
             'frontLink': cardImg[0],
             'imgBack': f'{cardID} Back',
             'backLink': cardImg[1],
            }

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
            }

        imgData.append(imgExport)
        cardData.append(cardExport)

    #Write Operations
    outImg = json.dumps(imgData, indent = 3)
    outData = json.dumps(cardData,ensure_ascii=False, indent = 3)
    img.write(outImg)
    export.write(outData)
    export.close()
    img.close()