# All in one script for scraping, fixing, and initializing NeoKatsuColle's Card Database
# Depends on all Aikatsu scrapers (utils/scrapers) and dbGenerator.py
# This will generate A LOT of intermediate .json files. These will be in utils/scraperData. Remove when not in use.
import os
from pathlib import Path
from scrapers.Scraper import InitDBScraper
from dbGenerator import genCardDB

BASE_DIR = Path(__file__).resolve().parents[1]

def main():
    # Phase 1: Scrape data
    InitDBScraper()

    # Phase 2: Create database tables
    genCardDB()

    # Phase 3: Import scraped data into databse (TODO)