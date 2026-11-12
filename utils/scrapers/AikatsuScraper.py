from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import json
from lxml import etree

BASE_DIR = Path(__file__).resolve().parents[2]

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

def rarity(cardID, cardRarity):
    match cardRarity:
        case "ノーマル":
            return f"{cardID} N"
        case "レア":
            return f"{cardID} R"
        case "プレミアムレア":
            if cardID[:2] in ["01", "02", "03", "04", "05", "06"]:
                return f"{cardID} P"
        case _:
            return cardID
        
def Generate(link, series):
    webLink = f'https://card.aikatsu.net/cardlist/index.php?search=true&category={link}'
    game = 'データカードダスアイカツ!'
    cardData = []

    if (BASE_DIR / "utils" / "scrapers" / "scrapedata" / "aikatsu" / f"aikatsu_Data-{series}.json").is_file():
        file = BASE_DIR / "utils" / "scrapers" / "scrapedata" / "aikatsu" / f"aikatsu_Data-{series}.json"

        if file.stat().st_size != 0:
            print("Database exists! Scraping next cardset...")
            return  
        
    OGKatsu = BeautifulSoup(requests.get(webLink).content, 'html.parser')  
        
    export = open(BASE_DIR / "utils" / "scrapers" / "scrapedata" / "aikatsu" / f"aikatsu_Data-{series}.json", 'w', encoding='utf-8')
    cardList = OGKatsu.find_all("div", {"class": "card"})
    title = OGKatsu.find("section", {"id":"contents"}).h3.img.attrs.get('alt') #change this
    print(f'({series}) Generating Card Database: {game} {title}')

    #SCRAPING DATA EHRE
    for cardLst in cardList:
        cardID = cardLst.table.tr.th.contents[0].string.strip()
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

        cardLink = details[2].contents[1].img.attrs.get("src")
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
            cardRemarks = "-"

        if not rowA[0].string:
            cardType = findCardType(rowA[0].img.attrs.get("src")[16:])

        if not rowA[1].string:
            cardCategory = findCardCategory(rowA[1].img.attrs.get("src")[16:])
        
        if not rowA[2].string:
            cardBrand = findCardBrand(rowA[2].img.attrs.get("src")[16:])

        if not rowB[1].string:
            cardStar = findCardLuckyStar(rowB[1].img.attrs.get("src")[16:])

        if len(rowB) == 3:
            if checkrow[-1].string == "星座":
                if not rowB[2].string:
                    cardConstellation = findCardConstellation(rowB[2].img.attrs.get("src")[16:])
            elif checkrow[-1].string == "ロマンス・ドリーム":
                if not rowB[2].string:
                    cardRomanceDream = findCardRomanceDream(rowB[2].img.attrs.get("src")[16:])
        else:
            if series != "215022":
                if not rowB[2].string:
                    cardBoom = findCardBoom(rowB[2].img.attrs.get("src")[16:])
                if not rowB[3].string:
                    cardFever = True
            else:
                if not rowB[2].string:
                    cardConstellation = findCardConstellation(rowB[2].img.attrs.get("src")[16:])
                    cardRomanceDream = findCardRomanceDream(rowB[2].img.attrs.get("src")[16:])
                    cardBoom = findCardBoom(rowB[2].img.attrs.get("src")[16:])

        lookACompat = True if details[0].find("span", {"class":"icon-aktphonelook"}) else False
        lookBCompat = True if details[0].find("span", {"class":"icon-aktphonelook2"}) else False
        phoneCompat = True if details[0].find("span", {"class":"icon-aktphone"}) else False
        

        #compile data as dictionary for csv exporting
        cardExport = {
            'ID': rarity(cardID),
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
            'QR': '', #todo
            'imgLink': cardOut
            }

        cardData.append(cardExport)

    #Write Operations
    outData = json.dumps(cardData,ensure_ascii=False, indent = 3)
    export.write(outData)
    export.close()