import discord
import requests
import util.common_functions as common_functions
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import os
import threading

log = convert_logging.get_logging()
BASE_API_URL = "http://localhost:3000"


def get_player_id(username: str) -> str:
    """Grabs player id for given username from api

    Args:
        username (str): The username of the player

    Returns:
        str: the player id
    """
    log.debug(f"Getting Player ID for {username}")
    player_data = requests.get(f"{BASE_API_URL}/tm2020/player/{username}").json()
    log.debug(f"Received Player Data, Parsing")
    player_id = player_data[0]["player"]["id"]
    log.debug(f"Player ID is {player_id}")
    return player_id
