import discord
from discord.ext import commands
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_member_join(member):
    try:
        guild = member.guild
        if not guild:
            return

        cursor.execute('SELECT roleId FROM AutoRole WHERE guildId = ?', (guild.id,))
        result = cursor.fetchone()
        if result:
            role_id = result[0]
            role = guild.get_role(int(role_id))
            if role:
                await member.add_roles(role)
    except Exception as e:
        print(f'Error giving role automatically: {e}')

# Remember to close the connection when done
@bot.event
async def on_disconnect():
    conn.close()
