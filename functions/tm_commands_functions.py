import discord
import requests
import logging
import functions.common_functions as cf
import functions.convert_logging as cl
import json
import os

log_level, discord_log_level, testing_server_id, version = "", "", "", ""

with open("./config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    testing_server_id = config["testing_server_id"]
    version = config["bot_version"]

# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

def get_tmnf_map(tmx_id: str) -> discord.Embed:
    if not tmx_id.isnumeric():
        log.error(f"TMX ID is not Numeric")

        return discord.Embed(
            title=":warning: TMX ID must be a number",
            description="Example: 2233",
            color=0xFF0000,
        )

    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tmnf-x/trackinfo/{tmx_id}"

    log.debug(f"Requesting Response from API")
    response = requests.get(LEADERBOARD_URL)
    log.debug(f"Received Response From Api")

    log.debug(f"Checking API Response")
    if int(response.status_code) == 400:
        if response.json["error"] == "INVALID_TMX_ID":
            log.error("Invalid TMX ID given")
            return discord.Embed(
                title=":warning: Invalid TMX Id",
                description="The TMX ID provided is invalid",
                color=0xFF0000,
            )
    log.debug(f"API Response Checked")

    api_data = response.json()

    log.debug(f'Creating Embed')
    embed = discord.Embed(
        title=api_data["name"],
        description=api_data["authorComments"],
        color=cf.get_random_color(),
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
    log.debug(f'Embed Created, Returning')

    return embed

def get_leaderboards(tmx_id: str) -> discord.Embed:
    if not tmx_id.isnumeric():
        log.error(f'TMX ID Given is Not Numeric')
        return discord.Embed(title=':warning: TMX ID Must be a number', description='Example: 8496396', color=0xff0000)

    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tmnf-x/leaderboard/{tmx_id}"
    response = requests.get(LEADERBOARD_URL)
    leaderboards = response.json()

    if int(response.status_code) == 400:
        if response.json()["error"] == "INVALID_TMX_ID":
            log.error("Invalid TMX ID Given")
            return discord.Embed(title=":warning: Invalid TMX ID", description="The TMX ID provided is invalid", color=0xff0000)

    log.debug(f'Requesting Map Name')
    map_name = requests.get(f"{BASE_API_URL}/tmnf-x/trackinfo/{tmx_id}").json()['name']
    
    log.debug(f'Creating Times String')
    times = [
            "**:first_place: {} by {}**".format(
                leaderboards[0]["time"], leaderboards[0]["username"]
            ),
            ":second_place: {} by {}".format(
                leaderboards[1]["time"], leaderboards[1]["username"]
            ),
            ":third_place: {} by {}".format(
                leaderboards[2]["time"], leaderboards[2]["username"]
            ),
            "4) {} by {}".format(leaderboards[3]["time"], leaderboards[3]["username"]),
            "5) {} by {}".format(leaderboards[4]["time"], leaderboards[4]["username"]),
            "6) {} by {}".format(leaderboards[5]["time"], leaderboards[5]["username"]),
            "7) {} by {}".format(leaderboards[6]["time"], leaderboards[6]["username"]),
            "8) {} by {}".format(leaderboards[7]["time"], leaderboards[7]["username"]),
            "9) {} by {}".format(leaderboards[8]["time"], leaderboards[8]["username"]),
            "10) {} by {}".format(leaderboards[9]["time"], leaderboards[9]["username"]),
        ]
    log.debug(f'Created Times String')
    
    log.debug(f'Creating Description String')
    desc_str = "{}\n[View all replays](https://tmnforever.tm-exchange.com/trackreplayshow/{})".format(
            "\n".join(times), tmx_id
        )
    log.debug(f'Created Description String')

    log.debug(f'Creating Embed')
    embed = discord.Embed(
            title="Leaderboard | " + map_name,
            url="https://tmnforever.tm-exchange.com/trackshow/" + tmx_id,
            description=desc_str,
            color=cf.get_random_color(),
        )
    log.debug(f'Created Embed')

    return embed