import os
import ast
import json
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(encoding="utf_8")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

pic_ext = ['.jpg','.png','.jpeg']


initial_extensions = [
    'cogs.crossword',
    'cogs.ibaelia'
    ]

CHANNEL_EMOJI_DICT = os.getenv("CHANNEL_EMOJI_DICT")
channel_emoji_dict = json.loads(CHANNEL_EMOJI_DICT)



reaction_channel_id = 759126207177687141
reaction_channel1to5_id = 846974659332538379

regex_pattern_1to5 = re.compile("(Outplay: |Funny: ).*\nPeople In Clip: .*\nExtra Notes: ((?:.|\n)*)\n<.*>((?:.|\n)*)")


bot = commands.Bot(command_prefix="uwu!")

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# On connection to discord
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    activity = discord.Activity(name='your uwus!',type=2)
    await bot.change_presence(activity=activity)

# On message to discord
@bot.event
async def on_message(payload):

    if (payload.channel.id == reaction_channel1to5_id):
        print(f"{bot.user} heard your message!")
        print(payload.content)
        if (regex_pattern_1to5.match(payload.content)):
            emojis_1to5 = list(channel_emoji_dict.keys())[:5]
            for emoji in emojis_1to5:
                await payload.add_reaction(emoji)
        else:
            print("bad message")


@bot.event
async def on_raw_reaction_add(payload):
    user = bot.get_user(payload.user_id)

    if payload.channel_id != reaction_channel_id:
        return

    emoji_str = str(payload.emoji)
    if emoji_str in channel_emoji_dict:
        channel = bot.get_channel(channel_emoji_dict[emoji_str])  
        perms = channel.overwrites_for(user)   
        perms.read_messages = True
        await channel.set_permissions(user, overwrite=perms)

@bot.event
async def on_raw_reaction_remove(payload):
    user = bot.get_user(payload.user_id)

    if payload.channel_id != reaction_channel_id:
        return

    emoji_str = str(payload.emoji)
    if emoji_str in channel_emoji_dict:
        channel = bot.get_channel(channel_emoji_dict[emoji_str])  
        perms = channel.overwrites_for(user)   
        perms.read_messages = False
        await channel.set_permissions(user, overwrite=perms)

# Errors >!< 
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN, bot=True)