import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

pic_ext = ['.jpg','.png','.jpeg']


initial_extensions = [
    'cogs.crossword',
    'cogs.ibaelia',
    'cogs.reactionlistener'
    ]

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

@bot.event
async def on_raw_reaction_add(payload):
    reaction_channel_id = 759126207177687141
    user = bot.get_user(payload.user_id)

    if payload.channel_id != reaction_channel_id:
        return

    print(str(payload.emoji))
    if str(payload.emoji) == "1️⃣":
        channel = bot.get_channel(759117258307403826)  
        perms = channel.overwrites_for(user)   
        perms.read_messages = True
        await channel.set_permissions(user, overwrite=perms)

    elif str(payload.emoji) == "2️⃣":
        channel = bot.get_channel(759299496256602123)  
        perms = channel.overwrites_for(user)   
        perms.read_messages = True
        await channel.set_permissions(user, overwrite=perms)

@bot.event
async def on_raw_reaction_remove(payload):
    reaction_channel_id = 759126207177687141
    user = bot.get_user(payload.user_id)

    if payload.channel_id != reaction_channel_id:
        return

    print(str(payload.emoji))
    if str(payload.emoji) == "1️⃣":
        channel = bot.get_channel(759117258307403826)  
        perms = channel.overwrites_for(user)   
        perms.read_messages = True
        await channel.set_permissions(user, overwrite=perms)

    elif str(payload.emoji) == "2️⃣":
        channel = bot.get_channel(759299496256602123)  
        perms = channel.overwrites_for(user)   
        perms.read_messages = True
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