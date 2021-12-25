import json
import datetime
import discord
from discord.ext import tasks
from util.logging import convert_logging
from util.trackmania.tm2020.totd import _get_current_totd
from util.discord.view_adder import ViewAdder

log = convert_logging.get_logging()


# Testing Server
# Guild ID: 876042400005505066
# Channel ID: 876042400731123724

# Main Server
# Guild ID: 735180785799096704
# Channel ID: 842626496437813258

# All Times are in UTC

# 15 Minutes Before the COTD
@tasks.loop(
    time=datetime.time(hour=17, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def cotd_one_reminder(client: discord.Bot):
    log.info("It is Time for COTD Rerun")

    log.debug(f"Checking Config File")
    with open("./data/config.json", "r", encoding="UTF-8") as file:
        config_data = json.load(file)

        if config_data["totdReminders"] is False:
            log.critical("TOTD Reminders are Switched off")
            return

    log.info("Pinging COTD #3 Role in TM India")

    guild = client.get_guild(735180785799096704)

    channel_id = 842626496437813258 if guild is not None else 876042400731123724
    role_id = 924146405642219520 if guild is not None else 924150185020522577

    if guild is None:
        log.debug("Running Testing Bot")
        guild = client.get_guild(876042400005505066)

    log.debug(f"Getting Channel with ID -> {channel_id} and Role with ID -> {role_id}")
    channel = client.get_channel(channel_id)
    role = guild.get_role(role_id)

    message = f"{role.mention}: **COTD starts in 15 minutes!**\n\n:medal: Past COTD Results: <https://trackmania.io/#/totd>"

    log.debug("Sending Message")
    await channel.send(content=message)


# 15 Minutes Before COTD
@tasks.loop(
    time=datetime.time(hour=9, minute=45, second=0, tzinfo=datetime.timezone.utc)
)
async def cotd_three_reminder(client: discord.Bot):
    log.info("It is Time for COTD Rerun")

    log.debug(f"Checking Config File")
    with open("./data/config.json", "r", encoding="UTF-8") as file:
        config_data = json.load(file)

        if config_data["totdReminders"] is False:
            log.critical("TOTD Reminders are Switched off")
            return

    log.info("Pinging COTD #3 Role in TM India")

    guild = client.get_guild(735180785799096704)

    channel_id = 842626496437813258 if guild is not None else 876042400731123724
    role_id = 924146521405026375 if guild is not None else 924150185020522577

    if guild is None:
        log.debug("Running Testing Bot")
        guild = client.get_guild(876042400005505066)

    log.debug(f"Getting Channel with ID -> {channel_id} and Role with ID -> {role_id}")
    channel = client.get_channel(channel_id)
    role = guild.get_role(role_id)

    message = f"{role.mention}: **COTD Rerun starts in 15 minutes!**\n\n:medal: Past COTD Results: <https://trackmania.io/#/totd>"

    log.debug("Sending Message")
    await channel.send(content=message)


@tasks.loop(
    time=datetime.time(hour=18, minute=0, second=5, tzinfo=datetime.timezone.utc)
)
async def totd_info(client: discord.Bot):
    log.info("It is 11:30.05pm, getting totd information")

    log.debug("Getting TM2020 Channel")
    channel = client.get_channel(842626496437813258)

    if channel is None:
        log.debug("Channel is NoneType")
        channel = client.get_channel(876042400731123724)

    embed, image, download_link, tmio_link, tmx_link = _get_current_totd()

    log.info("Creating Buttons to Add")
    download_map = discord.ui.Button(
        label="Download Map!", style=discord.ButtonStyle.primary, url=download_link
    )
    tmio_button = discord.ui.Button(
        label="TMIO", style=discord.ButtonStyle.url, url=tmio_link
    )

    if tmx_link is not None:
        tmx_button = discord.ui.Button(
            label="TMX", style=discord.ButtonStyle.url, url=tmx_link
        )

        log.info("Sending TOTD Embed")
        await channel.send(
            file=image,
            embed=embed,
            view=ViewAdder([download_map, tmio_button, tmx_button]),
        )
    else:
        log.info("Sending TOTD Embed")

        await channel.send(
            file=image,
            embed=embed,
            view=ViewAdder([download_map, tmio_button]),
        )
