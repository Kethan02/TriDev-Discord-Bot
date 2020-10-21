import discord
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command(name = 'about')
async def about(ctx):

    myEmbed = discord.Embed(
    title = "Kethan Bethamcharla", description = "I am 17 years old"
    )

    await ctx.message.channel.send(embed = myEmbed)
# use embed to send the newsletter (this is a good idea)

client.run('NzY2NTE5NzU0MTc2MzMxODE2.X4kjJg.tfogUj4ihVX296Gfcjc2hQziCkk')
