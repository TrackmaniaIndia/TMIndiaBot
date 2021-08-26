import discord
from discord.ext import commands
import json
import logging
import datetime
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

class SetChannelCommands(commands.Cog, description='Administrator Commands for Bot Functions'):
    def __init__(self, client):
        self.client = client

    @commands.command(name='SetAnnouncementChannel', aliases=['SetStartupChannel', 'SetBootUpChannel'], help='Set a channel for the bot to send messages when it starts up')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(administrator=True)
    async def set_announcement_channel(self, ctx, channel: discord.TextChannel):
        log.debug(f'Opening announcement_channels json file')

        with open('./json_files/announcement_channels.json', 'r') as file:
            log.debug(f'Reading json file')
            channels = json.load(file)
            log.debug(f'Read json file')
            file.close()

        channels[str(ctx.guild.id)] = str(channel.id)

        log.debug(f'Writing to announcement_channels.json')
        with open('./json_files/announcement_channels.json', 'w') as file:
            log.debug(f'Dumping Prefixes to File')
            json.dump(channels, file, indent=4)
            file.close()

        log.debug('Finished setting channel for {}'.format(ctx.guild.id))


def setup(client):
    client.add_cog(SetChannelCommands(client))