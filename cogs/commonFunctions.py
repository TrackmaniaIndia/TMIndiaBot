import logging
import os
from dotenv import load_dotenv
from requests import get
import random
import time
import discord
from discord.ext import commands

try:
    import cogs.convertLogging as cl
except:
    import convertLogging as cl

load_dotenv()
log_level = os.getenv("LOG_LEVEL")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)


def getRandomColor():
    log.debug(f"getRandomColor called")
    colors = (
        0x000000,
        0xFFFFFF,
        0x028C6A,
        0xFAA2B0,
        0x82B741,
        0x00AEEF,
        0xFF9FF6,
        0x6289FF,
        0x41FF00,
        0x00FFFF,
        0x800080,
        0xFFFF00,
        0xFF0000,
        0xFF00FF,
        0x00FF00,
        0xAABBCC,
        0xCCAABB,
        0xFF2FF2,
        0x23FFFF,
    )

    rInt = random.randint(0, len(colors) - 1)

    log.debug(f"Random Number is: {rInt} - Color Being Returned is: {colors[rInt]}")
    return colors[rInt]


def makeString(my_list: list) -> str:
    list_string = ""

    for list_item in my_list:
        log.debug(f"Adding {list_item} to String")

        list_string += list_item + " "

    return list_string


if __name__ == "__main__":
    for i in range(0, 100):
        print(f"{getRandomColor()}")
