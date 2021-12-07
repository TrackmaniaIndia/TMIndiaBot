import json
import util.logging.convert_logging as convert_logging
from dotenv import load_dotenv
import os
from util.trackmania.trackmania_username.checks import (
    check_valid_trackmania_username,
    get_trackmania_id_from_api,
)
from util.trackmania.trackmania_username.get_stored import (
    get_stored_usernames,
    get_stored_discord_ids,
)

load_dotenv()
BASE_URL = os.getenv("BASE_API_URL")

log = convert_logging.get_logging()


def check_username_in_file(username: str) -> bool:
    """
    Checks if given username is in the tm2020_usernames.json file
    """
    log.debug(f"Converting Username to String")
    username = str(username)
    log.debug(f"Converted Username to String")

    log.debug(f"Getting all Useranmes")
    all_usernames = get_stored_usernames()
    log.debug(f"Got all Usernames")

    if username in all_usernames:
        log.debug(f"Username in File")
        return True

    log.debug(f"Username not in file")
    return False


def check_discord_id_in_file(discord_id: str) -> bool:
    """
    Checks if the given discord id is in the file
    """
    log.debug(f"Converting Discord ID to String")
    discord_id = str(discord_id)
    log.debug(f"Converted Discord ID to String")

    log.debug(f"Getting all Discord IDs")
    all_discord_ids = get_stored_discord_ids()
    log.debug(f"Got all Discord IDs")

    if str(discord_id) in all_discord_ids:
        log.debug(f"Discord Id in file")
        return True

    log.debug(f"Discord id not in file")
    return False


def get_trackmania_username(discord_id: str) -> str:
    if not check_discord_id_in_file(discord_id):
        log.debug(f"Discord ID not in file, returning none")
        return None

    log.debug(f"Discord Id in Username")
    all_usernames = get_stored_usernames()
    all_discord_ids = get_stored_discord_ids()

    log.debug(f"Returning Username")
    return all_usernames[all_discord_ids.index(discord_id)]


def get_trackmania_id_from_file(discord_id: str) -> str:
    """
    Gets trackmania id with discord_id
    """

    if not check_discord_id_in_file(discord_id):
        log.debug(f"Discord ID not in file, returning none")
        return None

    log.debug(f"Discord ID in File")
    log.debug(f"Opening File")

    with open("./data/json/tm2020_usernames.json", "r") as file:
        log.debug(f"Loading JSON File")
        all_data = json.load(file)
        log.debug(f"Loaded JSON File")

        log.debug(f"Returning ID")
        return all_data["Usernames"][discord_id]["TM2020 ID"]


def get_trackmania_id_with_username_from_file(username: str) -> str:
    """
    Gets trackmania2020 id with username given
    """

    log.debug(f"Checking if Username Exists in File")
    if not check_username_in_file(username):
        log.debug(f"Username not in File")
        return None

    log.debug(f"Username Exists in File")
    log.debug(f"Getting All Usernames and Discord Ids")
    all_usernames = get_stored_usernames()
    all_ids = get_stored_discord_ids()
    log.debug(f"Got All Usernames and Discord Ids")

    log.debug(f"Getting Discord ID")
    discord_id = all_ids[all_usernames.index(username)]
    log.debug(f"Returning Discord Id w/ Other Function")

    return get_trackmania_id_from_file(discord_id)


def get_id(username: str = None) -> str:
    log.debug(f"Checking {username}")

    if username is None:
        log.debug(f"Username is None, Returning None")
        return None

    if not check_username_in_file(username):
        log.debug(f"{username} not in file")
        log.debug(f"Checking if Username is Valid")

        if not check_valid_trackmania_username(username):
            log.debug("Not a Valid Username, returning None")
            return None

        log.debug(f"Pinging API and Getting Trackmania ID")
        return get_trackmania_id_from_api(username)
    else:
        log.debug(f"{username} is in file")
        return get_trackmania_id_with_username_from_file(username)
