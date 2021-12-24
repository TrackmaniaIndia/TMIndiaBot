import datetime
import json

import discord
from discord.ext import tasks

from util.logging import convert_logging

log = convert_logging.get_logging()


@tasks.loop(minutes=10)
async def change_status(client: discord.Bot, statuses: dict):
    """Changes Bot Status Every 10 minutes

    Args:
        client (discord.Bot): The bot client
        statuses (dict): The statuses to parse
    """
    log.debug(
        f"10 Minutes have Passed, Changing Status at - {datetime.datetime.utcnow()}"
    )
    log.debug("Checking for First Time")

    log.debug("Changing Status")

    await client.change_presence(activity=discord.Game(next(statuses)))

    log.debug("Changed Status")


def get_statuses():
    with open("./data/json/statuses.json", "r", encoding="UTF-8") as file:
        return json.load(file)
