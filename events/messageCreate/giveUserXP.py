import discord
from discord.ext import commands
import sqlite3
import random
import time

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
cooldowns = set()

def calculate_level_xp(level):
    return 5 * (level ** 2) + 50 * level + 100

def get_random_xp(min_xp, max_xp):
    return random.randint(min_xp, max_xp)

@bot.event
async def on_message(message):
    if not message.guild or message.author.bot or message.author.id in cooldowns:
        return

    xp_to_give = get_random_xp(5, 15)

    cursor.execute('SELECT xp, level FROM Level WHERE userId = ? AND guildId = ?', (message.author.id, message.guild.id))
    result = cursor.fetchone()

    if result:
        xp, level = result
        xp += xp_to_give

        if xp >= calculate_level_xp(level):
            xp = 0
            level += 1
            await message.channel.send(f'{message.author.mention} you have leveled up to **level {level}**.')

        cursor.execute('UPDATE Level SET xp = ?, level = ? WHERE userId = ? AND guildId = ?', (xp, level, message.author.id, message.guild.id))
    else:
        cursor.execute('INSERT INTO Level (userId, guildId, xp, level) VALUES (?, ?, ?, ?)', (message.author.id, message.guild.id, xp_to_give, 1))

    conn.commit()
    cooldowns.add(message.author.id)
    time.sleep(60)
    cooldowns.remove(message.author.id)

# Remember to close the connection when done
@bot.event
async def on_disconnect():
    conn.close()
