import discord
import requests
import logging
import functions.common_functions.common_functions as common_functions
import functions.logging.convert_logging as convert_logging
import os
import datetime

# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def get_tmnf_map(tmx_id: str) -> discord.Embed:
    if not tmx_id.isnumeric():
        log.error(f"TMX ID is not Numeric")

        return discord.Embed(
            title=":warning: TMX ID must be a number",
            description="Example: 2233",
            color=discord.Colour.red(),
        )

    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tmnf-x/trackinfo/{tmx_id}"

    log.debug(f"Requesting Response from API")
    response = requests.get(LEADERBOARD_URL)
    log.debug(f"Received Response From Api")

    log.debug(f"Checking API Response")
    if int(response.status_code) == 400:
        if response.json()["error"] == "INVALID_TMX_ID":
            log.error("Invalid TMX ID given")
            return discord.Embed(
                title=":warning: Invalid TMX Id",
                description="The TMX ID provided is invalid",
                color=discord.Colour.red(),
            )
    log.debug(f"API Response Checked")

    api_data = response.json()

    log.debug(f"Creating Embed")
    embed = discord.Embed(
        title=api_data["name"],
        description=api_data["authorComments"],
        color=common_functions.get_random_color(),
        url="https://tmnforever.tm-exchange.com/trackshow/" + tmx_id,
    )

    embed.set_thumbnail(
        url=f"https://tmnforever.tm-exchange.com/getclean.aspx?action=trackscreenscreens&id={tmx_id}&screentype=0"
    )

    embed.add_field(name="Author", value=api_data["author"], inline=True)
    embed.add_field(name="Version", value=api_data["version"], inline=True)
    embed.add_field(name="Released", value=api_data["releaseDate"], inline=True)
    embed.add_field(name="LB Rating", value=api_data["LBRating"], inline=True)
    embed.add_field(name="Game version", value=api_data["gameVersion"], inline=True)
    embed.add_field(name="Map type", value=api_data["type"], inline=True)
    embed.add_field(name="Map style", value=api_data["style"], inline=True)
    embed.add_field(name="Environment", value=api_data["environment"], inline=True)
    embed.add_field(name="Routes", value=api_data["routes"], inline=True)
    embed.add_field(name="Length", value=api_data["length"], inline=True)
    embed.add_field(name="Difficulty", value=api_data["difficulty"], inline=True)
    embed.add_field(name="Mood", value=api_data["mood"], inline=True)
    log.debug(f"Embed Created, Returning")

    return embed


def get_leaderboards(tmx_id: str, authUrl) -> list[discord.Embed]:
    if not tmx_id.isnumeric():
        log.error(f"TMX ID Given is Not Numeric")
        return discord.Embed(
            title=":warning: TMX ID Must be a number",
            description="Example: 8496396",
            color=discord.Colour.red(),
        )

    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tmnf-x/leaderboard/{tmx_id}"
    response = requests.get(LEADERBOARD_URL)
    leaderboards = response.json()

    if int(response.status_code) == 400:
        if response.json()["error"] == "INVALID_TMX_ID":
            log.error("Invalid TMX ID Given")
            return discord.Embed(
                title=":warning: Invalid TMX ID",
                description="The TMX ID provided is invalid",
                color=discord.Colour.red(),
            )

    log.debug(f"Requesting Map Name")
    map_name = requests.get(f"{BASE_API_URL}/tmnf-x/trackinfo/{tmx_id}").json()["name"]

    log.debug(f"Creating Times String")
    times_page_1 = times_page_2 = times_page_3 = times_page_4 = times_page_5 = ""

    for i in range(0, 10):
        times_page_1 += "{}. {} - {}\n".format(
            i + 1, leaderboards[i]["username"], leaderboards[i]["time"]
        )
        times_page_2 += "{}. {} - {}\n".format(
            i + 11, leaderboards[i + 10]["username"], leaderboards[i + 10]["time"]
        )
        times_page_3 += "{}. {} - {}\n".format(
            i + 21, leaderboards[i + 20]["username"], leaderboards[i + 20]["time"]
        )
        times_page_4 += "{}. {} - {}\n".format(
            i + 31, leaderboards[i + 30]["username"], leaderboards[i + 30]["time"]
        )
        times_page_5 += "{}. {} - {}\n".format(
            i + 41, leaderboards[i + 40]["username"], leaderboards[i + 40]["time"]
        )

    times = [times_page_1, times_page_2, times_page_3, times_page_4, times_page_5]
    embed_pages = []
    log.debug(f"Created Strings")
    log.debug(f"Creating Embeds")
    for i in range(0, 5):
        embed_pages.append(
            discord.Embed(
                title="Map: {} - Page {}".format(map_name, i + 1),
                description=times[i],
                color=common_functions.get_random_color(),
            ).set_footer(
                text=datetime.datetime.utcnow(), icon_url=authUrl  #
            )
        )

    log.debug(f"Created Embeds")
    return embed_pages


