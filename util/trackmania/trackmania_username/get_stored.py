import json
import os
from util.logging import convert_logging
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("base_api_url")

log = convert_logging.get_logging()


def get_stored_usernames() -> list[str]:
    """Get's all usernames stored in tm2020_usernames.json file

    Returns:
        list[str]: list of Usernames
    """
    usernames = []

    log.debug("Opening file")
    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        log.debug("Opened File")
        log.debug("Loading Json")
        all_usernames = json.load(file)

        log.debug("Appending Usernames to List")
        for author_id in all_usernames["Usernames"]:
            log.debug(f"Appending {author_id}'s Username")
            usernames.append(all_usernames["Usernames"][author_id]["TM2020 Username"])

    log.debug("All Usernames Appended")
    log.debug(f"Username List is -> {usernames}")
    return usernames


def get_stored_discord_ids() -> list[str]:
    """Gets stored discord ids in the tm2020_usernames.json file

    Returns:
        list[str]: List of discord ids
    """
    discord_ids = []

    log.debug("Opening File")
    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        log.debug("Opened File")
        all_data = json.load(file)
        log.debug("Loaded JSON, Appending IDs")
        for discord_id in all_data["Usernames"]:
            discord_ids.append(str(discord_id))

    log.debug("All IDS Appended")
    log.debug(f"List of IDs -> {discord_ids}")
    return discord_ids
