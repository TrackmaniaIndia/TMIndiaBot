import discord
from discord.ext import commands
import requests
import logging
import functions.common_functions.common_functions as common_functions
import functions.logging.convert_logging as convert_logging
import functions.ciphers.xor_cipher
import json
import os
import datetime

log_level, discord_log_level, testing_server_id, version = "", "", "", ""

with open("./json_data/config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    testing_server_id = config["testing_server_id"]
    version = config["bot_version"]

# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = convert_logging.get_logging()

def store_trackmania_username(ctx: commands.Context, unencrypted_string: str) -> None:
    log.debug(f'Getting Encrypted String and Encryption Key')
    encrypted_string, encryption_key = functions.ciphers.xor_cipher.encrypt(unencrypted_string)
    log.debug(f'Received Encryption String and Encryption Key')
    
    username = ctx.author.name
    log.debug(f'Encrypting Username')
    username_encrypted, username_key = functions.ciphers.xor_cipher.encrypt(username)

    user_dict = {"Username": username_encrypted, "Username Key": username_key, "TM2020 Username": encrypted_string, "TM2020 Username Key": encryption_key}

    log.debug(f'Loading Username JSON File')
    with open('./json_data/tm2020_usernames.json', 'r') as file:
        log.debug(f'Storing Usernames into a Variable')
        all_usernames = json.load(file)
        log.debug(f'Stored Usernames into a Variable')

    log.debug(f'Adding User Dictionary to Existing File')
    all_usernames['participants'].append(user_dict)
    log.debug(f'Added User Dictionary to Existing File')

    log.debug(f'Opening TM2020 Usernames File and Dumping')
    with open('./json_data/tm2020_usernames.json', 'w') as file:
        json.dump(all_usernames, file, indent=4)
        log.debug(f'Dumped to JSON File')
