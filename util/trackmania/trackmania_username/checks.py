import requests
import os

import util.logging.convert_logging as convert_logging

from util.trackmania.trackmania_username.get_stored import get_stored_usernames
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("BASE_API_URL")

log = convert_logging.get_logging()


def check_valid_trackmania_username(username: str) -> bool:
    """
    This function checks if the username is valid in the api
    """
    log.debug(f"Checking {username}")

    if username is None:
        log.debug(f"Username is None, Returning")
        return False

    if username in get_stored_usernames():
        log.debug(f"Username is in stored Usernames")
        return True

    USERNAME_URL = BASE_URL + f"/tm2020/player/{username}"

    log.debug(f"Requesting from Url")

    try:
        check_player = requests.get(USERNAME_URL).json()
    except:
        log.error(f"API is Offline")
        exit()

    log.debug(f"Checking check_player")
    if check_player == []:
        log.error(f"{username} does not exist")
        return False

    log.debug(f"User exists, returning")
    return True


def get_trackmania_id_from_api(username: str) -> str:
    log.debug(f"Checking if Username is Valid")
    if not check_valid_trackmania_username(username):
        log.debug(f"Not a valid username")
        return None

    PLAYER_URL = BASE_URL + f"/tm2020/player/{username}"

    log.debug(f"Getting Player Id")
    player_details = requests.get(PLAYER_URL).json()
    log.debug(f"Got Player Details")

    log.debug(f"Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    log.debug(f"Returning User ID")
    return user_id
