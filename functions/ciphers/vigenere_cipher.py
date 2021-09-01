import os
import json
import logging
import random
import functions.logging.convert_logging as convert_logging
from functions.other_functions.get_letter_lists import get_lower_case, get_upper_case

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
log = convert_logging.get_logging(log_level, discord_log_level)

log.debug(f'Getting Lower Case Letters')
lower_case_letters = get_lower_case()

log.debug(f'Getting Upper Case Letters')
upper_case_letters = get_upper_case()

letters = lower_case_letters + upper_case_letters

log.debug(f'Randomizing Letter List')
letters = random.shuffle(letters)
log.debug(f'Randomized Letter List')

