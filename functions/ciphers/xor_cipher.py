import os
import json
import logging
import random
import functions.logging.convert_logging as cl

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
log = cl.get_logging(log_level, discord_log_level)

lower_case_letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
upper_case_letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
letters = lower_case_letters + upper_case_letters

def encrypt(input_string: str) -> tuple[str]:
    log.info(f'Encrypting {input_string}')
    log.debug(f'Receiving Random Number')
    xor_key = random.randint(1, 52) - 1 # 52 Characters, -1 for indicing
    log.debug(f'Received Random Number - Number: {xor_key}')
    xor_key_char = letters[xor_key]
    log.debug(f'Received xor_key_char - {xor_key_char}')

    log.debug(f'Encrypting Begins')

    length = len(input_string)

    for i in range(length):
        input_string = (input_string[:i] +
             chr(ord(input_string[i]) ^ ord(xor_key_char)) +
                     input_string[i + 1:]); 

    log.info(f'Encrypting Finished - Encrypted String: {input_string}')
    return (input_string, xor_key_char)

def decrypt(input_string: str, xor_key_char: str) -> str:
    log.info(f'Decrypting {input_string} using key {xor_key_char}')

    log.debug(f'Decrypting Begins')

    length = len(input_string)

    for i in range(length):
        input_string = (input_string[:i] +
             chr(ord(input_string[i]) ^ ord(xor_key_char)) +
                     input_string[i + 1:]); 

    log.info(f'Decrypting Finished - Encrypted String: {input_string}')