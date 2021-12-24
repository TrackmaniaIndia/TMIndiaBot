import json
import os

from dotenv import load_dotenv

import util.trackmania.trackmania_username.checks as tm_checks
import util.trackmania.trackmania_username.get_stored as tm_get_stored
from util.logging import convert_logging

load_dotenv()
BASE_URL = os.getenv("base_api_url")

log = convert_logging.get_logging()


def check_username_in_file(username: str) -> bool:
    """
    Checks if given username is in the tm2020_usernames.json file
    """
    log.debug("Converting Username to String")
    username = str(username)
    log.debug("Converted Username to String")

    log.debug("Getting all Useranmes")
    all_usernames = tm_get_stored.get_stored_usernames()
    log.debug("Got all Usernames")

    if username in all_usernames:
        log.debug("Username in File")
        return True

    log.debug("Username not in file")
    return False


def check_discord_id_in_file(discord_id: str) -> bool:
    """
    Checks if the given discord id is in the file
    """
    log.debug("Converting Discord ID to String")
    discord_id = str(discord_id)
    log.debug("Converted Discord ID to String")

    log.debug("Getting all Discord IDs")
    all_discord_ids = tm_get_stored.get_stored_discord_ids()
    log.debug("Got all Discord IDs")

    if str(discord_id) in all_discord_ids:
        log.debug("Discord Id in file")
        return True

    log.debug("Discord id not in file")
    return False


def get_trackmania_username(discord_id: str) -> str:
    if not check_discord_id_in_file(discord_id):
        log.debug("Discord ID not in file, returning none")
        return None

    log.debug("Discord Id in Username")
    all_usernames = tm_get_stored.get_stored_usernames()
    all_discord_ids = tm_get_stored.get_stored_discord_ids()

    log.debug("Returning Username")
    return all_usernames[all_discord_ids.index(discord_id)]


def get_trackmania_id_from_file(discord_id: str) -> str:
    """
    Gets trackmania id with discord_id
    """

    if not check_discord_id_in_file(discord_id):
        log.debug("Discord ID not in file, returning none")
        return None

    log.debug("Discord ID in File")
    log.debug("Opening File")

    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        log.debug("Loading JSON File")
        all_data = json.load(file)
        log.debug("Loaded JSON File")

        log.debug("Returning ID")
        return all_data["Usernames"][discord_id]["TM2020 ID"]


def get_trackmania_id_with_username_from_file(username: str) -> str:
    """
    Gets trackmania2020 id with username given
    """

    log.debug("Checking if Username Exists in File")
    if not check_username_in_file(username):
        log.debug("Username not in File")
        return None

    log.debug("Username Exists in File")
    log.debug("Getting All Usernames and Discord Ids")
    all_usernames = tm_get_stored.get_stored_usernames()
    all_ids = tm_get_stored.get_stored_discord_ids()
    log.debug("Got All Usernames and Discord Ids")

    log.debug("Getting Discord ID")
    discord_id = all_ids[all_usernames.index(username)]
    log.debug("Returning Discord Id w/ Other Function")

    return get_trackmania_id_from_file(discord_id)


def get_id(username: str = None) -> str:
    log.debug(f"Checking {username}")

    if username is None:
        log.debug("Username is None, Returning None")
        return None

    if not check_username_in_file(username):
        log.debug(f"{username} not in file")
        log.debug("Checking if Username is Valid")

        if not tm_checks.check_valid_trackmania_username(username):
            log.debug("Not a Valid Username, returning None")
            return None

        log.debug("Pinging API and Getting Trackmania ID")
        return tm_checks.get_trackmania_id_from_api(username)

    log.debug(f"{username} is in file")
    return get_trackmania_id_with_username_from_file(username)
