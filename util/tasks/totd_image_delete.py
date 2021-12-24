import datetime
import os
import discord

from util.logging import convert_logging

from discord.ext import tasks

log = convert_logging.get_logging()


@tasks.loop(time=datetime.time(hour=16, minute=58, second=50))
async def totd_deleter(client: discord.Bot):
    if os.path.exists("./data/temp/totd.png"):
        os.remove("./data/temp/totd.png")
        log.debug("Removed Totd Image")
    else:
        log.debug("Totd Image Does Not Exist")
