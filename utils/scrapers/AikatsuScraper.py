from bs4 import BeautifulSoup
import requests
import os
import re
import json
from lxml import etree

def findCardType(input):
    if input == "icon-tycute.jpg":
        return "キュート"
    elif input == "icon-tycool.jpg":
        return "クール"
    elif input == "icon-tysexy.jpg":
        return "セクシー"
    elif input == "icon-typop.jpg":
        return "ポップ"
    return

def findCardCategory(input):
    if input == "icon-cttops.jpg":
        return "トップス"
    elif input == "icon-ctbottoms.jpg":
        return "ボトムス"
    elif input == "icon-ctshoes.jpg":
        return "シューズ"
    elif input == "icon-cttb.jpg":
        return "トップス ＆ ボトムス"
    elif input == "icon-ctaccessory.jpg":
        return "アクセサリー"
    return

def findCardBrand(input):
    if input == "icon-bras.jpg":
        return "エンジェリーシュガー"
    elif input == "icon-brfg.jpg":
        return "フューチャーリングガール"
    elif input == "icon-brsa.jpg":
        return "スパイシーアゲハ"
    elif input == "icon-brhr.jpg":
        return "ハッピーレインボー"
    elif input == "icon-brlg.jpg":
        return "ロリゴシック"
    elif input == "icon-braf.jpg":
        return "オーロラファンタジー"
    elif input == "icon-brlq.jpg":
        return "ラブクイーン"
    elif input == "icon-brmt.jpg":
        return "マジカルトイ"
    elif input == "icon-brsr.jpg":
        return "スイングロック"
    elif input == "icon-brbs.jpg":
        return "ボヘミアンスカイ"
    elif input == "icon-brlm.jpg":
        return "ラブムーンライズ"
    elif input == "icon-brvk.jpg":
        return "ヴィヴィッドキス"
    elif input == "icon-brdc.jpg":
        return "ドリーミークラウン"
    elif input == "icon-brro.jpg":
        return "サングリアロッサ"
    elif input == "icon-brsc.jpg":
        return "桜色花伝"
    elif input == "icon-brdf.jpg":
        return "ダンスフュージョン"
    elif input == "icon-brrc.jpg":
        return "レトロクローバー"
    elif input == "icon-brdd.jpg":
        return "ドーリーデビル"
    elif input == "icon-brmp.jpg":
        return "メチャパニック"
    else:
        raise Exception(f'Brand not implemented: {input}')
    
def findCardLuckyStar(input):
    if input == "icon-rs0.jpg":
        return "☆☆☆"
    elif input == "icon-rs1.jpg":
        return "★☆☆"
    elif input == "icon-rs2.jpg":
        return "★★☆"
    elif input == "icon-rs3.jpg":
        return "★★★"
    return

def findCardConstellation(input):
    if input == "icon-clscorpio.jpg":
        return "さそり座"
    elif input == "icon-clleo.jpg":
        return "しし座"
    elif input == "icon-clpisces.jpg":
        return "うお座"
    elif input == "icon-cllibra.jpg":
        return "てんびん座"
    elif input == "icon-clsagittarius.jpg":
        return "いて座"
    elif input == "icon-claries.jpg":
        return "おひつじ座"
    elif input == "icon-claquarius.jpg":
        return "みずがめ座"
    elif input == "icon-clvirgo.jpg":
        return "おとめ座"
    elif input == "icon-cltaurus.jpg":
        return "おうし座"
    elif input == "icon-clcapricorn.jpg":
        return "やぎ座"
    elif input == "icon-clcancer.jpg":
        return "かに座"
    elif input == "icon-clgemini.jpg":
        return "ふたご座"
    elif input == "icon-clgemini.jpga":
        return "ふたご座"
    else:
        return "-"
    # raise Exception(f'Constellation not implemented: {input}')

def findCardRomanceDream(input):
    if input == "icon-rmsl.jpg":
        return "Swan Lake"
    elif input == "icon-rmsw.jpg":
        return "Snow White"
    elif input == "icon-rmnc.jpg":
        return "The Nutcracker"
    elif input == "icon-rmcd.jpg":
        return "Snow White"
    elif input == "icon-rmsb.jpg":
        return "Sleeping Beauty"
    elif input == "icon-rmtb.jpg":
        return "Thumbelina"
    elif input == "icon-rmlm.jpg":
        return "The Little Mermaid"
    elif input == "icon-rmbc.jpg":
        return "The Tale of the Bamboo Cutter"
    elif input == "icon-drap.jpg":
        return "Alice in Wonderland"
    elif input == "icon-drmh.jpg":
        return "Pinocchio"
    elif input == "icon-drnj.jpg":
        return "Peter Pan"
    elif input == "icon-draf.jpg":
        return "Arabian Nights"
    elif input == "icon-drst.jpg":
        return "Hansel and Gretel"
    elif input == "icon-drbo.jpg":
        return "Town Musicians of Bremen"
    elif input == "icon-drom.jpg":
        return "The Wizard of Oz"
    else:
        return "-"
    # raise Exception(f'Romance / Dream not implemented: {input}')

def findCardBoom(input):
    if input == "icon-jewelry.jpg":
        return "Jewelry"
    elif input == "icon-party.jpg":
        return "Party"
    else:
        return "-"
    # raise Exception(f'Boom not implemented: {input}')

