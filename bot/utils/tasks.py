import datetime
import os
import sys
import json

import discord
from discord.ext import tasks

from bot import constants
from bot.api import APIClient
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.discord import ViewAdder
from bot.utils.birthdays import Birthday
from bot.utils.trackmania import TrackmaniaUtils

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
    """Keeps bot alive by sending a message to a designated channel and pings the API."""
    log.debug("Keeping Bot Alive")

    try:
        await _ping_api()
        log.debug("API Ping Successfull")
    except BaseException:
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


@tasks.loop(
    time=datetime.time(hour=0, minute=30, second=0, tzinfo=datetime.timezone.utc)
)
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
        except BaseException:
            log.debug("Testing bot is running")
            return

    log.debug("There is no birthday today")
    return


# 15 minutes before the COTD
@tasks.loop(
    time=datetime.time(hour=17, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def cotd_one_reminder(bot: Bot):
    log.info("It is time for COTD #1")

    log.debug("Checking config file")
    if constants.Bot.totd_reminders is False:
        log.critical("TOTD Reminders are disabled")
        return

    log.info("Pinging COTD #1 Role in TM India")
    guild = bot.get_guild(constants.Guild.tmi_server)

    channel_id = (
        constants.Channels.general
        if guild is not None
        else constants.Channel.testing_general
    )
    role_id = (
        constants.Role.cotd_reminder_one
        if guild is not None
        else constants.Role.cotd_reminder_one_testing
    )

    guild = (
        guild if guild is not None else bot.get_guild(constants.Guild.testing_server)
    )

    channel, role = bot.get_channel(channel_id), guild.get_role(role_id)

    message = f"{role.mention}: **COTD starts in 15 minutes**\n\n:medal: Past COTD results: <https://trackmania.io/#/totd>"

    log.debug("Sending Message")
    await channel.send(content=message)


# 15 Minutes before the COTD
@tasks.loop(
    time=datetime.time(hour=9, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def cotd_three_reminder(bot: Bot):
    log.info("it is time for COTD Rerun #3")

    log.debug("Checking config file")
    if constants.Bot.totd_reminders is False:
        log.critical("TOTD Reminders are disabled")
        return

    log.info("Pinging COTD #3 Role in TM India")
    guild = bot.get_guild(constants.Guild.tmi_server)

    channel_id = (
        constants.Channels.general
        if guild is not None
        else constants.Channel.testing_general
    )
    role_id = (
        constants.Role.cotd_reminder_three
        if guild is not None
        else constants.Role.cotd_reminder_three_testing
    )

    guild = (
        guild if guild is not None else bot.get_guild(constants.Guild.testing_server)
    )

    channel, role = bot.get_channel(channel_id), guild.get_role(role_id)

    message = f"{role.mention}: **COTD Reminder #3 starts in 15 minutes**\n\n:medal: Past COTD results: <https://trackmania.io/#/totd>"

    log.debug("Sending Message")
    await channel.send(content=message)


async def _ping_api():
    api_client = APIClient()

    try:
        await api_client.get("http://localhost:3000/")
    except BaseException:
        log.error("API is OFFLINE")
        # raise OfflineAPI("API is Offline")
    await api_client.close()
    del api_client


class OfflineAPI(Exception):
    def __init__(self, excp: Exception):
        self.message = excp.message

    def __str__(self):
        return self.message if self.message is not None else None
