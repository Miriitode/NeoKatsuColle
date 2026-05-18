import time
import os
import utils.scrapers.PlanetScraper as PlanetScraper
import utils.scrapers.ParadeScraper as ParadeScraper
import utils.scrapers.FriendsScraper as FriendsScraper
import utils.scrapers.StarsScraper as StarsScraper
import utils.scrapers.AikatsuScraper as AikatsuScraper
        
def timer(start, end):
    runtime = round((end - start), 2)
    if runtime < 60:
        return f'{runtime} seconds'
    else:
        return str(round((runtime/60), 2)) + ' minutes'

def Database_Check():
    '''
    Generates Directories when no folders are present
    '''

    series = ["aikatsu", "stars", "friends", "parade", "planet"]
    subfolder = ["CardList", "ImgList"]
    databaseDir = os.path.join(os.getcwd(),"Database")

    for ser in series:
        for sub in subfolder:
            try: os.makedirs(os.path.join(databaseDir,ser,sub))
            except OSError: pass

def main():

    Database_Check()

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

main() #called when program runs independently, otherwise individual scrapers are called in the app