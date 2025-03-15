import discord
from discord.ext import commands
import json

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

devs = config['devs']
test_server = config['testServer']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

def get_local_commands():
    # Implement this function to return a list of command objects
    pass

@bot.event
async def on_interaction(interaction):
    if not interaction.is_command():
        return

    local_commands = get_local_commands()
    try:
        command_object = next((cmd for cmd in local_commands if cmd['name'] == interaction.command.name), None)

        if not command_object:
            return

        if command_object.get('devOnly'):
            if interaction.user.id not in devs:
                await interaction.response.send_message('Only developers are allowed to run this command.', ephemeral=True)
                return

        if command_object.get('testOnly'):
            if interaction.guild.id != test_server:
                await interaction.response.send_message('This command cannot be run here.', ephemeral=True)
                return

        if 'permissionsRequired' in command_object:
            for permission in command_object['permissionsRequired']:
                if not interaction.permissions.has(getattr(discord.Permissions, permission)):
                    await interaction.response.send_message('Not enough permissions.', ephemeral=True)
                    return

        if 'botPermissions' in command_object:
            bot_member = interaction.guild.me
            for permission in command_object['botPermissions']:
                if not bot_member.guild_permissions.has(getattr(discord.Permissions, permission)):
                    await interaction.response.send_message("I don't have enough permissions.", ephemeral=True)
                    return

        await command_object['callback'](bot, interaction)
    except Exception as e:
        print(f'There was an error running this command: {e}')
