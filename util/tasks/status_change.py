import util.logging.convert_logging as cl
import discord
from discord.ext import tasks, commands
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import json

log = cl.get_logging()


@tasks.loop(minutes=10)
async def change_status(client, statuses, first_time):
    """Changes Status Every 10 Minutes

    Args:
        client ([type]): [description]
        statuses ([type]): [description]
        first_time ([type]): [description]

    Returns:
        [type]: [description]
    """
    log.debug(f"10 Minutes have Passed, Changing Status at - {datetime.utcnow()}")
    log.debug(f"Checking for First Time")
    if first_time:
        log.debug(f"First Time is True, returning")
        first_time = False
        return None

    log.debug(f"Changing Status")

    await client.change_presence(activity=discord.Game(next(statuses)))

    log.debug(f"Changed Status")


def get_statuses():
    with open("./data/json/statuses.json", "r") as file:
        return json.load(file)
