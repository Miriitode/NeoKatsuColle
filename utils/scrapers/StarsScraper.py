from bs4 import BeautifulSoup
import requests
import os
import re
import json
from lxml import etree

def Generate(link, series):
    # This might be the most complicated scraper I ever have to do...
    # Cause unlike the other websites, each card has only full details on a separate page.....
    # fetching requests for each specific card is extremely slow...
    webLink = f'https://www.aikatsu.com/stars/cardlist/dresslist.php?search=true&category={link}'
    game = 'データカードダスアイカツスターズ!'
    cardData = []
    imgData = []
    s = requests.session()
    stars = BeautifulSoup(s.get(webLink).content, 'lxml')

    if os.path.isfile(os.path.join(os.getcwd(),f'Database/stars/CardList/Stars_Data-{series}.json')):
        file = os.path.join(os.getcwd(),f'Database/stars/CardList/Stars_Data-{series}.json')

        if os.stat(file).st_size != 0:
            print("Database exists! Scraping next cardset...")
            return

    export = open(os.path.join(os.getcwd(),f'Database/stars/CardList/Stars_Data-{series}.json'), 'w', encoding='utf-8')
    
    img = open(os.path.join(os.getcwd(),f'Database/stars/ImgList/Stars_Img-{series}.json'), 'w', encoding='utf-8')
    cardList = stars.find("div", {"id":"list"}).find_all("a")
    title = stars.find("h3", {"id":"title"}).img.attrs.get("alt")
    print(f'({series}) Generating Card Database: {game} {title}')

    for cardLst in cardList:
        cardo = f'https://www.aikatsu.com/stars/cardlist/{cardLst.attrs.get("href")}'
        indiv_Card = BeautifulSoup(s.get(cardo).content, 'lxml') 
        card = indiv_Card.find("div", {"id":"list"})

        cardGrade = None
        cardRemark = None
        cardAPP = None

        cardTitle = card.find("div", {"class": "dress-detail-title clearfix"})
        # cardTable = card.find("div", {"class": "dress-detail clearfix"})
        
        if "星のツバサ" in title:
            brand = card.find("li", {"class":"brand"})
            cardID = cardTitle.p.string
            cardName = cardTitle.h4.string
            cardType = card.find("li", {"class":"type"}).dl.dd.img.attrs.get("alt")
            cardCategory = card.find("li", {"class":"category"}).dl.dd.string
            cardRarity = card.find("li", {"class":"reality"}).dl.dd.contents[0]
            cardAppeal = card.find("li", {"class":"dressappeal"}).dl.dd.string
            cardAP = card.find("li", {"class":"appealpoint"}).dl.dd.string.strip()
            cardAPP = card.find("li", {"class":"appealpoint_plus"}).dl.dd.string.strip()
            cardLink = card.find("img", {"class": "dress-detail-card_img"}).attrs.get("src")[3:]
            cardOut = f'https://www.aikatsu.com/stars/{cardLink}'

            if brand.dl.dd.img:
                cardBrand = brand.dl.dd.img.attrs.get("alt")
            else:
                cardBrand = brand.dl.dd.string.strip()
        else:
            cardAttrs = card.find("div", {"class": "dress-detail-data"}).div.table.find_all("tr") #This breaks on Hoshi no Tsubasa cardsets
            cardRemark = card.find("div", {"class":"dress-detail-remarks"}).div.p.string
            cardLink = card.find("img", {"class": "dress-detail-card_img"}).attrs.get("src")[3:]
            cardOut = f'https://www.aikatsu.com/stars/{cardLink}'
            
            attrA = cardAttrs[1]
            attrB = cardAttrs[3]
            brand = card.find("div", {"class": "dress-detail-brand"})

            cardID = cardTitle.p.string
            cardName = cardTitle.h4.string
            cardType = attrA.contents[1].img.attrs.get("alt")
            cardCategory = attrA.contents[3].string
            cardRarity = attrA.contents[5].string
            cardAppeal = attrB.contents[1].string
            cardAP = attrB.contents[3].string

            if attrB.contents[5].img:
                cardGrade = attrB.contents[5].img.attrs.get("alt")
            else:
                cardGrade = attrB.contents[5].string.strip()
        
            if brand.div.img:
                cardBrand = brand.div.img.attrs.get("alt")
            else:
                cardBrand = brand.div.p.string.strip()

        #compile data as dictionaries for json exporting

        cardExport = {
            'ID': cardID,
            'Rarity': cardRarity,
            'Category': cardCategory,
            'Name': cardName,
            'Brand': cardBrand,
            'Type': cardType,
            'Appeal': cardAppeal,
            'Points': cardAP,
        }

        if cardGrade:
            cardExport['Upgrade'] = True
        else:
            cardExport['Upgrade'] = False

        if cardRemark:
            cardExport['Notes'] = cardRemark
        else:
            cardExport['Notes'] = 'None'

        if cardAPP:
            cardExport['Plus'] = cardAPP
        else:
            cardExport['Plus'] = '-'


        imgExport = {
            'imgFile': cardID,
            'imgLink': cardOut,
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