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

bot = commands.Bot(command_prefix="!")

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# On connection to discord
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

# Errors >!< 
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# push_score("123456", "Test#1234", "00:14:03", "2020-06-25 09:49:39", "143212208761864192")
# push_score("654321", "Test#4321", "00:07:03", "2020-06-25 09:49:39", "143212208761864192")
# push_score("654321", "Test#4321", "00:13:03", "2020-06-24 09:49:39", "143212208761864192")
# push_score("134527530014212096", "Mahkookeh#6092", "00:59:33", "2020-06-24 09:49:40", "143212208761864192")
# push_score("134527530014212096", "Mahkookeh#6092", "00:08:33", "2020-06-26 09:49:40", "143212208761864192")
# exit()


bot.run(TOKEN, bot=True)