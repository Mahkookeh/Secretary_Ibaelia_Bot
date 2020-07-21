import discord
from discord.utils import get
from discord.ext import commands

class IbaeliaCommands(commands.Cog):
    """Ibaelia Bot's General Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="todo", help="My To Dos~")
    async def todo(self, ctx):
        embed = discord.Embed(title="My To Dos~", color=0x14e1d4)
        embed.add_field(value="[Here's](https://github.com/Mahkookeh/Secretary_Ibaelia_Bot/projects/1) the current To Do list for Secretary Ibaelia.", name='\u200b')
        embed.set_footer(text="uwu")
        await ctx.send(embed=embed)

    @commands.command(name="sourcecode", help="Don't stare too long!")
    async def sourcecode(self, ctx):
        embed = discord.Embed(title="You want to look at my *what*?! :flushed:", color=0x14e1d4)
        embed.add_field(value="Oh gosh, don't stare too long!\n[(⁄⁄•⁄ω⁄•⁄⁄)](https://github.com/Mahkookeh/Secretary_Ibaelia_Bot)\nHow embarrassing...", name='\u200b')
        embed.set_footer(text="uwu")
        await ctx.send(embed=embed)

    @commands.command(name="unsubscribe", help="Unsubscribe from my antics.")
    async def unsubscribe(self, ctx):
        embed = discord.Embed(title="You meanie! :cry:", description=f"You're stuck with me though...", color=0x14e1d4)
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
    
    @commands.command(name="furry", help="thicc")
    async def furry_clip(self, ctx):
        await ctx.send("Enjoy!\nhttps://streamable.com/qs39z6")
    
    @commands.command(name="uwu")
    async def test_function(self, ctx):
        embed = discord.Embed(color=0x14e1d4)
        irelia_buns = "ibaelia_images//IreliaBuns.jpg"
        file = discord.File(irelia_buns, filename="image.png")
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text="uwu")
        await ctx.send(file=file, embed=embed)

    @commands.command(aliases=['hewlp', 'hwelp', 'hwewlp', 'hewelp'], hidden=True)
    async def _help(self, ctx):
        await ctx.send_help()
        
def setup(bot):
    bot.add_cog(IbaeliaCommands(bot))