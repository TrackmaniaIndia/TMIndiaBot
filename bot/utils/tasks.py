import datetime
import os
import sys
import os

from discord.ext import tasks

import discord
from bot import constants
from bot.api import APIClient
from bot.bot import Bot
from bot.log import get_logger
from bot import constants
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


@tasks.loop(minutes=10)
async def change_status(bot: Bot, statuses: dict):
    """Changes Bot Status Every 10 minutes
    Args:
        client (discord.Bot): The bot client
        statuses (dict): The statuses to parse
    """
    log.debug("Changing Status")
    await bot.change_presence(activity=discord.Game(next(statuses)))
    log.debug("Changes Status")


@tasks.loop(minutes=15)
async def keep_alive(bot: Bot):
    log.debug("Keeping Bot Alive")

    try:
        await _ping_api()
        log.debug("API Ping Successfull")
    except:
        log.error("API is Offline")
        sys.exit(-1)

    log.debug("Sending a Message to the Designated Channel")
    channel = bot.get_channel(881732050451849216)
    await channel.send(f"Bot is still alive at {datetime.datetime.utcnow()} UTC")


@tasks.loop(time=datetime.time(hour=16, minute=58, second=50))
async def totd_image_deleter(bot: Bot):
    if os.path.exists("./bot/resources/temp/totd.png"):
        os.remove("./bot/resources/temp/totd.png")
        log.debug("Removed the TOTD Image")
    else:
        log.debug("TOTD Image does not exist")


@tasks.loop(time=datetime.time(hour=0, minute=30, second=0))
async def todays_birthday(bot: Bot):
    log.debug("Checking if it is anyone's birthday today")
    birthday_embed = Birthday.today_birthday()

    if birthday_embed is not None:
        log.debug("A birthday is today")

        log.debug("Getting channel")

        try:
            tmi_guild = bot.get_guild(constants.Guild.tmi_guild)
            general_channel = bot.get_guild(constants.Channels.general)

            await general_channel.send(embed=birthday_embed)
        except:
            log.debug("Testing bot is running")
            return

    log.debug("There is no birthday today")
    return


async def _ping_api():
    api_client = APIClient()

    try:
        await api_client.get("http://localhost:3000/")
    except:
        log.error("API is OFFLINE")
        # raise OfflineAPI("API is Offline")
    await api_client.close()
    del api_client


class OfflineAPI(Exception):
    def __init__(self, excp: Exception):
        self.message = excp.message

    def __str__(self):
        return self.message if self.message is not None else None
