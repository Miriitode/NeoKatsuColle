# NeoKatsuColle

A (new) card collection tracker and card database for the Data Carddass Aikatsu series.

---

NeoKatsuColle is a rework of the original KatsuColle, a card collection tracker and card database for the Data Carddass Aikatsu series. Originally made with the Flet framework (and with very limited experience), it was since then migrated to the NiceGUI framework. This allows for NeoKatsuColle to be both a web application and a local, standalone application for personal use.

## Features

- View list of cards and detailed card information from every Aikatsu Series (up to Aikatsu Planet!)
- Card collection tracking with statistics
- QR and Barcode scanning of cards for easy card identification and registering to the tracker (Only works for the original Aikatsu series for the time being)
- Mark favorite cards, and create personalized lists of cards
- Importing and exporting card tracker data
- Mass card tracking mode for quick and easy card tracking (useful when you already have an existing collection of cards and want to add them in bulk to the tracker)

## Running NeoKatsuColle

NeoKatsuColle can be run as a web app and a local instance. To run it locally:

1. Make sure you have python 3.13+ installed

2. Go into the main directory of the project with the command prompt, and run the following command (optionally, for advanced users: create a virtual environment and run the command):

```
pip install requirements.txt
```

3. In the same command prompt and location, run the following command (if a venv was made, activate that first):

```
python main.py
```

This should open up your web browser, and the app should run right away!

## NeoKatsuColle Utilities

This section is for advanced users and for documentation of the various utilities available and used for the development of this project.

### Scrapers (`utils/scrapers`)

- These are exclusive Python scripts that were used to scrape all the card information from the official card list websites. The scrapers export (almost) all available data present in the database into a `.json` file.
> [!WARNING]
> There are some promotional cards that are not in the website for some reason, as evident by the QR Data scraper. Using the scraper will have certain cards missing compared to the data in the database.

- To use the scraper, run `Scraper.py`. You can scrape card data for a specific main series and subseries. Additionally, you can scrape everything in one go. The scraped data is saved in the `Database` folder.
> [!NOTE]
> Running the scraper for every series will take a few minutes. Additionally, the scraper for Aikatsu Stars generally takes longer compared to other scrapers due to the nature of the website.

### QR Data Scraper for Aikatsu! (`utils/scrapers/qrScraper.py`)

- The official website does not have QR and Barcode information for each card (and for good reasons). This Python script scrapes the QR and Barcode data compiled [from this website.](https://pokehunngry.com). If the scraped card data already exists, the Python script automatically appends this data into the `.json` files.
> [!NOTE]
> The website covers most of the cards for Data Carddass Aikatsu. It also has promotional card QR codes for Data Carddass Aikatsu Stars, but is not included in the scraper. Additionally, some of the QR and Barcode data for some promotional cards for Data Carddass Aikatsu is missing.

### Promotional Card Comparison Script (`utils/Aikat_Promo_Compare.py`)
- Due to inconsistencies with the official website list for promotional cards and the QR code list website, this script identifies any missing cards for both sources.

### Promotional Card Category Separator Script (`utils/PromoSeparate.py`)
- This script allows for promotional cards in Data Carddass Aikatsu to be separated into categories (as indicated by their promotional ID code). This script was left unused as the entire database was migrated for a cleaner codebase.

## TODO
- Rework Database
- UI rework
- Add settings
- Add user statistics page
- Personalized lists and favorite cards
- Tracker import / export
- Mass Card Tracking Mode
