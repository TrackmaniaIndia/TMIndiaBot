import datetime
import discord

from util.logging import convert_logging

from discord.ext import tasks


log = convert_logging.get_logging()


@tasks.loop(time=datetime.time(hour=16, minute=45, seconds=0))
async def main_cotd_reminder(client: discord.Bot):
    log.debug("Time is 11:30pm, Main COTD Starts in 15 Minutes")
    log.debug("Getting Channel to Send the Reminder")
    reminder_channel = client.get_channel()  # Insert Channel ID here
    log.debug("Getting Role to Ping")
    ping_role_main = discord.Guild.get_role()  # Insert Ping Role here
