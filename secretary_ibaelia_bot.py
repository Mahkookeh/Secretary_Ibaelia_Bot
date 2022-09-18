import os
import ast
import json
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv(encoding="utf_8")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

pic_ext = ['.jpg','.png','.jpeg']


# initial_extensions = [
#     'cogs.crossword',
#     'cogs.ibaelia',
#     'cogs.guildwars'
#     ]

CHANNEL_EMOJI_DICT = os.getenv("CHANNEL_EMOJI_DICT")
channel_emoji_dict = json.loads(CHANNEL_EMOJI_DICT)


CHANNEL_EMOJI_DICT_2021 = os.getenv("CHANNEL_EMOJI_DICT_2021")
channel_emoji_dict_2021 = json.loads(CHANNEL_EMOJI_DICT_2021)


reaction_channel_id = 759126207177687141
reaction_channel_id_2021 = 897032807497469952

reaction_channel1to5_id = 846974659332538379
reaction_channel1to5_message_id = 846975577368952832

regex_pattern_1to5 = re.compile("(<@!*&*[0-9]+>\\s*\n)?(Outplay: |Funny: ).*\nPeople In Clip: .*\nExtra Notes: ((?:.|\n)*)\n<.*>((?:.|\n)*)")


bot = commands.Bot(command_prefix="uwu!", intents=discord.Intents.all())

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != '__init__.py':
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(load_extensions())

# On connection to discord
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    activity = discord.Activity(name='your uwus!',type=2)
    await bot.change_presence(activity=activity)

# On message to discord
# @bot.event
# async def on_message(payload):

#     if (payload.channel.id == reaction_channel1to5_id):
#         print(f"{bot.user} heard your message!")
#         print(payload.content)
#         if (regex_pattern_1to5.match(payload.content)):
#             emojis_1to5 = list(channel_emoji_dict.keys())[:5]
#             for emoji in emojis_1to5:
#                 await payload.add_reaction(emoji)
#         else:
#             print("bad message")
#     await bot.process_commands(payload)


# @bot.event
# async def on_raw_reaction_add(payload):
#     user = bot.get_user(payload.user_id)

#     if payload.channel_id == reaction_channel_id:
#         emoji_str = str(payload.emoji)
#         if emoji_str in channel_emoji_dict:
#             channel = bot.get_channel(channel_emoji_dict[emoji_str])  
#             perms = channel.overwrites_for(user)   
#             perms.read_messages = True
#             await channel.set_permissions(user, overwrite=perms)
#     if payload.channel_id == reaction_channel_id_2021:
#         emoji_str = str(payload.emoji)
#         if emoji_str in channel_emoji_dict_2021:
#             channel = bot.get_channel(channel_emoji_dict_2021[emoji_str])  
#             perms = channel.overwrites_for(user)   
#             perms.read_messages = True
#             await channel.set_permissions(user, overwrite=perms)
#     elif payload.channel_id == reaction_channel1to5_id:
#         if payload.message_id == reaction_channel1to5_message_id:
#             print(payload.emoji.name)
#             if payload.emoji.name == "pepoPigeon":
#                 guild = bot.get_guild(payload.guild_id)
#                 role = discord.utils.get(guild.roles, name="Clip Connoisseur")
#                 member = guild.get_member(payload.user_id)
#                 await member.add_roles(role)
#     elif payload.channel_id in spoiler_thread_channel_ids:
#         pass



# @bot.event
# async def on_raw_reaction_remove(payload):
#     user = bot.get_user(payload.user_id)

#     print(payload.channel_id)
#     if payload.channel_id == reaction_channel_id:
#         emoji_str = str(payload.emoji)
#         if emoji_str in channel_emoji_dict:
#             channel = bot.get_channel(channel_emoji_dict[emoji_str])  
#             perms = channel.overwrites_for(user)   
#             perms.read_messages = False
#             await channel.set_permissions(user, overwrite=perms)
#     if payload.channel_id == reaction_channel_id_2021:
#         emoji_str = str(payload.emoji)
#         if emoji_str in channel_emoji_dict_2021:
#             channel = bot.get_channel(channel_emoji_dict_2021[emoji_str])  
#             perms = channel.overwrites_for(user)   
#             perms.read_messages = False
#             await channel.set_permissions(user, overwrite=perms)
#     elif payload.channel_id == reaction_channel1to5_id:
#         if payload.message_id == reaction_channel1to5_message_id:
#             print(payload.emoji.name)
#             if payload.emoji.name == "pepoPigeon":
#                 guild = bot.get_guild(payload.guild_id)
#                 role = discord.utils.get(guild.roles, name="Clip Connoisseur")
#                 member = guild.get_member(payload.user_id)
#                 await member.remove_roles(role)

# Errors >!< 
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


bot.run(TOKEN)