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


def get_all_usernames() -> list[str]:
    """
    Gets all usernames stored in tm2020_usernames.json file
    """
    log.debug(f"Opening File")

    usernames = []

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


def get_all_discord_ids() -> list[str]:
    """
    Gets all the stored discord ids in the tm2020_usernames.json file
    """

    log.debug(f"Opening File")
    discord_ids = []

    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Opened File")
        all_data = json.load(file)

        for discord_id in all_data:
            log.debug(f"Appending {discord_id}")
            discord_ids.append(str(discord_id))

    log.debug(f"Returning Ids")
    return discord_ids


def check_username_in_file(username: str) -> bool:
    """
    Checks if given username is in the tm2020_usernames.json file
    """
    log.debug(f"Converting Username to String")
    username = str(username)
    log.debug(f"Converted Username to String")

    log.debug(f"Getting all Useranmes")
    all_usernames = get_all_usernames()
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
    all_discord_ids = get_all_discord_ids()
    log.debug(f"Got all Discord IDs")

    if discord_id in all_discord_ids:
        log.debug(f"Discord Id in file")
        return True

    log.debug(f"Discord id not in file")
    return False


def check_valid_trackmania_username(username: str) -> bool:
    """
    This function checks if the username is valid in the api
    """
    log.debug(f"Checking {username}")

    USERNAME_URL = BASE_API_URL + f"/tm2020/player/{username}"

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


def store_trackmania_username(discord_id: str, unencrypted_string: str) -> None:
    log.debug(f"Getting Encrypted String and Encryption Key")
    encrypted_string, encryption_key = encrypt(unencrypted_string)
    log.debug(f"Received Encryption String and Encryption Key")

    username_id = str(discord_id)

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

    log.debug(f"Checking if User Is Already In File")
    if check_discord_id_in_file(discord_id=discord_id):
        log.debug(f"Username is already in all_usernames, popping")
        all_usernames.pop(str(username_id))

    log.debug(f"Adding User Dictionary to Existing File")
    all_usernames[username_id] = user_dict
    log.debug(f"Added User Dictionary to Existing File")

    log.debug(f"Opening TM2020 Usernames File and Dumping")
    with open("./json_data/tm2020_usernames.json", "w") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f"Dumped to JSON File")


def remove_trackmania_username(discord_id: str):
    if not check_discord_id_in_file(discord_id=discord_id):
        log.debug(f"User not in JSON File, Returning")
        return None

    log.debug(f"Loading Username JSON File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug(f"Stored Usernames into a Variable")

    log.debug(f"Popping {discord_id}")
    all_usernames.pop(str(discord_id))
    log.debug(f"Popped {discord_id}")

    log.debug(f"Opening TM2020 Usernames File and Dumping")
    with open("./json_data/tm2020_usernames.json", "w") as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f"Dumped to JSON File")


def get_trackmania_username(discord_id: str) -> str:
    if not check_discord_id_in_file(discord_id):
        log.debug(f"Discord ID not in file, returning none")
        return None

    log.debug(f"Discord Id in Username")
    all_usernames = get_all_usernames()
    all_discord_ids = get_all_discord_ids()

    log.debug(f"Returning Username")
    return all_usernames[all_discord_ids.index(discord_id)]


def get_trackmania_id(discord_id: str) -> str:
    """
    Gets trackmania id with discord_id
    """

    if not check_discord_id_in_file(discord_id):
        log.debug(f"Discord ID not in file, returning none")
        return None

    log.debug(f"Discord ID in File")
    log.debug(f"Opening File")

    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Loading JSON File")
        all_data = json.load(file)
        log.debug(f"Loaded JSON File")

        log.debug(f"Returning ID")
        return all_data[discord_id]["TM2020 ID"]


def get_trackmania_id_with_username(username: str) -> str:
    """
    Gets trackmania2020 id with username given
    """

    log.debug(f"Checking if Username Exists in File")
    if not check_username_in_file(username):
        log.debug(f"Username not in File")
        return None

    log.debug(f"Username Exists in File")
    log.debug(f"Getting All Usernames and Discord Ids")
    all_usernames = get_all_usernames()
    all_ids = get_all_discord_ids()
    log.debug(f"Got All Usernames and Discord Ids")

    log.debug(f"Getting Discord ID")
    discord_id = all_ids[all_usernames.index(username)]
    log.debug(f"Returning Discord Id w/ Other Function")

    return get_trackmania_id(discord_id)
