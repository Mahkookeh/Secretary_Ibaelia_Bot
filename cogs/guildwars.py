import discord
from discord.ext import commands
# from discord import option
import requests
import os
import json

class GuildWarsCommands(commands.Cog):
    """Ibaelia Bot's Guild Wars Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="uploadLogs", usage="<UrlListFilename> [PhaseConfigFilename=None]", description="", show_parameter_descriptions=False, arguments_heading=False, pass_context=True)
    # @option("urlListName", str, description="The name of the file containing all urls to parse in the LogParser.")
    # @option("phaseConfigName", str, description="The name of the file containing the phase configurations. If a phase config file isn't sent, the default phase configurations will be used.")
    async def upload_logs(self, ctx, urlListName : str, phaseConfigName: str = None) -> None:
        """Upload Logs to the LogParser database
        
        Upload your big dps logs to the log parser!

        Parameters
        ------------
        urlListName: str
            The name of the file containing all urls to parse in the LogParser.
        phaseConfigName: str (default: None)
            The name of the file containing the phase configurations. If a phase config file isn't sent, the default phase configurations will be used.

        Raises
        ------
        MissingRequiredArgumentError
            Required argument is missing.
        TooManyArgumentsError
            Too many arguments.
        """
        for attachment in ctx.message.attachments:
            try:
                url = attachment.url
                if url and attachment.filename in [urlListName, phaseConfigName]:
                    r = requests.get(url, allow_redirects=True)
                    file = attachment.filename
                    open(file, 'wb').write(r.content)
            except:
                pass
        payload = {}
        if phaseConfigName is None:
            with open(urlListName, 'rb') as urlList:
                payload = {'Url List' : urlList}
                r = requests.post('https://logparser.fly.dev/api/logs-with-data/', files = payload, auth=(os.getenv("LOGPARSER_USERNAME"), os.getenv("LOGPARSER_PASSWORD")))
        else:
            with open(urlListName, 'rb') as urlList, open(phaseConfigName, 'rb') as phaseConfig:
                payload = {'Url List' : urlList, 'Phase Config': phaseConfig}
                r = requests.post('https://logparser.fly.dev/api/logs-with-data/', files = payload, auth=(os.getenv("LOGPARSER_USERNAME"), os.getenv("LOGPARSER_PASSWORD")))
        
        embed = discord.Embed(title="Upload Logs", color=0x14e1d4)

        result_json = r.json()
        result_file = open('results.json', 'w')
        json.dump(result_json, result_file)
        result_file.close()
        if r.status_code == 200:
            embed.add_field(value='Upload successful!', name='\u200b')
        else:
            embed.add_field(value='Upload failed! Check the results file to see the error message.', name='\u200b')
        embed.set_footer(text="uwu")
        await ctx.send(embed=embed, file=discord.File('results.json'))
    
    @upload_logs.error
    async def upload_logs_error(self, ctx, error):
        """A local Error Handler for our command upload_logs.
        This will only listen for errors in upload_logs.
        The global on_command_error will still be invoked after.
        """
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You're missing a required argument idiot.¯\\_(ツ)_/¯\n**Usage: {ctx.prefix}{ctx.command.name} {ctx.command.signature}**")
        if isinstance(error, commands.FileNotFoundError): # TODO: Fix
            await ctx.send(f"You didn't attach a file with the right name idiot.¯\\_(ツ)_/¯\n**Usage: {ctx.prefix}{ctx.command.name} {ctx.command.signature}**")
        
async def setup(bot):
    await bot.add_cog(GuildWarsCommands(bot))