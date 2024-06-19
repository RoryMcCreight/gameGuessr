import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('database/games.db')
cursor = conn.cursor()

# Get a random game ID
cursor.execute('SELECT id FROM Games ORDER BY RANDOM() LIMIT 1')
game_id = cursor.fetchone()[0]

# Insert or replace the daily game
date = datetime.now().strftime('%Y-%m-%d')
cursor.execute('''
    INSERT OR REPLACE INTO DailyGames (game_id, date)
    VALUES (?, ?)
''', (game_id, date))

# Commit the changes and close the connection
conn.commit()
conn.close()
