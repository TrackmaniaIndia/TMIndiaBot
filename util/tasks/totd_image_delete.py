import discord
import datetime
import os

import util.logging.convert_logging as convert_logging

from discord.ext import tasks, commands


log = convert_logging.get_logging()


@tasks.loop(time=datetime.time(hour=16, minute=58, second=50))
async def totd_deleter(client: discord.Bot):
    if os.path.exists("./data/temp/totd.png"):
        os.remove("./data/temp/totd.png")
        log.debug(f"Removed Totd Image")
    else:
        log.debug(f"Totd Image Does Not Exist")
