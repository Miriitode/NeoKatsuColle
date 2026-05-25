from bs4 import BeautifulSoup
import requests
import os
import re
import json
from pathlib import Path
import unicodedata

BASE_DIR = Path(__file__).resolve().parents[2]

fw = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" \
     "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ" \
     "０１２３４５６７８９"

ascii_ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
         "abcdefghijklmnopqrstuvwxyz" \
         "0123456789"

table = str.maketrans(fw, ascii_)

unidentify = []
assoc_Unique = []
assoc_Info = {}

def patch(patchData, series, subnum, is_promote=False):
    if not is_promote:
        asc = subnum
    else:
        match series:
            case 'aikatsu':
                asc = '22'

    with open(BASE_DIR / "Database" / series / "CardList" / f'{series}_Data-{asc}.json', 'r', encoding='utf-8') as file:
        cards = json.load(file)

    with open(BASE_DIR / "Database" / series / "CardList" / f'{series}_Data-{asc}.json', 'w', encoding='utf-8') as file:
        for card in cards:
            found = False
            for patch in patchData.keys():
                test1 = unicodedata.normalize("NFKC", patch)
                test2 = card['Name']
                test3 = patchData[patch]['ID']
                test4 = card['ID']
                # if not is_promote:
                #     if test2 == test1:
                #         found = True
                #         # print(f"Detected! | {card['Name']}")
                #         if 'http://aikatsu.com/qr/id=' not in patchData[patch]['QR']:
                #             print(f'[WARN] {card['Name']} has no QR code')
                #         else:
                #             card['Barcode'] = patchData[patch]['Barcode']
                #             card['QR'] = patchData[patch]['QR']
                # else:
                #     if test4 == test3:
                #         found = True
                #         # print(f"Detected! | {card['Name']}")
                #         if 'http://aikatsu.com/qr/id=' not in patchData[patch]['QR']:
                #             print(f'[WARN] {card['Name']} has no QR code')
                #         else:
                #             card['Barcode'] = patchData[patch]['Barcode']
                #             card['QR'] = patchData[patch]['QR']

                #match by name
                if test4 == test3:
                    found = True
                    # print(f"Detected! | {card['Name']}")
                    if 'http://aikatsu.com/qr/id=' not in patchData[patch]['QR']:
                        print(f'[WARN] {card['Name']} has no QR code')
                    else:
                        card['Barcode'] = patchData[patch]['Barcode']
                        card['QR'] = patchData[patch]['QR']
        
            if not found:
                unidentify.append(f'{card['ID']} | {card['Name']}')

        json.dump(cards, file, ensure_ascii=False, indent=3)

def Generate(link, series, subnum, is_promote=False):
    if not is_promote:
        assoc_Info.clear() 

    qrList = BeautifulSoup(requests.get(link).content, 'html.parser')

    info_sifted = qrList.find_all("tr", class_=re.compile(r'^row-\d+$'))

    for card in info_sifted:
        elem_Id = card.find("td", class_="column-1")
        if elem_Id:
            card_Id = elem_Id.find("font")
        else:
            # print("INVALID ENTRY")
            ...

        card_Name = card.find("td", class_="column-3")
        card_Bar = card.find("td", class_="column-4")
        elem_Qr = card.find("td", class_="column-5")

        if elem_Qr:
            card_Qr = elem_Qr.find('input') 
        else:
            # print("INVALID ENTRY")
            ...

        if card_Name and card_Bar and card_Qr:
            # print(f'{card_Id.text} | {card_Name.text} | {card_Bar.text} | {card_Qr['value']}')
            if card_Name.text.strip() not in assoc_Unique:
                assoc_Unique.append(card_Name.text.strip())
                assoc_Info[card_Name.text.strip()] = {
                    'ID': card_Id.text,
                    'Barcode': card_Bar.text,
                    'QR': card_Qr['value']
                    }
        else:
            # print("INVALID ENTRY")
            ...

    if not is_promote:
        with open(BASE_DIR / "utils" / "scrapers" / "qr_Data" / series / f'aikatsu_QRData-{subnum}.json', 'w', encoding='utf-8') as data:
            export = json.dumps(assoc_Info,ensure_ascii=False,indent=3)
            data.write(export)

# For testing
# Generate('https://pokehunngry.com/266.html', 'aikatsu', 0)

aikatsu = [
    '266', #2013 series part 1
    '839', #2013 series part 2
    '859', #2013 series part 3
    '885', #2013 series part 4
    '888', #2013 series part 5
    '892', #2013 series part 6
    '942', #2014 series part 1
    '1090', #2014 series part 2
    '1239', #2014 series part 3
    '1303', #2014 series part 4
    '1438', #2014 series part 5
    '1696', #2014 series part 6
    '3953', #2015 series part 1
    '4548', #2015 series part 2
    '5396', #2015 series part 3
    '5991', #2015 series part 4
    '6332', #2015 series part 5
    '6735', #2015 series part 6
    '6941', #2016 series part 1
    '7590', #2016 series part 2
    '7805', #2016 series part 3
    '8066', #2016 series part 4
]

aikatsu_promote = [
    '734', #Collectible toys / food items
    '464', #Tournaments / events / campaigns
    '376', #Magazines / other publications
    '552', #Gashapon / prize related
    '761', #Misc
    '703', #Apparel / Aikatsu style merch
    '583', #CD / DVD / DS game promo
]

def scrape_QR():
    for i, j in enumerate(aikatsu):
        # print(f'Aikatsu {i}')
        Generate(f'https://pokehunngry.com/{j}.html', 'aikatsu', i)

    for i, j in enumerate(aikatsu_promote):
        # print(f'Aikatsu Promo {i}')
        Generate(f'https://pokehunngry.com/{j}.html', 'aikatsu', 22, is_promote=True)
        with open(BASE_DIR / "utils" / "scrapers" / "qr_Data" / 'aikatsu' / f'aikatsu_QRData-22.json', 'w', encoding='utf-8') as data:
            export = json.dumps(assoc_Info,ensure_ascii=False,indent=3)
            data.write(export)

def patch_QR():
    for i, _ in enumerate(aikatsu):
        with open(BASE_DIR / "utils" / "scrapers" / "qr_Data" / 'aikatsu' / f'aikatsu_QRData-{i}.json', 'r', encoding='utf-8') as data:
            assoc = json.load(data)
            patch(assoc, 'aikatsu', i, False)

    with open(BASE_DIR / "utils" / "scrapers" / "qr_Data" / 'aikatsu' / f'aikatsu_QRData-{22}.json', 'r', encoding='utf-8') as data:
        assoc = json.load(data)
    patch(assoc, 'aikatsu', 22, True)
    

print('Warning! This script will modify the current database json files to include QR and Barcodes. This will take a while. Continue? (Press Y to continue)')

arg = input()

if arg.lower() == 'y':
    # scrape_QR()
    patch_QR()
else:
    quit()

if len(unidentify) > 0:
    warning = (
        "[WARN] The scraper has not resolved the following cards. "
        "This is due to name text mismatches from the QR code library "
        "and the Database library. Please locate the missing codes in "
        "the generated json files and add them to the database manually."
    )

    note = (
        "Note: This does not track unadded promotional cards. "
        "Please check manually."
    )

    print(warning)
    print(note)

    report_path = BASE_DIR / "utils" / "scrapers" / "unidentified_cards.txt"

    with open(report_path, "w", encoding="utf-8") as report:
        report.write(warning + "\n")
        report.write(note + "\n\n")

        for mismatch in unidentify:
            print(mismatch)
            report.write(mismatch + "\n")

    print(f"\nReport written to: {report_path}")

