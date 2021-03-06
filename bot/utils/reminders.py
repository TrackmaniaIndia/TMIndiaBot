import datetime
import json
import traceback

import discord.ext.tasks as tasks

from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


@tasks.loop(
    time=datetime.time(hour=16, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def main_cotd_reminder(bot: Bot):
    log.debug("Starting Main COTD Reminder Task.")

    async for guild in bot.fetch_guilds():
        await __send_message(bot, guild.id, "one", False)


@tasks.loop(
    time=datetime.time(hour=0, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def first_rerun_cotd_reminder(bot: Bot):
    log.debug("Starting First Rerun COTD Reminder Task.")

    async for guild in bot.fetch_guilds():
        await __send_message(bot, guild.id, "two", False)


@tasks.loop(
    time=datetime.time(hour=8, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def second_rerun_cotd_reminder(bot: Bot):
    log.debug("Starting Second Rerun COTD Reminder Task.")

    async for guild in bot.fetch_guilds():
        await __send_message(bot, guild.id, "three", False)


@tasks.loop(
    time=datetime.time(hour=17, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def main_royal_reminder(bot: Bot):
    log.debug("Starting Main Royal Reminder Task.")

    async for guild in bot.fetch_guilds():
        await __send_message(bot, guild.id, "one", True)


@tasks.loop(
    time=datetime.time(hour=1, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def first_rerun_royal_reminder(bot: Bot):
    log.debug("Starting First Rerun Royal Reminder Task.")

    async for guild in bot.fetch_guilds():
        await __send_message(bot, guild.id, "two", True)


@tasks.loop(
    time=datetime.time(hour=9, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def second_rerun_royal_reminder(bot: Bot):
    log.debug("Starting Second Rerun Royal Reminder Task.")

    async for guild in bot.fetch_guilds():
        await __send_message(bot, guild.id, "three", True)


async def __send_message(
    bot: Bot, guild_id: int, type: str = "one", royal: bool = False
):
    log.debug("Opening Config File for %s", guild_id)

    with open(
        f"./bot/resources/guild_data/{guild_id}/config.json", "r", encoding="UTF-8"
    ) as file:
        config_data = json.load(file)

    if royal:
        reminder_channel_name = "royal_reminder_channel"
        reminder_flag_name = f"royal_{type}_reminder"
        competition = "Royal"
        role_name = f"royal_{type}_role"
    else:
        reminder_channel_name = "cotd_reminder_channel"
        reminder_flag_name = f"cotd_{type}_reminder"
        competition = "COTD"
        role_name = f"cotd_{type}_role"

    reminder_channel_id = config_data.get(reminder_channel_name, 0)

    if reminder_channel_id == 0:
        log.debug("No COTD Main Reminder Channel for %s", guild_id)
        return

    reminder_channel = bot.get_channel(reminder_channel_id)

    if config_data.get(reminder_flag_name, False):
        # Change string type to a number
        if type == "one":
            type = 1
        elif type == "two":
            type = 2
        else:
            type = 3

        # Check if the guild owner set a role for the reminder.
        role_id = config_data.get(role_name, 0)

        if role_id != 0:
            guild = bot.get_guild(guild_id)
            role = guild.get_role(role_id)
        else:
            role = None

        try:
            if role is not None:
                log.debug("Role is set for %s", guild_id)
                msg = f"Hey {role.mention}!\nThere's 15 minutes left for {competition} #{type}"
            else:
                msg = (
                    f"Hey Everyone!\nThere's 15 minutes left for {competition} #{type}"
                )

            await reminder_channel.send(content=msg)
        except:
            log.error(
                "Something went wrong sending the message to the channel of %s.\n%s",
                guild_id,
                traceback.format_exc(),
            )
