import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('guessr.db')
cursor = conn.cursor()

# Create a temporary table with unique entries
cursor.execute('''
    CREATE TABLE Games_temp AS
    SELECT *
    FROM Games
    WHERE rowid IN (
        SELECT MIN(rowid)
        FROM Games
        GROUP BY title, release_year
    )
''')

# Drop the original table
cursor.execute('DROP TABLE Games')

# Rename the temporary table to the original table name
cursor.execute('ALTER TABLE Games_temp RENAME TO Games')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Duplicates removed successfully.")
