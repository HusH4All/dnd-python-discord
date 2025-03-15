import discord
from discord.ext import commands
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command(name='autorole-disable', description="Disable auto-role in this server.")
@commands.has_permissions(administrator=True)
async def autorole_disable(ctx):
    try:
        await ctx.defer()

        cursor.execute('SELECT roleId FROM AutoRole WHERE guildId = ?', (ctx.guild.id,))
        result = cursor.fetchone()

        if not result:
            await ctx.send('Auto role not been configured in this server. Use `/autorole-configure` to set it up.', ephemeral=True)
            return

        cursor.execute('DELETE FROM AutoRole WHERE guildId = ?', (ctx.guild.id,))
        conn.commit()
        await ctx.send("Autorole has been disabled for this server. Use `/autorole-configure` to set it up again.", ephemeral=True)
    except Exception as e:
        print(f'Error: {e}')
