from discord import player
import requests
import time
import json
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import discord

log = convert_logging.get_logging()
BASE_LEADERBOARD_URL = "http://localhost:3000/tm2020/leaderboard/"


def _get_all_compaign_ids(ignore_first_five: bool = False, year: str = "2021", season: str = "Fall") -> list[str]:
    """Gets a list of all campaign ids for a given year and season

    Args:
        ignore_first_five (bool, optional): Whether to ignore the first five maps. Defaults to False.
        year (str, optional): The year of the season. Defaults to "2021".
        season (str, optional): The season itself. Defaults to "Fall".

    Returns:
        list[str]: List of ids
    """
    log.debug(f"Getting IDs from File, Ignore -> {ignore_first_five}")
    log.debug(f"Opening {year}/{season.lower()} Data File")
    with open(f"./data/json/campaign/{year}/{season.lower()}.json", "r") as file:
        file_data = json.load(file)
        id_list = file_data["ids"]

    if not ignore_first_five:
        log.debug(f"Not Ignoring First Five Maps")
        return id_list
    else:
        log.debug(f"Ignoring First Five Maps")
        return id_list[5:]


def update_leaderboards_campaign(id_list: list[str], year: str = "2021", season: str = "Fall", skip_first_five: bool = False):
    """Updates the leaderboard files for the campaign

    Args:
        id_list (list[str]): Campaign map id list
        year (str, optional): The year of the season. Defaults to "2021"
        season (str, optional): The season itself. Defaults to "Fall".
    """
    for i, id in enumerate(id_list, start = 5 if skip_first_five else 0):
        leaderboard_data = []

        while len(leaderboard_data) < 500:
            log.debug(f"Requesting for Leaderboard Data of {id}")
            leaderboard_data = requests.get(BASE_LEADERBOARD_URL + str(id)).json()
            log.debug(f"Got Leaderboard Data of {id}")

            log.debug(f"Sleeping for 7s")
            time.sleep(7)

        log.debug(f"Dumping Data to a File")
        with open(f"./data/leaderboard/{year}/{season.lower()}/{i + 1}.json", "w") as file:
            json.dump(leaderboard_data, file, indent=4)

        log.debug(f"Sleeping for 15s")
        time.sleep(15)
        log.info(f"Finished Map #{i + 1}")


def get_player_list(map_no: str, year: str = "2021", season: str = "Fall"):
    log.debug(f"Opening File, Map No -> {map_no}")
    with open(f"./data/leaderboard/{year}/{season.lower()}/{map_no}.json", "r") as file:
        data = json.load(file)

    player_list = []

    log.debug(f"Appending Players")
    for player in data:
        player_list.append((player["player"]["name"], player["position"]))

    return player_list


def get_player_good_maps(player_name: str, year: str = "2021", season: str = "Fall") -> discord.Embed:
    log.debug(f"Getting Player Details for Player Name -> {player_name}")
    player_embed = ezembed.create_embed(
        title=f"{player_name} is good at the following maps",
        color=discord.Colour.random(),
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
        log.debug(f"Player does not have any top 100 ranks")
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
        log.debug(f"Player does not have any top 200 ranks")
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
        log.debug(f"Player does not have any top 300 ranks")
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
        log.debug(f"Player does not have any top 400 ranks")
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
        log.debug(f"Player does not have any top 500 ranks")
        player_embed.add_field(
            name="**Top 500**",
            value="Player does not have any top 500 times for maps 06-25",
            inline=False,
        )

    return player_embed
