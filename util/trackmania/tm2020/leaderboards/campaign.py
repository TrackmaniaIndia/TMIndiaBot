import requests
import time
import json
import util.logging.convert_logging as convert_logging

log = convert_logging.get_logging()
BASE_LEADERBOARD_URL = "http://localhost:3000/tm2020/leaderboard/"


def _get_all_fall_campaign_ids(ignore_first_five: bool = False) -> list[str]:
    """Get's a list of all fall campaign ids

    Args:
        ignore_first_five (bool, optional): Whether or not to ignore the first five maps. Defaults to False.

    Returns:
        list[str]: The list of ids
    """
    log.debug(f"Getting Fall IDs from File, Ignore -> {ignore_first_five}")
    log.debug(f"Opening Fall Data File")
    with open("./data/json/campaign/2021/fall.json", "r") as file:
        file_data = json.load(file)
        id_list = file_data["ids"]

    if not ignore_first_five:
        log.debug(f"Not Ignoring First Five Maps")
        return id_list
    else:
        log.debug(f"Ignoring First Five Maps")
        return id_list[5:]


def update_leaderboards_campaign(id_list: list[str]):
    """Updates the leaderboard files for the campaign

    Args:
        id_list (list[str]): Campaign map id list
    """
    for i, id in enumerate(id_list):
        leaderboard_data = []

        while len(leaderboard_data) < 500:
            log.debug(f"Requesting for Leaderboard Data of {id}")
            leaderboard_data = requests.get(BASE_LEADERBOARD_URL + str(id)).json()
            log.debug(f"Got Leaderboard Data of {id}")

            log.debug(f"Sleeping for 5s")
            time.sleep(7)

        log.debug(f"Dumping Data to a File")
        try:
            with open(f"./data/leaderboard/2021/fall/{i + 1}.json", "w") as file:
                json.dump(leaderboard_data, file, indent=4)
        except:
            with open(
                "./data/leaderboard/2021/fall/0{}.json".format(str(i + 1)), "r"
            ) as file:
                json.dump(leaderboard_data, file, indent=4)

        log.debug(f"Sleeping for 15s")
        time.sleep(15)
        log.info(f"Finished Map #{i + 1}")
