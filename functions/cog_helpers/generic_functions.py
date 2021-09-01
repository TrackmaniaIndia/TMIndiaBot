import os
import json
import logging
import functions.logging.convert_logging as convert_logging


# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def check_for_times_run() -> None:
    log.debug(f"Checking for Times Run File")
    if not os.path.exists("./data"):
        log.critical("Data Directory doesn't Exist, Creating")
        os.mkdir("./data")
    if not os.path.exists("./data/times_run.txt"):
        log.critical("Times Run File doesn't Exist, Creating")
        with open("./data/times_run.txt", "w") as file:
            print(0, file=file)

    return
