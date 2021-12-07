import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import get_version
import json

# Creating a logger
log = convert_logging.get_logging()


def _get_statuses():
    """
    Returns a list of statuses
    """
    statuses = []

    # Getting Bot Version
    log.debug(f"Getting Bot Version")
    VERSION = get_version()

    # Adding the Basic Version Status
    log.debug(f"Appending Statuses")
    statuses.append(f"Version: {VERSION}! Online and Ready")
    with open("util/cog_helpers/statuses.json") as file:
        statuses = json.load(file)["statuses"]

    log.debug(f"Returning Statuses -> {statuses}")
    return statuses
