@ -1,5 +1,6 @@
import discord
import os
import asyncio
import os
from discord.ext import commands
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# Importing text summerization library. Feel free to make any changes
# if you think there is a better library for text summarization
# check the texttest.py file to see how it works.

client = commands.Bot(command_prefix = '!')
@ -56,3 +57,5 @@ async def on_message(message):

<<<<<<< HEAD
keyWords_List = ['Homework', 'homework', 'hw', 'HW']

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

@client.command(name = 'quit')
async def close(ctx):
    await client.close()
    print('Bot Closed')

@client.command(name = 'addKeyword', aliases = ['addKW', 'aKW', 'addkeyword'])
async def about(ctx, *, newKeyWord):
    keyWords_List.append(newKeyWord)

    if newKeyWord in keyWords_List:
        await ctx.send('Keyword added successfully')
    else:
        await ctx.send('Keyword not added successfully')

@client.command(name = 'myKeywords', aliases = ['myKW', 'mykw', 'mkw'])
async def about(ctx):
    for words in keyWords_List:
        await ctx.send(words)

    await ctx.send('These are your keywords')

@client.event
async def on_message(message):
    if (message.author.bot):
        return
    if (message.author.id != message.author.bot):
        for key in keyWords_List:
            if key in message.content:
                print('Found')
                myMessageEmbed = discord.Embed(
                title = "Message Found",
                description = message.content,
                )

                await message.channel.send(embed = myMessageEmbed)
    await client.process_commands(message)
    
client.run(os.environ['DISCORD_TOKEN'])
=======
                await message.channel.send(embed = myMessageEmbed)
    await client.process_commands(message)
    
client.run(os.environ['DISCORD_TOKEN'])
>>>>>>> database
