import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create AutoRole table
cursor.execute('''
CREATE TABLE IF NOT EXISTS AutoRole (
    guildId TEXT PRIMARY KEY,
    roleId TEXT NOT NULL
)
''')
conn.commit()
