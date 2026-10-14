import sqlite3
import os
from pathlib import Path

# Card Table
# - ID (internal) PK INT ()
# - CardID (ID on card) STR
# - CardSeries INT FK Series
# - Rarity

BASE_DIR = Path(__file__).resolve().parents[1]
firstCreate = False

def genCardDB():
    if os.path.exists(BASE_DIR / "Database" / "katsuColleDB.db"):
        firstCreate = False
    else:
        firstCreate = True
        
    con = sqlite3.connect(BASE_DIR / "Database" / "katsuColleDB.db")

    cur = con.cursor()

    if firstCreate:
        # Create Card Table
        cur.execute(
            ""
        )

