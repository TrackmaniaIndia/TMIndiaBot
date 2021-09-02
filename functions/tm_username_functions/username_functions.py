from discord.ext import commands
import logging
import functions.logging.convert_logging as convert_logging
from functions.ciphers.vigenere_cipher import encrypt, decrypt
import json

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def check_trackmania_username(ctx: commands.Context) -> bool:
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

    user_dict = {
        "TM2020 Username": encrypted_string,
        "TM2020 Username Key": encryption_key,
    }

    log.debug(f"Loading Username JSON File")
    with open("./json_data/tm2020_usernames.json", "r") as file:
        log.debug(f"Storing Usernames into a Variable")
        all_usernames = json.load(file)
        log.debug(f"Stored Usernames into a Variable")

    dont_append = False

    log.debug(f"Checking if User Is Already In File")
    if check_trackmania_username(ctx):
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
    if not check_trackmania_username(ctx):
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
