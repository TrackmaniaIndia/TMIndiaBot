import json
from util.logging import convert_logging
from util.cog_helpers import generic_helper

# Creating a logger
log = convert_logging.get_logging()


def _get_statuses():
    """
    Returns a list of statuses
    """
    statuses = []

    # Getting Bot Version
    log.debug("Getting Bot Version")
    version = generic_helper.get_version()

    # Adding the Basic Version Status
    log.debug("Appending Statuses")
    statuses.append(f"Version: {version}! Online and Ready")
    with open("data/json/statuses.json", encoding="UTF-8") as file:
        statuses = json.load(file)["statuses"]

    log.debug(f"Returning Statuses -> {statuses}")
    return statuses
