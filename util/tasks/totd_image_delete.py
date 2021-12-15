import discord
from discord.ext import tasks, commands
import util.logging.convert_logging as convert_logging
import datetime
import os

log = convert_logging.get_logging()


@tasks.loop(time=datetime.time(hour=16, minute=58, second=50))
async def totd_delete(client: discord.Bot):
    if os.path.exists("./data/totd.jpg"):
        os.remove("./data/totd.jpg")
        log.debug(f"Removed Totd Image")
    else:
        log.debug(f"Totd Image Does Not Exist")
