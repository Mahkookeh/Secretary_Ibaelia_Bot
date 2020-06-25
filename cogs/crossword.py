import discord
import cogs.helper_files.crossword_cog_helper as cch 
import cogs.helper_files.crossword_score_extraction as cse
import requests
from PIL import Image
from discord.utils import get
from io import BytesIO

from discord.ext import commands

class CrosswordCommands(commands.Cog):
    """Crossword Commands"""
    def __init__(self, bot):
        self.bot = bot

    # Command to send the link to the mini crossword
    @commands.command(name="cwlink", help="I'll send the link to the mini crossword puzzle. Good luck!")
    async def return_crossword_link(self, ctx):
        embed = discord.Embed(title="My To Dos~", color=0x14e1d4)
        embed.add_field(value="[Here's](https://www.nytimes.com/crosswords/game/mini) the link for the crossword. \nGood luck!", name='\u200b')
        embed.set_footer(text="uwu")
        await ctx.send(embed=embed)

    @commands.command(name="cwregister", help="I'll add you to the list of people to keep track of in this server.")
    async def register_for_crossword(self, ctx):
        user_id = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        guild_name = str(ctx.message.guild.name)
        user = await self.bot.fetch_user(ctx.message.author.id)
        username = str(user)
        ids = cch.add_user_to_database(user_id, username, guild_id)
        cch.add_to_server(user_id, guild_id, ids)
        await ctx.send(f"You ({username}) are registered for the crossword scoreboard in {guild_name}.")


    @commands.command(name="cwupload", help="Attach an image so I can add your time to the scoreboard!")
    async def upload_score(self, ctx):
        image_url = ctx.message.attachments[0].url
        image_request = requests.get(image_url)
        provided_image = Image.open(BytesIO(image_request.content))
        formatted_time = cse.get_time_from_image(provided_image)
        user = await self.bot.fetch_user(ctx.message.author.id)
        username = str(user)
        done, prev_score = cch.push_score(str(ctx.message.author.id), username, formatted_time, str(ctx.message.created_at), str(ctx.message.guild.id))
        if done:
            await ctx.send(f"Your time of {formatted_time} has been uploaded to today's scoreboard.")
        else:
            await ctx.send(f"Nice try, but you've already submitted a time of {prev_score} for today.")

    @commands.command(name="cwscores", help="I'll send you a list of your scores for the past week.")
    async def get_personal_scores(self, ctx):
        user_id = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        scores = cch.get_scores_by_id(user_id, guild_id, 7)
        embed = discord.Embed(title="Your Weekly Crossword Scores", color=0x14e1d4)
        for score in scores:
            embed.add_field(name=score['time'].split(" ")[0], value=score['score'], inline=False)
        embed.set_footer(text="uwu")
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="cwscoreboard", help="I'll show you everyone's scores for today.")
    async def get_scoreboard(self, ctx):
        message_time = str(ctx.message.created_at).split(" ")[0]
        guild_id = str(ctx.message.guild.id)
        scores = cch.get_scores_by_time(message_time, guild_id)
        embed = discord.Embed(title="Daily Crossword Scoreboard", color=0x14e1d4)
        for idx in range(len(scores)):
            embed.add_field(name=f"{idx + 1}. {scores[idx]['name']}", value=scores[idx]['score'], inline=False)
        embed.set_footer(text="uwu")
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="cwuploadother", help="Upload someone else's score.", hidden=True, pass_context=True)
    async def upload_other_user_score(self, ctx, *, message_args):
        author_id = ctx.message.author.id
        author = str(author_id)
        owner = str(134527530014212096)
        owner_name = str(await self.bot.fetch_user(owner))
        if author != owner:
            await ctx.send(f"Only {owner_name} has permissions to use this command.")
            return
        other_user_id = message_args
        image_url = ctx.message.attachments[0].url
        image_request = requests.get(image_url)
        provided_image = Image.open(BytesIO(image_request.content))
        formatted_time = cse.get_time_from_image(provided_image)
        other_user = await self.bot.fetch_user(other_user_id)
        other_username = str(other_user)
        done, prev_score = cch.push_score(str(other_user_id), other_username, formatted_time, str(ctx.message.created_at), str(ctx.message.guild.id))
        if done:
            await ctx.send(f"{other_username}'s time of {formatted_time} has been uploaded to today's scoreboard.")
        else:
            await ctx.send(f"Nice try, but {other_username} already has a submitted time of {prev_score} for today.")

def setup(bot):
    bot.add_cog(CrosswordCommands(bot))