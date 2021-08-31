import discord
from discord import colour
from discord.ext import commands
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

import functions.convert_logging as cl
import functions.common_functions as cf
import functions.generic_functions
from functions.usage import record_usage, finish_usage

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level, version = "", "", ""

with open("./json_data/config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    version = config["bot_version"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

DEFAULT_PREFIX = "*"

class Owner(commands.Cog, description='Owner Functions'):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        log.debug(f'Attempting to Load {cog}')

        try:
            log.debug(f'Attempting Load of {cog}')
            self.client.load_extension(cog)
            log.debug(f'Loaded {cog}')
        except Exception as e:
            log.error(f'An Exception Occured, Sending Embed')
            await ctx.send(embed=discord.Embed(title=f'**`ERROR:`** {type(e).__name__} - {e}', colour=discord.Colour.red()))
        else:
            log.debug(f'Successfully Completed, Sending Embed')
            await ctx.send(embed=discord.Embed(title=f'Success!', colour=discord.Colour.green()))


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        log.debug(f'Attempting to Load {cog}')

        try:
            log.debug(f'Attempting Unload of {cog}')
            self.client.unload_extension(cog)
            log.debug(f'Unloaded {cog}')
        except Exception as e:
            log.error(f'An Exception Occured, Sending Embed')
            await ctx.send(embed=discord.Embed(title=f'**`ERROR:`** {type(e).__name__} - {e}', colour=discord.Colour.red()))
        else:
            log.debug(f'Successfully Completed, Sending Embed')
            await ctx.send(embed=discord.Embed(title=f'Success!', colour=discord.Colour.green()))


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        log.debug(f'Attempting to Reload {cog}')

        try:
            log.debug(f'Attempting Unload of {cog}')
            self.client.unload_extension(cog)
            log.debug(f'Unloaded {cog}')
            log.debug(f'Loading {cog}')
            self.client.load_extension(cog)
            log.debug(f'Loaded {cog}')
        except Exception as e:
            log.error(f'An Exception Occured, Sending Embed')
            await ctx.send(embed=discord.Embed(title=f'**`ERROR:`** {type(e).__name__} - {e}', colour=discord.Colour.red()))
        else:
            log.debug(f'Successfully Completed, Sending Embed')
            await ctx.send(embed=discord.Embed(title=f'Success!', colour=discord.Colour.green()))


def setup(client):
    client.add_cog(Owner(client))