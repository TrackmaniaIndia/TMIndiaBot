import discord
import requests
import os

import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import util.common_functions as common_functions

log = convert_logging.get_logging()


def get_leaderboards(tmx_id: str, authUrl) -> list[discord.Embed]:
    if not tmx_id.isnumeric():
        log.error(f"TMX ID Given is Not Numeric")
        return ezembed.create_embed(
            title=":warning: TMX ID Must be a number",
            description="Example: 8496396",
            color=0xFF0000,
        )

    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tmnf-x/leaderboard/{tmx_id}"
    response = requests.get(LEADERBOARD_URL)
    leaderboards = response.json()

    if int(response.status_code) == 400:
        if response.json()["error"] == "INVALID_TMX_ID":
            log.error("Invalid TMX ID Given")
            return ezembed.create_embed(
                title=":warning: Invalid TMX ID",
                description="The TMX ID provided is invalid",
                color=0xFF0000,
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
            ezembed.create_embed(
                title="Map: {} - Page {}".format(map_name, i + 1),
                description=times[i],
                color=common_functions.get_random_color(),
            )
        )

    log.debug(f"Created Embeds")
    return embed_pages
