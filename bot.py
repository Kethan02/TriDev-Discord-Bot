import discord
import asyncio
from discord.ext import commands
# Importing text summerization library. Feel free to make any changes
# if you think there is a better library for text summarization
# check the texttest.py file to see how it works.
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# Custom modules
import db

client = commands.Bot(command_prefix = '!')

# This takes a while and should be run only once on startup
mongo_client = db.connect_to_mongo(db.user, db.pswd)

# Get the keyword list for test server (each guild will have their own list)
keywords_collection = db.get_collection(
    db.get_db(mongo_client, db.db_name),
    db.collections[0]
)
keywords_list = db.get_keywords(keywords_collection)

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
    keywords_list.append(newKeyWord)

    if newKeyWord in keywords_list:
        await ctx.send('Keyword added successfully')
    else:
        await ctx.send('Keyword not added successfully')

@client.command(name = 'myKeywords', aliases = ['myKW', 'mykw', 'mkw'])
async def about(ctx):
    for words in keywords_list:
        await ctx.send(words)

    await ctx.send('These are your keywords')

@client.event
async def on_message(message):
    if (message.author.bot):
        return
    if (message.author.id != message.author.bot):
        for key in keywords_list:
            if key in message.content:
                print('Found')
                myMessageEmbed = discord.Embed(
                title = "Message Found",
                description = message.content,
                )

                await message.channel.send(embed = myMessageEmbed)
    await client.process_commands(message)