def Generate(link, series):
    '''
    Generates a card database for the game Aikatsu!

    Scrapes a given card list link for the specific series and compiles the data into two 'csv' files. One for the card list data, another for the card image links.

    Can be configured to only generate the card list, or card image links. (TODO)

    Args:
        link (string): A link to the card list to scrape
        series (int): The series identifier used in the output file

    Returns:
        None
    '''

    webLink = f'https://www.aikatsu.com/cardlist/index.php?search=true&category={link}'
    game = 'データカードダスアイカツ!'
    cardData = []
    imgData = []

    if os.path.isfile(os.path.join(os.getcwd(),f'Database/aikatsu/CardList/OGKatsu_Data-{series}.json')):
        file = os.path.join(os.getcwd(),f'Database/aikatsu/CardList/OGKatsu_Data-{series}.json')

        if os.stat(file).st_size != 0:
            print("Database exists! Scraping next cardset...")
            return  
        
    OGKatsu = BeautifulSoup(requests.get(webLink).content, 'html.parser')  
        
    export = open(os.path.join(os.getcwd(),f'Database/aikatsu/CardList/OGKatsu_Data-{series}.json'), 'w', encoding='utf-8')
    img = open(os.path.join(os.getcwd(),f'Database/aikatsu/ImgList/OGKatsu_Img-{series}.json'), 'w', encoding='utf-8')
    cardList = OGKatsu.find_all("div", {"class": "card"})
    title = OGKatsu.find("section", {"id":"contents"}).h3.img.attrs.get('alt') #change this
    print(f'({series}) Generating Card Database: {game} {title}')

    #SCRAPING DATA EHRE
    for cardLst in cardList:
        cardID = cardLst.table.attrs.get("id")
        details = [x for x in cardLst.table.contents if x != '\n']
        rowA = [x for x in details[3].contents if x != '\n']
        rowB = [x for x in details[5].contents if x != '\n']
        rowC = [x for x in details[7].contents if x != '\n']
        checkrow = [x for x in details[4].contents if x != '\n']

        cardName = details[1].contents[3].string
        # cardType = cardLst.table.attrs.get("class")[0][5:]
        cardRarity = rowB[0].string
        cardAppeal = rowC[0].string
        cardAP = rowC[1].string

        cardLink = details[2].contents[1].img.attrs.get("src")[3:]
        #cardOut = f'https://www.aikatsu.com/{cardLink}'
        cardOut = f'https://card.aikatsu.net/cardlist/{cardLink}' #cannot access images through the old website directly
        

        cardType = "-"
        cardCategory = "-"
        cardBrand = "-"
        cardStar = "-"
        cardConstellation = "-"
        cardRomanceDream = "-"
        cardBoom = "-"
        cardFever = False

        if len(details) > 8:
            if details[-1].td.string:
                cardRemarks = details[-1].td.string
            else:
                cardRemarks = details[-1].td.text
        else:
            cardRemarks = "None"

        if not rowA[0].string:
            cardType = findCardType(rowA[0].img.attrs.get("src")[19:])

        if not rowA[1].string:
            cardCategory = findCardCategory(rowA[1].img.attrs.get("src")[19:])
        
        if not rowA[2].string:
            cardBrand = findCardBrand(rowA[2].img.attrs.get("src")[19:])

        if not rowB[1].string:
            cardStar = findCardLuckyStar(rowB[1].img.attrs.get("src")[19:])

        if len(rowB) == 3:
            if checkrow[-1].string == "星座":
                if not rowB[2].string:
                    cardConstellation = findCardConstellation(rowB[2].img.attrs.get("src")[19:])
            elif checkrow[-1].string == "ロマンス・ドリーム":
                if not rowB[2].string:
                    cardRomanceDream = findCardRomanceDream(rowB[2].img.attrs.get("src")[19:])
        else:
            if series != "215022":
                if not rowB[2].string:
                    cardBoom = findCardBoom(rowB[2].img.attrs.get("src")[19:])
                if not rowB[3].string:
                    cardFever = True
            else:
                if not rowB[2].string:
                    cardConstellation = findCardConstellation(rowB[2].img.attrs.get("src")[19:])
                    cardRomanceDream = findCardRomanceDream(rowB[2].img.attrs.get("src")[19:])
                    cardBoom = findCardBoom(rowB[2].img.attrs.get("src")[19:])

        lookACompat = True if details[0].find("span", {"class":"icon-aktphonelook"}) else False
        lookBCompat = True if details[0].find("span", {"class":"icon-aktphonelook2"}) else False
        phoneCompat = True if details[0].find("span", {"class":"icon-aktphone"}) else False
        

        #compile data as dictionary for csv exporting
        cardExport = {
            'ID': cardID,
            'Rarity': cardRarity,
            'Category': cardCategory,
            'Name': cardName,
            'Brand': cardBrand,
            'Type': cardType,
            'Appeal': cardAppeal,
            'Points': cardAP,
            'LuckyStar': cardStar,
            'Constellation': cardConstellation,
            'Romance': cardRomanceDream,
            'BOOM': cardBoom,
            'Fever': cardFever,
            'Notes': cardRemarks,
            'PhoneCompat': phoneCompat,
            'Look1Compat': lookACompat,
            'Look2Compat': lookBCompat,
            'Barcode': '', #todo
            'QR': '' #todo
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