import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
from handlers.event_handler import setup_events

load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    level INTEGER NOT NULL,
    xp INTEGER NOT NULL
)
''')
conn.commit()

@bot.event
async def on_disconnect():
    conn.close()


async def main():
    try:
        print('✅ Connected to SQLite Database.')
        setup_events(bot)
        await bot.start(os.getenv('TOKEN'))
    except Exception as e:
        print(f'❗Error: {e}.')
    finally:
        conn.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

