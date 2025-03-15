import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create dndGame table
cursor.execute('''
CREATE TABLE IF NOT EXISTS dndGame (
    gameId INTEGER PRIMARY KEY AUTOINCREMENT,
    guildId TEXT NOT NULL,
    creatorId TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    level TEXT,
    duration TEXT,
    players TEXT,
    experience TEXT,
    categoryId TEXT,
    roleId TEXT
)
''')
conn.commit()
