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
all_messages_collection = db.get_collection(
    db.get_db(mongo_client, db.db_name),
    db.collections[3]
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

    Embed = discord.Embed(
    title = "Kethan Bethamcharla", description = "I am 17 years old"
    )

    await ctx.message.channel.send(embed = Embed)
# use embed to send the newsletter (this is a good idea)

@client.command(name = 'quit')
@commands.has_permissions(administrator=True)
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

@client.command(name = 'addKeyword', aliases = ['addKW', 'aKW', 'addkeyword', 'akw'])
async def about(ctx, existingCategory, *, newKeyword):
    db.add_keyword(keywords_collection, users_collection, str(ctx.author), existingCategory, newKeyword)

    keywords_list = db.get_keywords(keywords_collection)

    if newKeyword in keywords_list:
        await ctx.send('Keyword added successfully')
    else:
        await ctx.send('Keyword not added successfully')

@client.command(name = 'addKeywordFromCategory', aliases = ['addKWFC', 'aKWFC', 'akwfc'])
async def about(ctx, *, category):
    db.add_all_keywords_from_category_to_user_keywords_list(keywords_collection, users_collection, str(ctx.author), category)

    await ctx.send('Keywords added successfully')

@client.command(name = 'getCategory', aliases = ['getC', 'gC', 'gc'])
async def about(ctx):
    categories_list = db.get_existing_keyword_categories(keywords_collection)

    await ctx.send(categories_list)
    await ctx.send('These are the keyword categories')

@client.command(name = 'getKeywordsCategory', aliases = ['getKC', 'gKC', 'gkc'])
async def about(ctx, *, category):
    keywords_in_category = db.get_existing_keywords_in_specific_category(keywords_collection, category)

    await ctx.send(keywords_in_category)
    await ctx.send('These are the keywords in the ' + category + ' category')



@client.command(name = 'myKeywords', aliases = ['myKW', 'mykw', 'mkw'])
async def about(ctx):
    # Updates keyword list
    keywords_list = db.get_keywords_of_user(users_collection, str(ctx.author))

    await ctx.send(keywords_list)
    await ctx.send('These are your keywords')

@client.command(name = 'newsletter', aliases = ['summary', 'nl', 's'])
async def about(ctx):
    messages = db.get_all_messages(all_messages_collection, ctx.guild.id, str(ctx.channel.name))

    Embed = discord.Embed(
        title = ("Newsletter from the " + channel + " channel in the " + ctx.guild.name + " server"),
        description = messages
    )

    await ctx.author.send(embed = Embed)

@client.command(name = 'sdc')
async def about(ctx, *, channel):
    guild_id = ctx.guild.id
    messages = db.get_all_messages(all_messages_collection, guild_id, channel)

    Embed = discord.Embed(
        title = ("Newsletter from the " + channel + " channel in the " + ctx.guild.name + " server"),
        description = messages
    )

    await ctx.author.send(embed = Embed)

@client.event
async def on_message(message):
    # Updates keyword list
    keywords_list = db.get_keywords(keywords_collection)

    if (message.author.bot):
        return
    if (message.author.id != message.author.bot):
        if(message.content.startswith("!") == False):
            db.add_all_messages(all_messages_collection, str(message.author),
                                message.created_at, message.content,
                                message.guild.id, str(message.channel.name))


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
                                   message.guild.id,
                                   str(message.channel.name),
                                   message.created_at)
    await client.process_commands(message)

# client.run(os.environ['DISCORD_TOKEN'])
client.run('NzY2NTE5NzU0MTc2MzMxODE2.X4kjJg.2bAKHIoIma1bg4rGq5YspMUaH9k')
