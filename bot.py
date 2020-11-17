import discord
import os
import asyncio
from discord.ext import commands

# Custom modules
import db

client = commands.Bot(command_prefix = '!')

# This takes a while and should be run only once on startup
mongo_client = db.connect_to_mongo(db.user, db.pswd)

# Get the keyword list for test server (each guild will have their own list)
# NOTE: This code must be updated to use with different guilds
users_collection = db.get_collection(
    db.get_db(mongo_client, db.db_name),
    db.collections[1]
)
message_collection = db.get_collection(
    db.get_db(mongo_client, db.db_name),
    db.collections[2]
)
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
    mongo_client.close()
    print('Mongo connection closed')

@client.command(name = 'createKeywordCategory', aliases = ['ckc', 'createKeyCat'])
async def about(ctx, newCategory, *, newKeyword):
    # Not sure why we need the timestamp. Younghoon said it was imortant
    db.create_keyword_category(
        keywords_collection,
        users_collection,
        str(ctx.author),
        newCategory,
        newKeyword
    )

    keywords_list = db.get_keywords(keywords_collection)

    if newKeyword in keywords_list:
        await ctx.send('New Keyword Category created successfully')
    else:
        await ctx.send('New Keyword Catgeory not created successfully')

@client.command(name = 'addKeyword', aliases = ['addKW', 'aKW', 'addkeyword'])
async def about(ctx, existingCategory, *, newKeyword):
    db.add_keyword(keywords_collection, users_collection, str(ctx.author), existingCategory, newKeyword)

    keywords_list = db.get_keywords(keywords_collection)

    if newKeyword in keywords_list:
        await ctx.send('Keyword added successfully')
    else:
        await ctx.send('Keyword not added successfully')

@client.command(name = 'myKeywords', aliases = ['myKW', 'mykw', 'mkw'])
async def about(ctx):
    # Updates keyword list
    keywords_list = db.get_keywords_of_user(users_collection, str(ctx.author))

    await ctx.send(keywords_list)
    await ctx.send('These are your keywords')

@client.event
async def on_message(message):
    # Updates keyword list
    keywords_list = db.get_keywords(keywords_collection)

    if (message.author.bot):
        return
    if (message.author.id != message.author.bot & message.content.startswith("!") == False):
        for key in keywords_list:
            if key in message.content:
                keyword_found = key
                print('Found')
                myMessageEmbed = discord.Embed(
                title = "Message Found",
                description = message.content,
                )

                await message.channel.send(embed = myMessageEmbed)

                # Adds message to the database
                db.add_message(message_collection,
                               users_collection,
                               str(message.author),
                               keyword_found,
                               message.content,
                               message.created_at)
    await client.process_commands(message)

# client.run(os.environ['DISCORD_TOKEN'])
client.run('NzY2NTE5NzU0MTc2MzMxODE2.X4kjJg.2bAKHIoIma1bg4rGq5YspMUaH9k')
