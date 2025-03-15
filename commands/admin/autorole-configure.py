import discord
from discord.ext import commands
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command(name='autorole-configure', description="Configure your auto-role for this server.")
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_roles=True)
async def autorole_configure(ctx, role: discord.Role):
    if ctx.guild is None:
        await ctx.send("You can only run this command inside a server.")
        return

    try:
        await ctx.defer()

        cursor.execute('SELECT roleId FROM AutoRole WHERE guildId = ?', (ctx.guild.id,))
        result = cursor.fetchone()

        if result:
            if result[0] == role.id:
                await ctx.send('Auto role has already been configured for that role. To disable run `/autorole-disable`.', ephemeral=True)
                return

            cursor.execute('UPDATE AutoRole SET roleId = ? WHERE guildId = ?', (role.id, ctx.guild.id))
        else:
            cursor.execute('INSERT INTO AutoRole (guildId, roleId) VALUES (?, ?)', (ctx.guild.id, role.id))

        conn.commit()
        await ctx.send("Autorole has now been configured. To disable run `/autorole-disable`.", ephemeral=True)
    except Exception as e:
        print(f'Error: {e}')

# Remember to close the connection when done
@bot.event
async def on_disconnect():
    conn.close()
