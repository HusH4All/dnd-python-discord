import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create Level table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Level (
    userId TEXT NOT NULL,
    guildId TEXT NOT NULL,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0,
    PRIMARY KEY (userId, guildId)
)
''')
conn.commit()
