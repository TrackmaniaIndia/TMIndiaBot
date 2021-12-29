import json
import time

import discord
import requests

import util.discord.easy_embed as ezembed
from util import common_functions
from util.logging import convert_logging

log = convert_logging.get_logging()
BASE_LEADERBOARD_URL = "http://localhost:3000/tm2020/leaderboard/"


def get_all_campaign_ids(year: str = "2021", season: str = "Fall") -> list[str]:
    """Gets a list of all campaign ids for a given year and season

    Args:
        ignore_first_five (bool, optional): Whether to ignore the first five maps. Defaults to False.
        year (str, optional): The year of the season. Defaults to "2021".
        season (str, optional): The season itself. Defaults to "Fall".

    Returns:
        list[str]: List of ids
    """
    log.debug(f"Opening {year}/{season.lower()} Data File")
    with open(
        f"./data/json/campaign/{year}/{season.lower()}.json", "r", encoding="UTF-8"
    ) as file:
        file_data = json.load(file)
        id_list = file_data["ids"]

    log.debug("Not Ignoring First Five Maps")
    return id_list


def update_leaderboards_campaign(
    id_list: list[str],
    year: str = "2021",
    season: str = "Fall",
    skip_first_five: bool = False,
):
    """Updates the leaderboard files for the campaign

    Args:
        id_list (list[str]): Campaign map id list
        year (str, optional): The year of the season. Defaults to "2021"
        season (str, optional): The season itself. Defaults to "Fall".
    """
    for i, id in enumerate(id_list):
        # if skip_first_five and i < 5:
        #     log.debug(f"Skipping i={i}")
        #     continue
        leaderboard_data = []

        leaderboard_data = requests.get(
            f"http://localhost:3000/tm2020/leaderboard/{id}/5"
        ).json()
        log.debug("Dumping Data to a File")
        with open(
            f"./data/leaderboard/{year}/{season.lower()}/{i + 1}.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(leaderboard_data, file, indent=4)

        log.debug("Sleeping for 15s")
        time.sleep(10)
        log.info(f"Finished Map #{i + 1}")


def get_player_list(map_no: str, year: str = "2021", season: str = "Fall"):
    log.debug(f"Opening File, Map No -> {map_no}")
    with open(
        f"./data/leaderboard/{year}/{season.lower()}/{map_no}.json",
        "r",
        encoding="UTF-8",
    ) as file:
        data = json.load(file)

    player_list = []

    log.debug("Appending Players")
    for player in data:
        player_list.append((player["player"]["name"], player["position"]))

    return player_list


def get_player_good_maps(
    player_name: str, year: str = "2021", season: str = "Fall"
) -> discord.Embed:
    log.debug(f"Getting Player Details for Player Name -> {player_name}")
    player_embed = ezembed.create_embed(
        title=f"{player_name} is good at the following maps",
        color=common_functions.get_random_color(),
    )
    top_100_string = ""
    top_200_string = ""
    top_300_string = ""
    top_400_string = ""
    top_500_string = ""

    for i in range(6, 26, 1):
        player_list = get_player_list(str(i), year, season.lower())

        for player_tuple in player_list:
            if player_tuple[0].lower() == player_name.lower():
                if int(player_tuple[1]) <= 100:
                    log.debug(f"{player_name} is a top 100 player for Map {i}")
                    top_100_string = (
                        top_100_string + str(i) + " - " + str(player_tuple[1]) + "\n"
                    )
                elif int(player_tuple[1]) <= 200 and int(player_tuple[1]) > 100:
                    log.debug(f"{player_name} is a top 200 player for Map {i}")
                    top_200_string = (
                        top_200_string + str(i) + " - " + str(player_tuple[1]) + "\n"
                    )
                elif int(player_tuple[1]) <= 300 and int(player_tuple[1]) > 200:
                    log.debug(f"{player_name} is a top 300 player for Map {i}")
                    top_300_string = (
                        top_300_string + str(i) + " - " + str(player_tuple[1]) + "\n"
                    )
                elif int(player_tuple[1]) <= 400 and int(player_tuple[1]) > 300:
                    log.debug(f"{player_name} is a top 400 player for Map {i}")
                    top_400_string = (
                        top_400_string + str(i) + " - " + str(player_tuple[1]) + "\n"
                    )
                elif int(player_tuple[1]) <= 500 and int(player_tuple[1]) > 400:
                    log.debug(f"{player_name} is a top 500 player for Map {i}")
                    top_500_string = (
                        top_500_string + str(i) + " - " + str(player_tuple[1]) + "\n"
                    )

    if top_100_string != "":
        log.debug(f"Appending Top 100 String for {player_name}")
        player_embed.add_field(
            name="**Top 100**", value="```" + top_100_string + "```", inline=False
        )
    else:
        log.debug("Player does not have any top 100 ranks")
        player_embed.add_field(
            name="**Top 100**",
            value="Player does not have any top 100 times for maps 06-25",
            inline=False,
        )

    if top_200_string != "":
        log.debug(f"Appending Top 100 String for {player_name}")
        player_embed.add_field(
            name="**Top 200**", value="```" + top_200_string + "```", inline=False
        )
    else:
        log.debug("Player does not have any top 200 ranks")
        player_embed.add_field(
            name="**Top 200**",
            value="Player does not have any top 200 times for maps 06-25",
            inline=False,
        )

    if top_300_string != "":
        log.debug(f"Appending Top 100 String for {player_name}")
        player_embed.add_field(
            name="**Top 300**", value="```" + top_300_string + "```", inline=False
        )
    else:
        log.debug("Player does not have any top 300 ranks")
        player_embed.add_field(
            name="**Top 300**",
            value="Player does not have any top 300 times for maps 06-25",
            inline=False,
        )

    if top_400_string != "":
        log.debug(f"Appending Top 100 String for {player_name}")
        player_embed.add_field(
            name="**Top 400**", value="```" + top_400_string + "```", inline=False
        )
    else:
        log.debug("Player does not have any top 400 ranks")
        player_embed.add_field(
            name="**Top 400**",
            value="Player does not have any top 400 times for maps 06-25",
            inline=False,
        )

    if top_500_string != "":
        log.debug(f"Appending Top 100 String for {player_name}")
        player_embed.add_field(
            name="**Top 500**", value="```" + top_500_string + "```", inline=False
        )
    else:
        log.debug("Player does not have any top 500 ranks")
        player_embed.add_field(
            name="**Top 500**",
            value="Player does not have any top 500 times for maps 06-25",
            inline=False,
        )

    return player_embed
