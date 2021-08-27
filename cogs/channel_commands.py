import discord
from discord.ext import commands
import json
import logging
from datetime import datetime
from discord.utils import valid_icon_size
from dotenv import load_dotenv
import requests
import os
import asyncio
from disputils import pagination
from disputils.pagination import BotEmbedPaginator

import functions.tm_commands_functions
import functions.convert_logging as cl
import functions.common_functions as cf
from functions.usage import record_usage, finish_usage

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level, version = "", "", ""

with open("./json_files/config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    version = config["bot_version"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

DEFAULT_PREFIX = "*"

class ChannelCommands(commands.Cog, description='Administrator Commands for Bot Functions'):
    def __init__(self, client):
        self.client = client

    @commands.command(name='SetAnnouncementChannel', aliases=['SetStartupChannel', 'SetBootUpChannel', 'SAC'], help='Set a channel for the bot to send messages when it starts up')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_announcement_channel(self, ctx, channel: discord.TextChannel):
        log.debug(f'Opening announcement_channels json file')

        with open('./json_files/announcement_channels.json', 'r') as file:
            log.debug(f'Reading json file')
            channels = json.load(file)
            log.debug(f'Read json file')
            file.close()

        channels["announcement_channels"].append(str(channel.id))

        log.debug(f'Writing to announcement_channels.json')
        with open('./json_files/announcement_channels.json', 'w') as file:
            log.debug(f'Dumping Prefixes to File')
            json.dump(channels, file, indent=4)
            file.close()

        log.debug('Finished setting channel for {}'.format(ctx.guild.id))
        await ctx.send(embed=discord.Embed(title=f'#{channel.name} has been added to announcements file', color=cf.get_random_color()))


    @commands.command(name='RemoveAnnouncementChannel', aliases=['RemoveStartupChannel', 'RemoveBootUpChannel', 'RAC'], help='Remove a channel for the bot to send messages when it starts up')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def remove_announcement_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        log.debug(f'Reading announcement_channels.json')

        with open('./json_files/announcement_channels.json', 'r')as file:
            log.debug(f'Reading json file')
            announcement_channels = json.load(file)
            log.debug(f'Read json file')
            file.close()

        if str(channel.id) not in announcement_channels['announcement_channels']:
            log.error(f'{str(channel.id)} is not in the json file')
            await ctx.send(embed=discord.Embed(title='That channel is not in the json file', color=0xff0000))
            return None

        log.debug(f'Removing {channel.id}')
        announcement_channels['announcement_channels'].remove(str(channel.id))
        log.debug(f'Removed {channel.id}')

        log.debug(f'Writing to JSON File')
        with open('./json_files/announcement_channels.json', 'w') as file:
            log.debug(f'Dumping to JSON File')
            json.dump(announcement_channels, file, indent=4)
            log.debug(f'Dumped to JSON file')
            file.close()

        await ctx.send(embed=discord.Embed(title=f'#{channel.name} has been removed from announcements file', color=cf.get_random_color()))

    @set_announcement_channel.error
    async def set_announcement_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title='Missing Permissions', color=discord.Color.red()).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title='Please Send a Channel Along With the Command', color=discord.Colour.red()).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url))
            return

    @remove_announcement_channel.error
    async def remove_announcement_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title='Missing Permissions', color=discord.Color.red()).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title='Please Send a Channel Along With the Command', color=discord.Colour.red()).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url))
            return


def setup(client):
    client.add_cog(ChannelCommands(client))