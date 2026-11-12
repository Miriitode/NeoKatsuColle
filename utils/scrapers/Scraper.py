import time
from pathlib import Path
import PlanetScraper as PlanetScraper
import ParadeScraper as ParadeScraper
import FriendsScraper as FriendsScraper
import StarsScraper as StarsScraper
import AikatsuScraper as AikatsuScraper
from qrScraper import patch_QR

BASE_DIR = Path(__file__).resolve().parents[2]

ogkatsuList = [
    '215001', # 2013 Series Part 1
    '215002', # 2013 Series Part 2
    '215003', # 2013 Series Part 3
    '215004', # 2013 Series Part 4
    '215005', # 2013 Series Part 5
    '215006', # 2013 Series Part 6
    '215007', # 2014 Series Part 1
    '215008', # 2014 Series Part 2
    '215009', # 2014 Series Part 3
    '215010', # 2014 Series Part 4
    '215011', # 2014 Series Part 5
    '215012', # 2014 Series Part 6
    '215013', # 2015 Series Part 1
    '215014', # 2015 Series Part 2
    '215015', # 2015 Series Part 3
    '215016', # 2015 Series Part 4
    '215017', # 2015 Series Part 5
    '215018', # 2015 Series Part 6
    '215019', # 2016 Series Part 1
    '215020', # 2016 Series Part 2
    '215021', # 2016 Series Part 3
    '215022', # 2016 Series Part 4
    '215901', # Promotional Cards
]

starsList = [
    "391000", # Four Star Academy Basic Dress
    "391001", # 1st Season: Spring
    "391002", # 2nd Season: Summer
    "391003", # 3rd Season: Autumn
    "391004", # 4th Season: Winter
    "391005", # 5th Season: S4 Selection
    "391101", # Hoshi no Tsubasa 1
    "391102", # Hoshi no Tsubasa 2
    "391103", # Hoshi no Tsubasa 3
    "391104", # Hoshi no Tsubasa 4
    "391105", # Hoshi no Tsubasa 5
    "391106", # Hoshi no Tsubasa 6
    "391801", # Hoshi no Tsubasa Promotional Cards
    "391901", # Promotional Cards
    "391902", # Promotional Cards 2
]

friendsList = [
    "458001", # Series 1
    "458002", # Series 2
    "458003", # Series 3
    "458004", # Series 4
    "458005", # Series 5
    "458006", # Series 6
    "458007", # Kagayaki no Jewel 1
    "458008", # Kagayaki no Jewel 2
    "458009", # Kagayaki no Jewel 3
    "458801", # Full Coordinate Cards
    "458901", # Promotional Cards
]

paradeList = [
    "491001", # Series 1
    "491002", # Series 2
    "491003", # Series 3
    "491004", # Dream Stage 1
    "491005", # Dream Stage 2
    "491006", # Dream Stage 3
    "491701", # Arcade Promotional Cards
    "491801", # Full Coordinate Cards
    "491901", # Promotional Cards
]

planetList = [
    '520001', # Series 1
    '520002', # Series 2
    '520003', # Series 3
    '520004', # Series 4
    '520005', # Series 5
    '520006', # Series 6
    '520007', # Unit Stage 1
    '520008', # Unit Stage 2
    '520009', # Unit Stage 3
    '520901', # Promotional Cards
]
    
def aikatsuQR_Warn(unidentify):
    warning = (
        "[WARN | AikatsuScraper.py] The scraper has not resolved the following cards. "
        "This is due to name text mismatches from the QR code library "
        "and the Database library. Please locate the missing codes in "
        "the generated json files and add them to the database manually."
    )

    print(warning)

    report_path = BASE_DIR / "utils" / "scrapers" / "unidentified_cards.txt"

    with open(report_path, "w", encoding="utf-8") as report:
        report.write(warning + "\n")

        for mismatch in unidentify:
            print(mismatch)
            report.write(mismatch + "\n")

    print(f"\nReport written to: {report_path}")

def timer(start, end):
    runtime = round((end - start), 2)
    if runtime < 60:
        return f'{runtime} seconds'
    else:
        return str(round((runtime/60), 2)) + ' minutes'

def Database_Check():
    series = ["aikatsu", "stars", "friends", "parade", "planet"]
    # databaseDir = Path(__file__).resolve().parents[2] / "Database"
    databaseDir = BASE_DIR / "utils" / "scrapers" / "scrapedata"

    for ser in series:
        (databaseDir / ser).mkdir(parents=True, exist_ok=True)

