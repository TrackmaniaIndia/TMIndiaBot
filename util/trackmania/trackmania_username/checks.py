import os
import sys
import requests
from util.logging import convert_logging
from util.trackmania.trackmania_username.get_stored import get_stored_usernames
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("base_api_url")

log = convert_logging.get_logging()


def check_valid_trackmania_username(username: str) -> bool:
    """
    This function checks if the username is valid in the api
    """
    log.debug(f"Checking {username}")

    if username is None:
        log.debug("Username is None, Returning")
        return False

    if username in get_stored_usernames():
        log.debug("Username is in stored Usernames")
        return True

    username_url = BASE_URL + f"/tm2020/player/{username}"

    log.debug("Requesting from Url")

    try:
        check_player = requests.get(username_url).json()
    except:
        log.error("API is Offline")
        sys.exit()

    log.debug("Checking check_player")
    if check_player == []:
        log.error(f"{username} does not exist")
        return False

    log.debug("User exists, returning")
    return True


def get_trackmania_id_from_api(username: str) -> str:
    log.debug("Checking if Username is Valid")
    if not check_valid_trackmania_username(username):
        log.debug("Not a valid username")
        return None

    player_url = BASE_URL + f"/tm2020/player/{username}"

    log.debug("Getting Player Id")
    player_details = requests.get(player_url).json()
    log.debug("Got Player Details")

    log.debug("Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    log.debug("Returning User ID")
    return user_id
