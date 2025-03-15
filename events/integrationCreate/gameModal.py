import discord
from discord.ext import commands
import sqlite3
import random

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

def get_random_color():
    return random.randint(0, 16777215)

@bot.event
async def on_interaction(interaction):
    if not interaction.is_modal_submit():
        return

    try:
        custom_id = interaction.custom_id
        _, players, experience = custom_id.split('_')
        creator = interaction.user

        title = interaction.text_values['titleInput']
        description = interaction.text_values['descriptionInput']
        level = interaction.text_values['levelInput']
        duration = interaction.text_values['durationInput']
        notes = interaction.text_values.get('notesInput', 'Ninguna')

        role = interaction.guild.get_role(int(experience))
        notifications_role = discord.utils.get(interaction.guild.roles, name='NotificacionesPartidas')
        notifications_role_mention = notifications_role.id if notifications_role else ''
        role_mention = f'<@&{role.id}>' if role else 'Unknown Role'

        embed = discord.Embed(
            title=title,
            description=description,
            color=get_random_color()
        )
        embed.add_field(name='Nivel de los personajes', value=level, inline=True)
        embed.add_field(name='Duración', value=duration, inline=True)
        embed.add_field(name='Número de jugadores', value=players, inline=True)
        embed.add_field(name='Experiencia requerida', value=role_mention, inline=True)
        embed.add_field(name='Notas adicionales', value=notes, inline=False)

        guild = interaction.guild
        new_role = await guild.create_role(name=title, reason=f'Created via modal by {interaction.user.name}')
        new_category = await guild.create_category(name=title, reason=f'Created via modal by {interaction.user.name}')

        await guild.create_text_channel(name=title, category=new_category, reason=f'Created via modal by {interaction.user.name}')
        await guild.create_text_channel(name="bot", category=new_category, reason=f'Created via modal by {interaction.user.name}')
        await guild.create_voice_channel(name="Taberna", category=new_category, reason=f'Created via modal by {interaction.user.name}')

        row = discord.ui.ActionRow()
        row.add_button(label="Entrar a la Partida", style=discord.ButtonStyle.primary, custom_id="joinGame")

        await interaction.response.send_message(embed=embed, components=[row])
        await interaction.channel.send(f'¡Tenemos nueva partida! <@&{notifications_role_mention}>')

        # Further interaction handling would be added here
    except Exception as e:
        print(f'Error processing the embed: {e}')

# Remember to close the connection when done
@bot.event
async def on_disconnect():
    conn.close()
