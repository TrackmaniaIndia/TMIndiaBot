import discord
import requests
import os
import threading
import json
import country_converter as coco
import flag
import re
import shutil

import util.common_functions as common_functions
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from datetime import datetime, timezone, timedelta

# Setting up logging
log = convert_logging.get_logging()


def _get_current_totd():
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
    try:
        mx_dt = datetime.strptime(mx_uploaded[:-3], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        mx_dt = datetime.strptime(mx_uploaded[:-4], "%Y-%m-%dT%H:%M:%S")
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

    log.debug(f"Getting Map Thumbnail")
    log.debug(f"Checking if Map Thumbnail has Already been Downloaded")
    if not os.path.exists(f"./data/totd.png"):
        log.critical(f"Map Thumbnail has not been Downloaded")
        _download_thumbnail(thumbnail_url)

    log.debug(f"Creating Embed")
    current_day = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d")
    current_month = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
        "%B"
    )

    if int(current_day) % 10 == 1:
        day_suffix = "st"
    elif int(current_day) % 10 == 2:
        day_suffix = "nd"
    elif int(current_day) % 10 == 3:
        day_suffix = "rd"
    else:
        day_suffix = "th"

    embed = ezembed.create_embed(
        title="Here is the {}{} {} TOTD".format(current_day, day_suffix, current_month),
        color=discord.Colour.nitro_pink(),
    )
    log.debug(f"Creating Image File")
    image = discord.File("data/totd.png", filename="totd.png")
    embed.set_image(url="attachment://totd.png")
    embed.add_field(name="Map Name", value=map_name, inline=True)
    embed.add_field(name="Author", value=author_name, inline=True)
    embed.add_field(name="Tags", value=_parse_mx_tags(mania_tags), inline=True)
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
    return embed, image


def _download_thumbnail(url: str) -> None:
    req = requests.get(url, stream=True)

    if os.path.exists(f"./data/totd.png"):
        log.debug(f"Thumbnail already downloaded")
        return

    # Checks if the Image was Retrieved Successfully
    if req.status_code == 200:
        log.debug(f"Image was retrieved succesfully")
        req.raw.decode_content = True

        log.debug(f"Saving Image to File")
        with open("./data/totd.png", "wb") as file:
            shutil.copyfileobj(req.raw, file)
    else:
        log.critical(f"Image could not be retrieved")


def _parse_mx_tags(tags: str) -> str:
    log.debug(f"Tags -> {tags}")
    log.debug(f"Removing Spaces")
    tags.replace(" ", "")
    log.debug(f"Without Spaces -> {tags}")

    tags = tags.split(",")

    tag_string = ""

    with open("./data/json/mxtags.json", "r") as file:
        mxtags = json.load(file)["mx"]

        for i, tag in enumerate(tags):
            log.debug(f"Converting {tag}")

            for j in range(len(mxtags)):
                if int(tag) == int(mxtags[j]["ID"]):
                    tag_string = tag_string + mxtags[j]["Name"] + ", "

    log.debug(f"Tag String -> {tag_string}")
    return tag_string[:-2]
