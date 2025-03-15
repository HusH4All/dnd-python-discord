import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command(name='timeout', description="Timeout a user.")
@commands.has_permissions(mute_members=True)
@commands.bot_has_permissions(mute_members=True)
async def timeout(ctx, target_user: discord.Member, duration: str, *, reason: str = "No reason provided"):
    await ctx.defer()

    if target_user.bot:
        await ctx.send("I can't timeout a bot.")
        return

    try:
        ms_duration = int(duration[:-1]) * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[duration[-1]]
    except (ValueError, KeyError):
        await ctx.send('Please provide a valid timeout duration (e.g., 30m, 1h, 1d).')
        return

    if ms_duration < 5 or ms_duration > 28 * 86400:
        await ctx.send('Timeout duration cannot be less than 5 seconds or more than 28 days.')
        return

    if target_user.top_role.position >= ctx.author.top_role.position:
        await ctx.send("You can't timeout that user because they have the same/higher role than you.")
        return

    if target_user.top_role.position >= ctx.guild.me.top_role.position:
        await ctx.send("I can't timeout that user because they have the same/higher role than me.")
        return

    try:
        await target_user.timeout_for(timedelta(seconds=ms_duration), reason=reason)
        await ctx.send(f'{target_user} was timed out for {timedelta(seconds=ms_duration)}.\nReason: {reason}.')
    except Exception as e:
        print(f'Error timing out user: {e}')
