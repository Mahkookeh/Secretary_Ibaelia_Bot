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

# Errors >!< 
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN, bot=True)