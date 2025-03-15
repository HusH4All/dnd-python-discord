import discord
from discord.ext import commands
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command(name='create-game', description="Create a new D&D game.")
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(administrator=True)
async def create_game(ctx, role: discord.Role, players: str):
    modal = discord.ui.Modal(title="Creador de Partidas")

    title_input = discord.ui.TextInput(label="Titulo", style=discord.TextStyle.short, required=True)
    description_input = discord.ui.TextInput(label="Descripción", style=discord.TextStyle.paragraph, required=True)
    level_input = discord.ui.TextInput(label="Nivel de los personajes", style=discord.TextStyle.short, required=True)
    duration_input = discord.ui.TextInput(label="Duración", style=discord.TextStyle.short, required=True)
    notes_input = discord.ui.TextInput(label="Notas adicionales", style=discord.TextStyle.paragraph, required=False)

    modal.add_item(title_input)
    modal.add_item(description_input)
    modal.add_item(level_input)
    modal.add_item(duration_input)
    modal.add_item(notes_input)

    async def on_submit(interaction):
        # Insert game data into the database
        cursor.execute('''
        INSERT INTO dndGame (guildId, creatorId, title, description, level, duration, players, experience, categoryId, roleId)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ctx.guild.id, ctx.author.id, title_input.value, description_input.value, level_input.value, duration_input.value, players, role.id, None, role.id))
        conn.commit()

        await interaction.response.send_message(f"Game created with title: {title_input.value}", ephemeral=True)

    modal.on_submit = on_submit
    await ctx.send_modal(modal)
