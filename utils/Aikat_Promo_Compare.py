import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

file_a = open(BASE_DIR / "Database" / "Aikatsu" / "CardList" / "aikatsu_Data-22.json", 'r', encoding='utf-8')
file_b = open(BASE_DIR / "utils" / "scrapers" / "qr_Data" / "aikatsu" / "aikatsu_QRData-22.json", 'r', encoding='utf-8')

main_Data = json.load(file_a)
qr_Data = json.load(file_b)

print(f'main_Database Count: {len(main_Data)}')
print(f'qr_Database Count: {len(qr_Data)}')

for i in qr_Data:
    found = False
    for j in main_Data:
        # if qr_Data[i]['ID'] == j['ID']:
        #     found = True
        if i == j['Name']:
            found = True
    
    if not found:
        print(f"Main Database does not have {qr_Data[i]['ID']}")

# for i in main_Data:
#     found = False
#     for j in qr_Data:
#         # if qr_Data[j]['ID'] == i['ID']:
#         #     found = True
#         if j == i['Name']:
#             found = True
    
#     if not found:
#         print(f"QR Database does not have {i['ID']}")
