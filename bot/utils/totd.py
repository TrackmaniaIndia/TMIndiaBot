from datetime import datetime

import discord
from trackmania import TOTD, TMXMap

import bot.utils.commons as commons
from bot import constants
from bot.log import get_logger
from bot.utils.discord import create_embed

log = get_logger(__name__)

MAP_TYPE_ENUMS: dict = {
    1: "Race",
    2: "FullSpeed",
    3: "Tech",
    4: "RPG",
    5: "LOL",
    6: "Press Forward",
    7: "SpeedTech",
    8: "MultiLap",
    9: "Offroad",
    10: "Trial",
    11: "ZrT",
    12: "SpeedFun",
    13: "Competitive",
    14: "Ice",
    15: "Dirt",
    16: "Stunt",
    17: "Reactor",
    18: "Platform",
    19: "Slow Motion",
    20: "Bumper",
    21: "Fragile",
    22: "Scenery",
    23: "Kacky",
    24: "Endurance",
    25: "Mini",
    26: "Remake",
    27: "Mixed",
    28: "Nascar",
    29: "SpeedDrift",
    30: "Minigame",
    31: "Obstacle",
    32: "Transitional",
    33: "Grass",
    34: "Backwards",
    35: "Freewheel",
    36: "Signature",
    37: "Royal",
    38: "Water",
    39: "Plastic",
    40: "Arena",
    41: "N/A",
    42: "Educational",
}


async def parse_totd_data(
    totd_data: TOTD,
    month: int | None,
) -> tuple[discord.Embed, list[discord.ui.Button]]:
    log.debug("Parsing Values")
    map_name = totd_data.map.name
    author_name = totd_data.map.author_name
    _todays_date = datetime.now()

    if month is None:
        month = _todays_date.month - 1

    title_string = f"Track of the Day of {commons.get_ordinal_number(totd_data.month_day)} {constants.Consts.months[month]}"
    nadeo_uploaded = f"<t:{int(totd_data.map.uploaded.timestamp())}:R>"
    map_download = totd_data.map.url
    tmio_url = f"https://trackmania.io/#/leaderboard/{totd_data.map.uid}"

    log.debug("Creating Embed")
    page_one = create_embed(title=title_string)

    medal_str = (
        f"{constants.Emojis.author_medal} {totd_data.map.medal_time.author_string}\n"
        + f"{constants.Emojis.gold_medal} {totd_data.map.medal_time.gold_string}\n"
        + f"{constants.Emojis.silver_medal} {totd_data.map.medal_time.silver_string}\n"
        + f"{constants.Emojis.bronze_medal} {totd_data.map.medal_time.bronze_string}\n"
    )

    log.debug("Creating Buttons")
    map_download_button = discord.ui.Button(
        label="Download Map!", style=discord.ButtonStyle.url, url=map_download
    )
    tmio_url_button = discord.ui.Button(
        label="TMIO Link", style=discord.ButtonStyle.url, url=tmio_url
    )

    log.debug("Updating Embed Page 1")
    page_one.add_field(name="Map Name", value=map_name, inline=True)
    page_one.add_field(name="Author Name", value=author_name, inline=True)
    page_one.add_field(name="Medals", value=medal_str, inline=False)
    page_one.add_field(name="Uploaded", value=nadeo_uploaded, inline=True)
    page_one.set_image(url=totd_data.map.thumbnail)

    if totd_data.map.exchange_id == 0:
        log.debug("Map was not uploaded to TMX")
        return page_one, [map_download_button, tmio_url_button]

    log.debug("Getting Data from TMX")
    tmx_data = await TMXMap.get_map(totd_data.map.exchange_id)
    uploaded_tmx = f"<t:{int(tmx_data.times.uploaded.timestamp())}:R>"
    tags = ""
    log.warn(tmx_data.tags.map_tags)
    for tag in tmx_data.tags.map_tags:
        tags = tags + f"{MAP_TYPE_ENUMS.get(tag)}, "

    tags = tags[:-2]

    log.debug("Adding TMX Main Data")
    page_one.add_field(name="Uploaded (TMX)", value=uploaded_tmx, inline=True)
    page_one.add_field(name="Tags", value=tags, inline=False)

    tmx_button = discord.ui.Button(
        label="TMX Page",
        style=discord.ButtonStyle.url,
        url=f"https://trackmania.exchange/maps/{totd_data.map.exchange_id}",
    )

    return page_one, [map_download_button, tmio_url_button, tmx_button]
