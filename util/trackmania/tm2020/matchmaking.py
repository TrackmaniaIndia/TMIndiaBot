from country_converter.country_converter import convert, match
import discord
from discord import player
import requests
import util.common_functions as common_functions
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
from util.trackmania.tm2020.cotd import (
    _get_avg_global_rank,
    _get_avg_div,
    _get_num_completed_cotds,
    _get_num_all_cotds,
)
import os
import threading
import json
import country_converter as coco
import flag


# Setting up Logging
log = convert_logging.get_logging()


def _get_matchmaking_data(player_id: str):
    log.debug(f"Getting Matchmaking Data from API")
    matchmaking_data = requests.get(
        "http://localhost:3000/tm2020/player/{}/matchmaking".format(player_id)
    ).json()
    log.debug(f"Got Matchmaking Data, Returning")

    return matchmaking_data


def _get_progression_to_next_rank(matchmaking_data) -> float:
    log.debug(f"Getting Progression to Next Round")

    # Checking if Player is Master 3 or Above
    if matchmaking_data["info"]["division"]["position"] >= 12:
        log.debug(f"Player is a Master 3 or Above Player")
        return 0

    current_score = matchmaking_data["info"]["score"]
    minpoints = matchmaking_data["info"]["division"]["minpoints"]
    maxpoints = matchmaking_data["info"]["division"]["maxpoints"] + 1

    numerator = minpoints - current_score
    denomenator = maxpoints - minpoints

    return round(numerator / denomenator, 2)


def _get_rank(matchmaking_data) -> str:
    log.debug(f"Getting Rank")
    rank = matchmaking_data["info"]["rank"]
    log.debug(f"Got Rank, Returning")
    return rank
