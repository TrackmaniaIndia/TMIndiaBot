import discord
import requests
import os
import threading
import json
import country_converter as coco
import flag

import util.common_functions as common_functions
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from datetime import datetime, timezone, timedelta

# Setting up logging
log = convert_logging.get_logging()


def _get_current_totd() -> discord.Embed:
    log.debug(f"Getting TOTD Data from API")
    totd_data = requests.get("http://localhost:3000/tm2020/totd/latest").json()

    log.debug(f"Parsing TOTD Data")
    map_name = totd_data["name"]
    author_name = totd_data["authorplayer"]["name"]
    thumbnail_url = totd_data["thumbnailUrl"]
    author_time = common_functions.format_seconds(int(totd_data["authorScore"]))
    gold_time = common_functions.format_seconds(int(totd_data["goldScore"]))
    silver_time = common_functions.format_seconds(int(totd_data["silverScore"]))
    bronze_time = common_functions.format_seconds(int(totd_data["bronzeScore"]))

    mania_tags = totd_data["exchange"]["Tags"]

    nadeo_uploaded = totd_data["timestamp"]
    mx_uploaded = totd_data["exchange"]["UploadedAt"]

    wr_holder = totd_data["leaderboard"]["tops"][0]["player"]["name"]
    wr_time = common_functions.format_seconds(
        int(totd_data["leaderboard"]["tops"][0]["time"])
    )

    tmio_id = totd_data["mapUid"]
    tmx_code = totd_data["exchange"]["TrackID"]

    log.debug(f"Parsed TOTD Data")

    log.debug(f"Parsing Mania Tags to Strings")
    log.debug(f"Parsed Mania Tags to Strings")

    log.debug(f"Parsing Time Uploaded to Timestamps")
    nadeo_dt = datetime.strptime(nadeo_uploaded[:-6], "%Y-%m-%dT%H:%M:%S")
    mx_dt = datetime.strptime(mx_uploaded[:-3], "%Y-%m-%dT%H:%M:%S")

    nadeo_dt_utc = nadeo_dt.replace(tzinfo=timezone.utc)
    mx_dt_utc = mx_dt.replace(tzinfo=timezone.utc)

    nadeo_timestamp = int(nadeo_dt_utc.timestamp())
    mx_timestamp = int(mx_dt_utc.timestamp())
    log.debug(f"Parsed Time Uploaded to Timestamps")

    log.debug(f"Creating Strings from Parsed Data")
    medal_times = f"<:author:894268580902883379> {author_time}\n<:gold:894268580970004510> {gold_time}\n<:silver:894268580655411220> {silver_time}\n<:bronze:894268580181458975> {bronze_time}"
    world_record = f"Holder: {wr_holder}\nTime: {wr_time}"

    nadeo_uploaded = "<t:{}:R>".format(nadeo_timestamp)
    mx_uploaded = "<t:{}:R>".format(mx_timestamp)

    log.debug(f"Created Strings from Parsed Data")

    log.debug(f"Creating Embed")
    current_day = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d")
    current_month = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
        "%m"
    )
    embed = ezembed.create_embed(
        title="Here is the {} {} TOTD".format(current_day, current_month),
        color=discord.Colour.nitro_pink(),
    )
    embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Map Name", value=map_name, inline=True)
    embed.add_field(name="Author", value=author_name, inline=True)
    embed.add_field(
        name="Time Uploaded to Nadeo Server", value=nadeo_uploaded, inline=False
    )
    embed.add_field(name="Time Uploaded to TMX", value=mx_uploaded, inline=True)
    embed.add_field(name="Medal Times", value=medal_times, inline=False)
    embed.add_field(name="World Record", value=world_record, inline=False)
    embed.add_field(
        name="Links",
        value="[TMIO]({}) | [TMX]({})".format(
            "https://trackmania.io/#/leaderboard/{}".format(tmio_id),
            "https://trackmania.exchange/maps/{}/".format(tmx_code),
        ),
        inline=False,
    )

    log.debug(f"Created Embed")
    return embed
