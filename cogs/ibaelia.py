import discord
from discord.utils import get
from discord.ext import commands

class IbaeliaCommands(commands.Cog):
    """Ibaelia Bot's General Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unsubscribe", help="Unsubscribe from my antics.")
    async def unsubscribe(self, ctx):
        emoji = get(ctx.message.guild.emojis, name="cry")
        embed = discord.Embed(title="You meanie! :cry:", description=f"You're stuck with me though...",color=0x14e1d4)
        irelia_buns = "ibaelia_images//sad_irelia.png"
        file = discord.File(irelia_buns, filename="image.png")
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text="uwu")
        await ctx.send(file=file, embed=embed)
    
    @commands.command(name="gotosleep", help="Go to sleep!")
    async def go_to_sleep(self, ctx):
        embed = discord.Embed(color=0x14e1d4)
        irelia_buns = "ibaelia_images//stayinguptoolatecheerleader.gif"
        file = discord.File(irelia_buns, filename="image.gif")
        embed.set_image(url="attachment://image.gif")
        embed.set_footer(text="uwu")
        await ctx.send(file=file, embed=embed)
    
    @commands.command(name="uwu")
    async def test_function(self, ctx):
        embed = discord.Embed(color=0x14e1d4)
        irelia_buns = "ibaelia_images//IreliaBuns.jpg"
        file = discord.File(irelia_buns, filename="image.png")
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text="uwu")
        await ctx.send(file=file, embed=embed)
        
def setup(bot):
    bot.add_cog(IbaeliaCommands(bot))