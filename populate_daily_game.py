import sqlite3
from datetime import date

DATABASE = 'guessr.db'

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Create Games table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            release_year INTEGER NOT NULL,
            genre TEXT NOT NULL,
            game_length INTEGER NOT NULL,
            publisher TEXT NOT NULL,
            platform TEXT NOT NULL,
            developer TEXT NOT NULL,
            country TEXT NOT NULL,
            rating REAL NOT NULL
        )
    ''')

    # Create DailyGames table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DailyGames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES Games (id)
        )
    ''')

    conn.commit()
    conn.close()

def populate_games():
    games = [
        ("The Legend of Zelda", 1986, "Action-adventure", 15, "Nintendo", "NES", "Nintendo", "Japan", 9.5),
        ("Super Mario Bros.", 1985, "Platformer", 7, "Nintendo", "NES", "Nintendo", "Japan", 9.0),
        ("Minecraft", 2011, "Sandbox", 30, "Mojang", "PC", "Mojang", "Sweden", 8.7),
        # Add more games as needed
    ]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Insert games if they don't already exist
    cur.executemany('''
        INSERT OR IGNORE INTO Games (title, release_year, genre, game_length, publisher, platform, developer, country, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', games)

    conn.commit()
    conn.close()

def set_daily_game():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Get a random game ID
    cur.execute('SELECT id FROM Games ORDER BY RANDOM() LIMIT 1')
    game_id = cur.fetchone()[0]

    # Insert the daily game for today
    cur.execute('''
        INSERT OR REPLACE INTO DailyGames (game_id, date)
        VALUES (?, ?)
    ''', (game_id, date.today().isoformat()))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    populate_games()
    set_daily_game()