def InitDBScraper():
    Database_Check()

    start = time.perf_counter()
        
    print("[initDB Phase 1] Generating Aikatsu Card List...")
    for i in enumerate(ogkatsuList):
        AikatsuScraper.Generate(i[1], i[0])

    print("[intiDB Phase 1] Generating Aikatsu QR Code List...")
    result = patch_QR()

    print("[initDB Phase 1] Generating Stars Card List...")
    for i in enumerate(starsList):
        StarsScraper.Generate(i[1], i[0])

    print("[initDB Phase 1] Generating Friends Card List...")
    for i in enumerate(friendsList):
        FriendsScraper.Generate(i[1], i[0])
    # FriendsScraper.GenerateIdolCard() 

    print("[initDB Phase 1] Generating Parade Card List...")
    for i in enumerate(paradeList):
        ParadeScraper.Generate(i[1], i[0])

    print("[initDB Phase 1] Generating Planet Card List...")
    for i in enumerate(planetList):
        PlanetScraper.Generate(i[1], i[0])

    end = time.perf_counter()
    print(f'[initDB Phase 1] Scraping Done! Operation took {timer(start, end)}')

    if result:
        aikatsuQR_Warn(result)

def main():

    Database_Check()

    print("input Number to generate card dabase: (input 0 to scrape everything) \n 1 - Data Carddass Aikatsu! \n 2 - Data Carddass Aikatsu Stars! \n 3 - Data Carddass Aikatsu Friends \n 4 - Data Carddass Aikatsu on Parade! \n 5 - Data Carddass Aikatsu Planet!")
    opt = int(input())

    match opt:
        case 0:
            print("WARNING!!! This will generate a card database from EVERY GAME SERIES! \n   This operation will take a few minutes. \n   Type \'YES\' to confirm the operation:")
            confirm = input()
            if confirm == "YES":
                start = time.perf_counter()
                print("Generating Aikatsu Database...")
                for i in enumerate(ogkatsuList):
                    AikatsuScraper.Generate(i[1], i[0])
                result = patch_QR()
                print("Generating Stars Database...")
                for i in enumerate(starsList):
                    StarsScraper.Generate(i[1], i[0])
                print("Generating Friends Database...")
                for i in enumerate(friendsList):
                    FriendsScraper.Generate(i[1], i[0])
                FriendsScraper.GenerateIdolCard()
                print("Generating Parade Database...")
                for i in enumerate(paradeList):
                    ParadeScraper.Generate(i[1], i[0])
                print("Generating Planet Database...")
                for i in enumerate(planetList):
                    PlanetScraper.Generate(i[1], i[0])
            else:
                print("Operation cancelled.")
                main()

        case 1:
            print("Select Series to Scrape, input 0 for all series")
            ogArg = int(input())
            match ogArg:
                case 0:
                    start = time.perf_counter()
                    for i in enumerate(ogkatsuList):
                        AikatsuScraper.Generate(i[1], i[0])
                case _:
                    start = time.perf_counter()
                    AikatsuScraper.Generate(ogkatsuList[ogArg-1], ogArg-1)
        case 2:
            print("Select Series to Scrape, input 0 for all series")
            starsArg = int(input())
            match starsArg:
                case 0:
                    start = time.perf_counter()
                    for i in enumerate(starsList):
                        StarsScraper.Generate(i[1], i[0])
                case _:
                    start = time.perf_counter()
                    StarsScraper.Generate(starsList[starsArg-1], starsArg-1)
        case 3:
            #Fix cases for the idol cards
            print("Select Series to Scrape, input 0 for all series")
            friendsArg = int(input())
            match friendsArg:
                case 0:
                    start = time.perf_counter()
                    for i in enumerate(friendsList):
                        FriendsScraper.Generate(i[1], i[0])

                    FriendsScraper.GenerateIdolCard()
                case _:
                    start = time.perf_counter()
                    FriendsScraper.Generate(friendsList[friendsArg-1], friendsArg-1)
        case 4:
            print("Select Series to Scrape, input 0 for all series")
            paradeArg = int(input())
            match paradeArg:
                case 0:
                    start = time.perf_counter()
                    for i in enumerate(paradeList):
                        ParadeScraper.Generate(i[1], i[0])
                case _:
                    start = time.perf_counter()
                    ParadeScraper.Generate(paradeList[paradeArg-1], paradeArg-1)

        case 5:
            print("Select Series to Scrape, input 0 for all series")
            planetArg = int(input())
            match planetArg:
                case 0:
                    start = time.perf_counter()
                    for i in enumerate(planetList):
                        PlanetScraper.Generate(i[1], i[0])
                case _:
                    start = time.perf_counter()
                    PlanetScraper.Generate(planetList[planetArg-1], planetArg)

    end = time.perf_counter()
    print(f'DONE! Operation took {timer(start, end)}')

    try:
        if result:
            aikatsuQR_Warn(result)
    except:
        print("No QR mismatches!")

main() #called when program runs independently, otherwise individual scrapers are called in the app