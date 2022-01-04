import datetime
import sys

from discord.ext import tasks

import discord
from bot.api import APIClient
from bot.bot import Bot
from bot.log import get_logger

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
    channel = bot.get_channel()
    await channel.send(f"Bot is still alive at {datetime.datetime.utcnow()} UTC")


@tasks.loop(time=datetime.time(hour=16, minute=58, second=50))
async def totd_image_deleter(bot: Bot):
    if os.path.exists("./bot/resources/temp/totd.png"):
        os.remove("./bot/resources/temp/totd.png")
        log.debug("Removed the TOTD Image")
    else:
        log.debug("TOTD Image does not exist")


async def _ping_api():
    api_client = APIClient()

    try:
        await api_client.get("http://localhost:3000/")
    except:
        log.error("API is OFFLINE")
        raise OfflineAPI("API is Offline")
    await api_client.close()
    del api_client


class OfflineAPI(Exception):
    def __init__(self, excp: Exception):
        self.message = excp.message

    def __str__(self):
        return self.message if self.message is not None else None
