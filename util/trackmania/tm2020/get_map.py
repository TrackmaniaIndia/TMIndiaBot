import discord
import requests
import os

import util.logging.convert_logging as convert_logging


log = convert_logging.get_logging()


def get_tm2020_map(tmx_id: str) -> discord.Embed:
    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tm2020/trackinfo/{tmx_id}"

    log.debug(f"Requesting Response from API")
    response = requests.get(LEADERBOARD_URL)
    log.debug(f"Received Response From Api")

    log.debug(f"Checking API Response")
    if int(response.status_code) == 400:
        if response.json()["error"] == "INVALID_TMIO_UID":
            log.error("Invalid TMIO ID given")
            return discord.Embed(
                title=":warning: Invalid TMIO UId",
                description="The TMIO UID provided is invalid",
                color=discord.Colour.red(),
            )
    log.debug(f"API Response Checked")

    api_data = response.json()

    log.debug(f"Creating Embed")

    exchange = api_data["exchange"]
    author = api_data["authorplayer"]

    times = {
        "author": _format_time_int(api_data["authorScore"]),
        "gold": _format_time_int(api_data["goldScore"]),
        "silver": _format_time_int(api_data["silverScore"]),
        "bronze": _format_time_int(api_data["bronzeScore"]),
    }

    tag = ""

    try:
        if author["tag"]:
            tag = f'[{author["tag"]}] '
        else:
            tag = ""
    except KeyError as e:
        pass

    medals = _get_map_medals(times)
    uploadedAt = _parse_tmio_time_string(exchange["UploadedAt"])
    updatedAt = _parse_tmio_time_string(exchange["UpdatedAt"])

    embed = discord.Embed(
        title=api_data["name"],
        description=exchange["Comments"] if exchange["Comments"] else "No Comments",
    )
    embed.set_author(
        name=tag + author["name"],
        url=f"https://trackmania.io/#/player/{author['id']}" + str(exchange["UserID"]),
    )
    embed.add_field(name="Medals", value=medals, inline=False)
    embed.add_field(name="Mood", value=exchange["Mood"], inline=True)
    embed.add_field(name="Type", value=exchange["MapType"], inline=True)
    embed.add_field(name="Style", value=exchange["StyleName"], inline=True)
    embed.add_field(name="Length", value=exchange["LengthName"], inline=True)
    embed.add_field(name="Laps", value=exchange["Laps"], inline=True)
    embed.add_field(name="Difficulty", value=exchange["DifficultyName"], inline=True)
    embed.add_field(name="Uploaded at ", value=uploadedAt, inline=True)
    embed.add_field(name="Updated at ", value=updatedAt, inline=True)
    embed.add_field(
        name="Links",
        value=f"[Download]({api_data['fileUrl']}) | [TMX](https://trackmania.exchange/maps/{exchange['TrackID']}/) | [Trackmania.io](https://trackmania.io/#/leaderboard/{tmx_id})",
        inline=False,
    )

    embed.set_image(url=api_data["thumbnailUrl"])

    log.debug(f"Embed Created, Returning")
    return embed


def _get_map_medals(times: dict) -> str:
    return f"""
    <:author:894268580902883379> {times['author']}
    <:gold:894268580970004510> {times['gold']}
    <:silver:894268580655411220> {times['silver']}
    <:bronze:894268580181458975> {times['bronze']}
    """


def _format_time_int(time: int) -> str:
    time = str(time)

    return f"0:{time[:2]}.{time[2:]}"


def _parse_tmio_time_string(string: str) -> str:
    # 020-07-02T01:23:50.87
    date, time = string.split("T")

    day, month, year = date.split("-")
    hour, minute, seconds = time.split(":")

    minute = f"{minute}PM" if int(minute) > 12 else f"{minute}AM"

    return f"{month}/{day}/{year} {hour}:{minute}"
