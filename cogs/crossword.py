import discord
import cogs.helper_files.crossword_cog_helper as cch 
import cogs.helper_files.crossword_score_extraction as cse
import requests
from PIL import Image
from discord.utils import get
from io import BytesIO

from discord.ext import commands

class CrosswordCog(commands.Cog):
    """Crossword Commands"""
    def __init__(self, bot):
        self.bot = bot

    # Command to send the link to the mini crossword
    @commands.command(name="cwlink", help="I'll send the link to the mini crossword puzzle. Good luck!")
    async def return_crossword_link(self, ctx):
        link = f"<https://www.nytimes.com/crosswords/game/mini>"
        message = f"Here's the link for the crossword:\n{link}\nGood luck!"
        await ctx.send(message)

    @commands.command(name="cwupload", help="Attach an image so I can add your time to the scoreboard!")
    async def upload_score(self, ctx):
        image_url = ctx.message.attachments[0].url
        image_request = requests.get(image_url)
        provided_image = Image.open(BytesIO(image_request.content))
        formatted_time = cse.get_time_from_image(provided_image)
        user_id = await self.bot.fetch_user(ctx.message.author.id)
        username = str(user_id)
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
        for score in scores:
            embed.add_field(name=score['name'], value=score['score'], inline=False)
        embed.set_footer(text="uwu")
        await ctx.message.channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(CrosswordCog(bot))