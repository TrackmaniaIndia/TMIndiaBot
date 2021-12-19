import requests

import util.logging.convert_logging as convert_logging

# Setting up Logging
log = convert_logging.get_logging()


def _get_matchmaking_data(player_id: str):
    log.debug(f"Getting Matchmaking Data from API")
    matchmaking_data = requests.get(
        "http://localhost:3000/tm2020/player/{}/matchmaking".format(player_id)
    ).json()
    log.debug(f"Got Matchmaking Data, Returning")

    return matchmaking_data


def _get_progression_to_next_rank(matchmaking_data) -> float:
    log.debug(f"Getting Progression to Next Round")

    # Checking if Player is Master 3 or Above
    if matchmaking_data["info"]["division"]["position"] >= 12:
        log.debug(f"Player is a Master 3 or Above Player")
        return 0

    current_score = matchmaking_data["info"]["score"]
    minpoints = matchmaking_data["info"]["division"]["minpoints"]
    maxpoints = matchmaking_data["info"]["division"]["maxpoints"] + 1

    numerator = minpoints - current_score
    denomenator = maxpoints - minpoints

    return round(numerator / denomenator, 2)


def _get_rank(matchmaking_data) -> str:
    log.debug(f"Getting Rank")
    rank = matchmaking_data["info"]["rank"]
    log.debug(f"Got Rank, Returning")
    return rank
