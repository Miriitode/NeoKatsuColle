import requests
import json
import time
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[3]
DATABASE_DIR = BASE_DIR / "Database"
ASSETS_DIR = BASE_DIR / "Assets"


def timer(start, end):
    runtime = round((end - start), 2)

    if runtime < 60:
        return f'{runtime} seconds'
    else:
        return str(round((runtime / 60), 2)) + ' minutes'


def get_img(series, refnum):

    json_path = DATABASE_DIR / series / f'{series}_Data-{refnum}.json'

    with open(json_path, encoding='utf-8') as data:
        imgdata = json.load(data)

    output_dir = ASSETS_DIR / "Cards" / series / f'cardimg-{refnum}'
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in imgdata:

        if series != "Planet":

            data = requests.get(i["imgLink"]).content

            print(f'Saving: {i["ID"]}.png')

            with open(output_dir / f'{i["ID"]}.png', 'wb') as file:
                file.write(data)

        else:

            data_front = requests.get(i["frontLink"]).content
            data_back = requests.get(i["backLink"]).content

            print(f'Saving: {i["ID"]} Front.png | {i["ID"]} Back.png')

            with open(output_dir / f'{i["ID"]} Front.png', 'wb') as file:
                file.write(data_front)

            with open(output_dir / f'{i["ID"]} Back.png', 'wb') as file:
                file.write(data_back)


def Imgbase_Check():

    series = ["OGKatsu", "Stars", "Friends", "Parade", "Planet"]
    databaseDir = ASSETS_DIR / "Cards"

    for ser in series:
        (databaseDir / ser).mkdir(parents=True, exist_ok=True)


def main():

    Imgbase_Check()

    series = ['OGKatsu', 'Stars', 'Friends', 'Parade', 'Planet']

    print(
        "input Number to generate card images: "
        "\n 1 - Data Carddass Aikatsu!"
        "\n 2 - Data Carddass Aikatsu Stars!"
        "\n 3 - Data Carddass Aikatsu Friends"
        "\n 4 - Data Carddass Aikatsu on Parade!"
        "\n 5 - Data Carddass Aikatsu Planet!"
    )

    opt = int(input())

    start = time.perf_counter()

    match opt:

        case 0:

            print(
                "WARNING!!! This will download every card image from EVERY GAME SERIES!"
                "\nThis operation will take AT LEAST AN HOUR."
                "\nType 'YES' to confirm the operation:"
            )

            confirm = input()

            if confirm == "YES":

                for i in series:

                    dir_path = DATABASE_DIR / i / "ImgList"

                    for j in range(len(list(dir_path.iterdir()))):

                        if (i == 'Friends') and (j == 11):
                            continue

                        get_img(i, j)

            else:
                print("Operation cancelled.")
                main()

        case _:

            print("Select Card Set Series to Download, input -1 to Download everything")

            opt2 = int(input())

            if opt2 == -1:

                dir_path = DATABASE_DIR / series[opt - 1] / "ImgList"

                for k in range(len(list(dir_path.iterdir()))):

                    if (series[opt - 1] == 'Friends') and (k == 11):
                        continue

                    get_img(series[opt - 1], k)

            else:
                get_img(series[opt - 1], opt2)

    end = time.perf_counter()

    print(f'DONE! Operation took {timer(start, end)}')


main()