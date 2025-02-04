CREATE TABLE IF NOT EXISTS tvshows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_name TEXT NOT NULL,
    season INTEGER,
    episode TEXT,
    genre TEXT
);
