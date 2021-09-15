from functions.tm_username_functions.username_functions_old import BASE_API_URL
from discord.ext import commands
import logging
import functions.logging.convert_logging as convert_logging
from functions.ciphers.vigenere_cipher import encrypt, decrypt
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def get_all_usernames() -> tuple[str]:
    """
    Gets all usernames stored in tm2020_usernames.json file
    """
    log.debug(f"Opening File")

    usernames = ()

    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Opened File")
        all_usernames = json.load(file)

        log.debug(f"Loaded JSON Data, Getting Usernames")
        for author_id in all_usernames:
            log.debug(f"Decrypting {author_id}'s username and appending")
            usernames.append(
                decrypt(author_id["TM2020 Username"], author_id["TM2020 Username Key"])
            )

    log.debug(f"Returning list of usernames")
    return usernames


def get_all_discord_ids() -> tuple[str]:
    """
    Gets all the stored discord ids in the tm2020_usernames.json file
    """

    log.debug(f"Opening File")
    discord_ids = ()

    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Opened File")
        all_data = json.load(file)

        for discord_id in all_data:
            log.debug(f"Appending {discord_id}")
            discord_ids.append(discord_id)

    log.debug(f"Returning Ids")
    return discord_ids


def check_username_in_file(username: str) -> bool:
    """
    Checks if given username is in the tm2020_usernames.json file
    """

    all_usernames = get_all_usernames()

    if username in all_usernames:
        log.debug(f"Username in File")
        return True

    log.debug(f"Username not in file")
    return False


def check_discord_id_in_file(discord_id: str) -> bool:
    all_discord_ids = get_all_discord_ids()

    if discord_id in all_discord_ids:
        log.debug(f"Discord Id in file")
        return True

    log.debug(f"Discord id not in file")
    return False