def getTm2020Map(tmx_id: str) -> discord.Embed:
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
        "author": formatTimeInt(api_data["authorScore"]),
        "gold": formatTimeInt(api_data["goldScore"]),
        "silver": formatTimeInt(api_data["silverScore"]),
        "bronze": formatTimeInt(api_data["bronzeScore"]),
    }

    tag = ""
    
    try:
        if author['tag']:
            tag = f'[{author["tag"]}] '
        else: 
            tag = ''
    except KeyError as e:
        pass

    medals = getMapMedals(times)
    uploadedAt = parseTmioTimeString(exchange['UploadedAt'])
    updatedAt = parseTmioTimeString(exchange['UpdatedAt'])

    embed=discord.Embed(title=api_data["name"], description=exchange["Comments"] if exchange["Comments"] else "No Comments")
    embed.set_author(name=tag + author["name"], url=f"https://trackmania.io/#/player/{author['id']}" + str(exchange["UserID"]))
    embed.add_field(name="Medals", value=medals, inline=False)
    embed.add_field(name="Mood", value=exchange["Mood"], inline=True)
    embed.add_field(name="Type", value=exchange["MapType"], inline=True)
    embed.add_field(name="Style", value=exchange["StyleName"], inline=True)
    embed.add_field(name="Length", value=exchange["LengthName"], inline=True)
    embed.add_field(name="Laps", value=exchange["Laps"], inline=True)
    embed.add_field(name="Difficulty", value=exchange["DifficultyName"], inline=True)
    embed.add_field(name="Uploaded at ", value=uploadedAt, inline=True)
    embed.add_field(name="Updated at ", value=updatedAt, inline=True)
    embed.add_field(name="Links", value=f"[Download]({api_data['fileUrl']}) | [TMX](https://trackmania.exchange/maps/{exchange['TrackID']}/) | [Trackmania.io](https://trackmania.io/#/leaderboard/{tmx_id})", inline=False)

    embed.set_image(url=api_data['thumbnailUrl'])

    log.debug(f"Embed Created, Returning")
    return embed

def getMapMedals(times: dict) -> str:
    return f"""
    <:author:894268580902883379> {times['author']}
    <:gold:894268580970004510> {times['gold']}
    <:silver:894268580655411220> {times['silver']}
    <:bronze:894268580181458975> {times['bronze']}
    """

def formatTimeInt(time: int) -> str:
    time = str(time)

    return f"0:{time[:2]}.{time[2:]}"    

def parseTmioTimeString(string: str) -> str:
    # 020-07-02T01:23:50.87
    date, time = string.split('T')
    
    day, month, year = date.split('-')
    hour, minute, seconds = time.split(':')

    minute = f"{minute}PM" if int(minute) > 12 else f"{minute}AM"

    return f"{month}/{day}/{year} {hour}:{minute}"