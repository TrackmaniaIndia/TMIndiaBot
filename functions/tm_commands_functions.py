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

def get_leaderboards():
    return