import logging
import json
import requests
from dotenv import load_dotenv
import os

import functions.logging.convert_logging as convert_logging

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def ping_api() -> None:
    log.debug(f"Loading Dotenv")
    load_dotenv()
    BASE_API_URL = os.getenv("BASE_API_URL")

    log.debug(f"Requesting from API")
    try:
        my_request = requests.get(BASE_API_URL)
    except:
        log.error("API is OFFLINE")
        raise Exception("API is OFFLINE")
    log.debug(f"Successfully Received Data from API")
