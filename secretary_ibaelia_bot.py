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
    'cogs.ibaelia'
    ]

channel_emoji_dict = {
    "1️⃣": 759117258307403826,
    "2️⃣": 759299496256602123,
    "3️⃣": 759630994205704211
}


reaction_channel_id = 759126207177687141


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