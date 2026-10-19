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
    print("[initDB Phase 2] Generating card database...")

    dbPath = BASE_DIR / "Database" / "katsuColleDB.db"
    firstCreate = not os.path.exists(dbPath)
        
    con = sqlite3.connect(dbPath)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    if firstCreate:
        # Create lookup tables
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS series(
                    series_id INTEGER PRIMARY KEY,
                    series_name TEXT NOT NULL
                )
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS subseries(
                    subseries_id INTEGER NOT NULL,
                    series_id INTEGER NOT NULL,
                    subseries_name TEXT NOT NULL,
                    
                    PRIMARY KEY (series_id, subseries_id),
                    
                    FOREIGN KEY (series_id) 
                        REFERENCES series(series_id)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS type(
                    type_id INTEGER PRIMARY KEY,
                    type_name TEXT NOT NULL UNIQUE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS rarity(
                    rarity_id INTEGER PRIMARY KEY,
                    series_id INTEGER NOT NULL,
                    rarity_name TEXT NOT NULL,
                    rarity_code TEXT,

                    FOREIGN KEY (series_id)
                        REFERENCES series(series_id),

                    UNIQUE (series_id, rarity_code)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS category(
                    category_id INTEGER PRIMARY KEY,
                    category_name TEXT NOT NULL UNIQUE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS brand(
                    brand_id INTEGER PRIMARY KEY,
                    brand_name TEXT NOT NULL UNIQUE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS constellation(
                    constellation_id INTEGER PRIMARY KEY,
                    constellation_name TEXT NOT NULL UNIQUE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS romance(
                    romance_id INTEGER PRIMARY KEY,
                    romance_name TEXT NOT NULL UNIQUE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS promo(
                    promo_id INTEGER PRIMARY KEY,
                    promo_name TEXT NULL UNIQUE
                )
            """
        )

        # Create card table
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS card(
                    id INTEGER PRIMARY KEY,
                    series_id INTEGER NOT NULL,
                    subseries_id INTEGER NOT NULL,
                    card_id TEXT NOT NULL,
                    card_name TEXT NOT NULL,
                    rarity_id INTEGER NOT NULL,
                    brand_id INTEGER,
                    image_url TEXT NOT NULL,
                    appeal TEXT,
                    notes TEXT,
                    promo_id INTEGER,

                    FOREIGN KEY (series_id, subseries_id)
                        REFERENCES subseries(series_id, subseries_id),

                    FOREIGN KEY (rarity_id)
                        REFERENCES rarity(rarity_id),

                    FOREIGN KEY (brand_id)
                        REFERENCES brand(brand_id),

                    FOREIGN KEY (promo_id)
                        REFERENCES promo(promo_id),

                    UNIQUE (series_id, card_id)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS card_type(
                    card_id INTEGER NOT NULL,
                    type_id INTEGER NOT NULL,

                    PRIMARY KEY (card_id, type_id),

                    FOREIGN KEY (card_id) REFERENCES card(id),

                    FOREIGN KEY (type_id) REFERENCES type(type_id)    
                );
            """
        )

        # Create series specific attribute tables
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS aikatsu_details(
                    card_id INTEGER PRIMARY KEY,
                    points INTEGER,
                    qr_code TEXT,
                    bar_code TEXT,
                    lucky_star INTEGER,
                    constellation_id INTEGER,
                    romance_id INTEGER,
                    boom INTEGER,
                    fever INTEGER,
                    phone_compat INTEGER,
                    look1_compat INTEGER,
                    look2_compat INTEGER,

                    FOREIGN KEY (card_id) REFERENCES card(id)
                        ON DELETE CASCADE,

                    FOREIGN KEY (constellation_id)
                        REFERENCES constellation(constellation_id),

                    FOREIGN KEY (romance_id)
                        REFERENCES romance(romance_id)
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS stars_details(
                    card_id INTEGER PRIMARY KEY,
                    points INTEGER,
                    upgrade INTEGER,
                    plus INTEGER,
                    
                    FOREIGN KEY (card_id) REFERENCES card(id)
                        ON DELETE CASCADE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS friends_details(
                    card_id INTEGER PRIMARY KEY,
                    points INTEGER,
                    
                    FOREIGN KEY (card_id) REFERENCES card(id)
                        ON DELETE CASCADE
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS parade_details(
                    card_id INTEGER PRIMARY KEY,
                    school TEXT,
                    
                    FOREIGN KEY (card_id) REFERENCES card(id)
                        ON DELETE CASCADE
                )
            """
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS planet_details(
                    card_id INTEGER PRIMARY KEY,
                    level INTEGER,
                    back_url TEXT,

                    FOREIGN KEY (card_id) REFERENCES card(id)
                        ON DELETE CASCADE
                )
            """
        )

    con.commit()
    con.close()

    print("[initDB Phase 2] Card database tables created!")

