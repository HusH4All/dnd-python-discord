import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command(name='kick', description="Kicks a member from the server")
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, target_user: discord.Member, *, reason: str = "No reason provided"):
    await ctx.defer()

    if target_user.id == ctx.guild.owner_id:
        await ctx.send("You can't kick the server owner.")
        return

    if target_user.top_role.position >= ctx.author.top_role.position:
        await ctx.send("You can't kick that user because they have the same/higher role than you.")
        return

    if target_user.top_role.position >= ctx.guild.me.top_role.position:
        await ctx.send("I can't kick that user because they have the same/higher role than me.")
        return

    try:
        await target_user.kick(reason=reason)
        await ctx.send(f'User {target_user} was kicked\nReason: {reason}.')
    except Exception as e:
        print(f'Error kicking user: {e}')
