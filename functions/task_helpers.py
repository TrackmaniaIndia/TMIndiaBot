import logging
import json
import requests
from dotenv import load_dotenv
import os

import functions.convert_logging as cl

log_level, discord_log_level = "", ""

with open("./json_data/config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)


def ping_api() -> None:
    log.debug(f"Loading Dotenv")
    load_dotenv()
    BASE_API_URL = os.getenv("BASE_API_URL")

    log.debug(f"Requesting from API")
    try:
        my_request = requests.get(BASE_API_URL)
    except:
        log.error('API is OFFLINE')
        raise Exception('API is OFFLINE')
    log.debug(f"Successfully Received Data from API")
