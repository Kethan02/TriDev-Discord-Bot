@ -1,5 +1,6 @@
import discord
import os
import asyncio
from discord.ext import commands
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# Importing text summerization library. Feel free to make any changes
# if you think there is a better library for text summarization
# check the texttest.py file to see how it works.

client = commands.Bot(command_prefix = '!')
@ -56,3 +57,5 @@ async def on_message(message):

                await message.channel.send(embed = myMessageEmbed)
    await client.process_commands(message)
    
client.run(os.environ['DISCORD_TOKEN'])
