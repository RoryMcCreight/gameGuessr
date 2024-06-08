-- Create the Games table
CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    length INTEGER NOT NULL,
    publisher TEXT NOT NULL,
    platform TEXT NOT NULL,
    developer TEXT NOT NULL,
    country TEXT NOT NULL,
    rating REAL NOT NULL
);

-- Insert sample data into the Games table
INSERT INTO Games (title, year, genre, length, publisher, platform, developer, country, rating)
VALUES 
('The Legend of Zelda: Breath of the Wild', 2017, 'Action-adventure', 50, 'Nintendo', 'Switch', 'Nintendo', 'Japan', 4.8),
('The Witcher 3: Wild Hunt', 2015, 'Role-playing', 70, 'CD Projekt', 'PC', 'CD Projekt', 'Poland', 4.9),
('Red Dead Redemption 2', 2018, 'Action-adventure', 60, 'Rockstar Games', 'PlayStation 4', 'Rockstar Games', 'USA', 4.8),
('Super Mario Odyssey', 2017, 'Platform', 12, 'Nintendo', 'Switch', 'Nintendo', 'Japan', 4.7),
('God of War', 2018, 'Action-adventure', 20, 'Sony Interactive Entertainment', 'PlayStation 4', 'Santa Monica Studio', 'USA', 4.9);

-- Create the DailyGames table with a unique constraint on the date column
CREATE TABLE IF NOT EXISTS DailyGames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    date TEXT NOT NULL UNIQUE,
    FOREIGN KEY (game_id) REFERENCES Games(id)
);

-- Set a game for today in the DailyGames table
INSERT OR REPLACE INTO DailyGames (game_id, date) VALUES (1, DATE('now'));
