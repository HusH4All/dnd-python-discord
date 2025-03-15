import discord
from discord.ext import commands
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import io

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

def calculate_level_xp(level):
    return 5 * (level ** 2) + 50 * level + 100

@bot.command(name='level', description="Shows your/someone's level.")
async def level(ctx, target_user: discord.Member = None):
    if ctx.guild is None:
        await ctx.send("You can only run this command inside a server.")
        return

    target_user = target_user or ctx.author
    target_user_id = target_user.id

    cursor.execute('SELECT xp, level FROM Level WHERE userId = ? AND guildId = ?', (target_user_id, ctx.guild.id))
    result = cursor.fetchone()

    if not result:
        await ctx.send(f"{target_user.mention} doesn't have any levels yet. Chat a little more and try again.")
        return

    xp, level = result

    cursor.execute('SELECT userId, level, xp FROM Level WHERE guildId = ? ORDER BY level DESC, xp DESC', (ctx.guild.id,))
    all_levels = cursor.fetchall()

    current_rank = next((index for index, lvl in enumerate(all_levels, start=1) if lvl[0] == target_user_id), None)

    # Create rank card image
    image = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((10, 10), f"Rank: {current_rank}", font=font, fill="black")
    draw.text((10, 30), f"Level: {level}", font=font, fill="black")
    draw.text((10, 50), f"XP: {xp}", font=font, fill="black")

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    file = discord.File(buffer, filename='rank.png')
    await ctx.send(file=file)

# Remember to close the connection when done
@bot.event
async def on_disconnect():
    conn.close()
