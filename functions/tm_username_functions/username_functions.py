from discord.ext import commands
import logging
import discord
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


def check_trackmania_username_in_file(ctx: commands.Context) -> bool:
    log.debug(f"Opening File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Checking for Discord ID")
        if str(ctx.author.id) in json.load(file):
            log.debug(f"Username is in JSON File")
            return True
        else:
            log.debug(f"Username is not in JSON File")
            return False


def store_trackmania_username(ctx: commands.Context, unencrypted_string: str) -> None:
    log.debug(f"Getting Encrypted String and Encryption Key")
    encrypted_string, encryption_key = encrypt(unencrypted_string)
    log.debug(f"Received Encryption String and Encryption Key")

    username_id = ctx.author.id

    PLAYER_URL = BASE_API_URL + f"/tm2020/player/{unencrypted_string}"

    log.debug(f"Getting Player Id")
    player_details = requests.get(PLAYER_URL).json()
    log.debug(f"Got Player Details")

    log.debug(f"Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    user_dict = {
        "TM2020 Username": encrypted_string,
        "TM2020 Username Key": encryption_key,
        "TM2020 ID": user_id,
    }

    log.debug(f"Loading Username JSON File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug(f"Stored Usernames into a Variable")

    dont_append = False

    log.debug(f"Checking if User Is Already In File")
    if check_trackmania_username_in_file(ctx):
        log.debug(f"Username is already in all_usernames, popping")
        all_usernames.pop(str(username_id))

    log.debug(f"Adding User Dictionary to Existing File")
    all_usernames[username_id] = user_dict
    log.debug(f"Added User Dictionary to Existing File")

    log.debug(f"Opening TM2020 Usernames File and Dumping")
    with open("./json_data/tm2020_usernames.json", "w") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f"Dumped to JSON File")


def remove_trackmania_username(ctx: commands.Context):
    if not check_trackmania_username_in_file(ctx):
        log.debug(f"User not in JSON File, Returning")
        return None

    log.debug(f"Loading Username JSON File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug(f"Stored Usernames into a Variable")

    all_usernames.pop(str(ctx.author.id))

    log.debug(f"Opening TM2020 Usernames File and Dumping")
    with open("./json_data/tm2020_usernames.json", "w") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f"Dumped to JSON File")


def check_username(username: str) -> bool:
    """
    This function checks if the username is valid in the api
    """
    log.debug(f"Checking {username}")

    USERNAME_URL = BASE_API_URL + f"/tm2020/player/{username}"

    log.debug(f"Requesting from Url")
    check_player = requests.get(USERNAME_URL).json()

    log.debug(f"Checking check_player")
    if check_player == []:
        log.error(f"{username} does not exist")
        return False

    log.debug(f"User exists, returning")
    return True


def get_username(ctx: commands.Command) -> str:
    log.debug(f"Getting Trackmania Username for {ctx.author.name}")

    log.debug(f"Checking if Username Exists in File")
    if not check_trackmania_username_in_file(ctx):
        log.error(f"User does not exist in file")
        return None

    log.debug(f"User exists in file")
    log.debug(f"Opening File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Returning Username")
        return decrypt(
            file[str(ctx.author.id)]["TM2020 Username"],
            file[str(ctx.author.id)]["TM2020 Username Key"],
        )


def get_trackmania_id(ctx: commands.Command) -> str:
    log.debug(f"Getting Trackmania ID for {ctx.author.name}")

    log.debug(f"Checking if Username Exists in File")
    if not check_trackmania_username_in_file(ctx):
        log.error(f"User does not exist in file")
        return None

    log.debug(f"User exists in file")
    log.debug(f"Opening File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Parsing JSON File")
        ids = json.load(file)
        log.debug(f"Returning ID")
        return str(ids[str(ctx.author.id)]["TM2020 ID"])


def get_trackmania_id_from_api(ctx: commands.Context, username: str) -> str:
    log.debug(f"Getting Trackmania ID for {ctx.author.name} from api")

    log.debug(f"Checking if User is in the file")
    if check_trackmania_username_in_file(ctx):
        log.error(f"User exists in the file")
        return None

    log.debug(f"User does not exist in the file, pinging API")
    USERNAME_URL = BASE_API_URL + f"/tm2020/player/{username}"

    log.debug(f"Requesting from Url")
    player_details = requests.get(USERNAME_URL).json()

    log.debug(f"Parsing Data for ID")
    user_id = player_details[0]["player"]["id"]

    log.debug(f"Returning User Id")
    return user_id
