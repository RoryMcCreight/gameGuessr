-- Create the Games table
CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    game_length INTEGER,  -- Allow NULL values
    publisher TEXT NOT NULL,
    platform TEXT NOT NULL,
    developer TEXT NOT NULL,
    country TEXT NOT NULL,
    rating REAL  -- Allow NULL values
);

-- Create the DailyGames table with a unique constraint on the date column
CREATE TABLE IF NOT EXISTS DailyGames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    date TEXT NOT NULL UNIQUE,
    FOREIGN KEY (game_id) REFERENCES Games(id)
);

-- Set a game for today in the DailyGames table
INSERT OR REPLACE INTO DailyGames (game_id, date) VALUES (1, DATE('now'));
