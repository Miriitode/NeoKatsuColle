# All in one script for scraping, fixing, and initializing NeoKatsuColle's Card Database
# Depends on all Aikatsu scrapers (utils/scrapers) and dbGenerator.py
# This will generate A LOT of intermediate .json files. These will be in utils/scraperData. Remove when not in use.

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def main():
    ...