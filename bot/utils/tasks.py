import datetime
import os
import sys

import discord
import requests
from discord.ext import tasks

from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.birthdays import Birthday
from bot.utils.cotd_util import TOTDUtils
from bot.utils.discord import ViewAdder

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
        await _ping_api(bot)
        log.debug("API Ping Successfull")
    except BaseException:
        sys.exit(-1)

    log.debug("Sending a Message to the Designated Channel")
    channel = bot.get_channel(constants.Channels.tmi_bot_channel)
    await channel.send(f"Bot is still alive at {datetime.datetime.utcnow()} UTC")


@tasks.loop(
    time=datetime.time(hour=16, minute=58, second=50, tzinfo=datetime.timezone.utc)
)
async def totd_image_deleter(bot: Bot):
    if os.path.exists("./bot/resources/temp/totd.png"):
        os.remove("./bot/resources/temp/totd.png")
        log.debug("Removed the TOTD Image")
    else:
        log.debug("TOTD Image does not exist")

    if os.path.exists("./bot/resources/json/totd.json"):
        os.remove("./bot/resources/json/totd.json")
        log.debug("Removed TOTD Json")
    else:
        log.debug("TOTD JSON does not exist")


@tasks.loop(
    time=datetime.time(hour=8, minute=56, second=30, tzinfo=datetime.timezone.utc)
)
async def todays_birthday(bot: Bot):
    log.debug("Checking if it is anyone's birthday today")
    birthdays_list = Birthday.today_birthday()

    if birthdays_list is not None:
        log.info("There is a birthday today")

        if len(birthdays_list) > 1:
            log.debug("There are multiple birthdays today")

            log.debug("Getting channel")
            general_channel = bot.get_channel(constants.Channels.general)

            if general_channel is None:
                log.debug("Testing bot is running, getting testing discord channel")
                general_channel = bot.get_channel(constants.Channels.testing_general)

            for birthday_embed in birthdays_list:
                log.debug(f"Sending {birthday_embed}")
                await general_channel.send(
                    content="Hey Everyone! Today we have a birthday",
                    embed=birthday_embed,
                )
            return
        else:
            log.debug("Only one birthday today")

            log.debug("Getting channel")
            general_channel = bot.get_channel(constants.Channels.general)

            if general_channel is None:
                log.debug("Testing bot is running, getting testing discord channel")
                general_channel = bot.get_channel(constants.Channels.testing_general)

            log.debug(f"Sending {birthdays_list[0]}")
            await general_channel.send(
                content="Hey Everyone! Today we have a birthday",
                embed=birthdays_list[0],
            )
            return
    else:
        log.debug("No birthdays today")
        return


@tasks.loop(
    time=datetime.time(hour=17, minute=0, second=0, tzinfo=datetime.timezone.utc)
)
async def today_totd(bot: Bot):
    log.info("Getting TOTD Info")
    log.info("Getting TOTD Information")
    (
        totd_embed,
        image,
        download_link,
        tmio_link,
        tmx_link,
    ) = await TOTDUtils.today()
    log.info("Got Information, Sending Response")

    log.info("Creating Buttons to Add")
    download_map = discord.ui.Button(
        label="Download Map!", style=discord.ButtonStyle.primary, url=download_link
    )
    tmio_button = discord.ui.Button(
        label="TMIO", style=discord.ButtonStyle.url, url=tmio_link
    )

    log.debug("Getting the TM2020 Channel")
    tm2020_channel = bot.get_channel(constants.Channels.tm2020)
    if tm2020_channel is None:
        tm2020_channel = bot.get_channel(constants.Channels.testing_general)

    if constants.Bot.totd_info:
        log.info("Sending the TOTD Embed")

        if tmx_link is not None:
            tmx_button = discord.ui.Button(
                label="TMX", style=discord.ButtonStyle.url, url=tmx_link
            )

            await tm2020_channel.send(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button, tmx_button]),
            )
        else:
            await tm2020_channel.send(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button]),
            )
    else:
        log.info("TOTD Flag set to false, returning")
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


async def _ping_api(bot: Bot):
    try:
        await bot.wait_until_ready()
        # await api_client.get("http://localhost:3000/")
        requests.get("http://localhost:3000")
    except BaseException:
        return
        # raise OfflineAPI("API is Offline")


class OfflineAPI(Exception):
    def __init__(self, excp: Exception):
        self.message = excp.message

    def __str__(self):
        return self.message if self.message is not None else None
