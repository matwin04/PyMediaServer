CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_name TEXT NOT NULL,
    season INTEGER,
    episode INTEGER,
    episodeName TEXT,
    sourceFormat TEXT,
    genre TEXT
);
