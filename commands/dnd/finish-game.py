import discord
from discord.ext import commands
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command(name='finish-game', description="Finish a D&D game.")
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(administrator=True)
async def finish_game(ctx, role: discord.Role):
    await ctx.defer(ephemeral=True)
    guild = ctx.guild

    try:
        category = discord.utils.get(guild.categories, name=role.name)

        if category:
            for channel in category.channels:
                await channel.delete(reason=f'Deleted by {ctx.author}')

            await category.delete(reason=f'Deleted by {ctx.author}')
        else:
            print(f'Category "{role.name}" not found.')

        # Delete the game entry from the database
        cursor.execute('DELETE FROM dndGame WHERE roleId = ? AND guildId = ?', (role.id, ctx.guild.id))
        conn.commit()

        await ctx.send('Partida cerrada correctamente, ¡Muchas gracias por jugar!')
    except Exception as e:
        print(f'Error: {e}')
        await ctx.send('Ha ocurrido un error mientras cerraba la partida')
