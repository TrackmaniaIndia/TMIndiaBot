import json
import os
import sys
import requests
from util.logging import convert_logging
from dotenv import load_dotenv
import util.trackmania.trackmania_username.get_stored as tm_get_stored

load_dotenv()
base_url = os.getenv("base_api_url")

log = convert_logging.get_logging()


def check_valid_trackmania_username(username: str) -> bool:
    """
    This function checks if the username is valid in the api
    """
    log.debug(f"Checking {username}")

    if username is None:
        log.debug("Username is None, Returning")
        return False

    if username in tm_get_stored.get_stored_usernames():
        log.debug("Username is in stored Usernames")
        return True

    username_url = base_url + f"/tm2020/player/{username}"

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


def store_trackmania_username(discord_id: str, username: str) -> None:
    log.debug(f"Storing {username} for {discord_id}")
    username_id = str(discord_id)

    player_url = base_url + f"/tm2020/player/{username}"

    log.debug("Getting Player Id")
    player_details = requests.get(player_url).json()
    log.debug("Got Player Details")

    log.debug("Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    user_dict = {
        "TM2020 Username": username,
        "TM2020 ID": user_id,
    }

    log.debug("Loading Username JSON File")
    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        log.debug("Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug("Stored Usernames into a Variable")

    log.debug("Checking if User Is Already In File")
    if str(discord_id) in tm_get_stored.get_stored_discord_ids():
        log.debug("Username is already in all_usernames, popping")
        all_usernames["Usernames"].pop(str(username_id))

    log.debug("Adding User Dictionary to Existing File")
    all_usernames["Usernames"][username_id] = user_dict
    log.debug("Added User Dictionary to Existing File")

    log.debug("Opening TM2020 Usernames File and Dumping")
    with open("./data/json/tm2020_usernames.json", "w", encoding="UTF-8") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug("Dumped to JSON File")
        log.debug(f"Current Username JSON file = {all_usernames}")


def remove_trackmania_username(discord_id: str):
    if str(discord_id) not in tm_get_stored.get_stored_discord_ids():
        log.debug("User not in JSON File, Returning")
        return

    log.debug("Loading Username JSON File")
    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        log.debug("Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug("Stored Usernames into a Variable")

    log.debug(f"Popping {discord_id}")
    all_usernames["Usernames"].pop(str(discord_id))
    log.debug(f"Popped {discord_id}")

    log.debug("Opening TM2020 Usernames File and Dumping")
    with open("./data/json/tm2020_usernames.json", "w", encoding="UTF-8") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug("Dumped to JSON File")


def get_trackmania_id_from_api(username: str) -> str:
    log.debug("Checking if Username is Valid")
    if not check_valid_trackmania_username(username):
        log.debug("Not a valid username")
        return None

    player_url = base_url + f"/tm2020/player/{username}"

    log.debug("Getting Player Id")
    player_details = requests.get(player_url).json()
    log.debug("Got Player Details")

    log.debug("Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    log.debug("Returning User ID")
    return user_id
