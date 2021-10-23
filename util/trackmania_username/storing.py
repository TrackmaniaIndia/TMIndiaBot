import json
import requests
import util.logging.convert_logging as cl
from dotenv import load_dotenv
import os
from util.trackmania_username.get_stored import (
    get_stored_usernames,
    get_stored_discord_ids,
)

load_dotenv()
BASE_URL = os.getenv("BASE_API_URL")

log = cl.get_logging()


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


def store_trackmania_username(discord_id: str, username: str) -> None:
    log.debug(f"Storing {username} for {discord_id}")
    username_id = str(discord_id)

    PLAYER_URL = BASE_URL + f"/tm2020/player/{username}"

    log.debug(f"Getting Player Id")
    player_details = requests.get(PLAYER_URL).json()
    log.debug(f"Got Player Details")

    log.debug(f"Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    user_dict = {
        "TM2020 Username": username,
        "TM2020 ID": user_id,
    }

    log.debug(f"Loading Username JSON File")
    with open("./data/json/tm2020_usernames.json", "r") as file:
        log.debug(f"Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug(f"Stored Usernames into a Variable")

    log.debug(f"Checking if User Is Already In File")
    if str(discord_id) in get_stored_discord_ids():
        log.debug(f"Username is already in all_usernames, popping")
        all_usernames["Usernames"].pop(str(username_id))

    log.debug(f"Adding User Dictionary to Existing File")
    all_usernames["Usernames"][username_id] = user_dict
    log.debug(f"Added User Dictionary to Existing File")

    log.debug(f"Opening TM2020 Usernames File and Dumping")
    with open("./data/json/tm2020_usernames.json", "w") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f"Dumped to JSON File")
        log.debug(f"Current Username JSON file = {all_usernames}")


def remove_trackmania_username(discord_id: str):
    if str(discord_id) not in get_stored_discord_ids():
        log.debug(f"User not in JSON File, Returning")
        return None

    log.debug(f"Loading Username JSON File")
    with open("./data/json/tm2020_usernames.json", "r") as file:
        log.debug(f"Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug(f"Stored Usernames into a Variable")

    log.debug(f"Popping {discord_id}")
    all_usernames["Usernames"].pop(str(discord_id))
    log.debug(f"Popped {discord_id}")

    log.debug(f"Opening TM2020 Usernames File and Dumping")
    with open("./data/json/tm2020_usernames.json", "w") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f"Dumped to JSON File")


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
