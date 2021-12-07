import util.logging.convert_logging as convert_logging
import discord
from discord.ext import tasks
from datetime import datetime
from dotenv import load_dotenv
import json

log = convert_logging.get_logging()


@tasks.loop(minutes=10)
async def change_status(client: discord.Bot, statuses: dict):
    """Changes Bot Status Every 10 minutes

    Args:
        client (discord.Bot): The bot client
        statuses (dict): The statuses to parse
    """
    log.debug(f"10 Minutes have Passed, Changing Status at - {datetime.utcnow()}")
    log.debug(f"Checking for First Time")

    log.debug(f"Changing Status")

    await client.change_presence(activity=discord.Game(next(statuses)))

    log.debug(f"Changed Status")


def get_statuses():
    with open("./data/json/statuses.json", "r") as file:
        return json.load(file)
