import json

import aiohttp
from trackmania import Client

from bot.api import APIClient
from bot.log import get_logger

log = get_logger(__name__)


async def get_trophies(
    access_token: str, account_ids: list[str]
) -> list[dict[str, int]]:
    request_headers = {
        "Authorization": f"nadeo_v1 t={access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": Client.USER_AGENT,
    }

    log.debug("Creating payload for trophies.")
    log.critical(account_ids)
    account_list = {"listPlayer": []}

    # Creating a payload with all the account_ids.
    for pid in account_ids:
        account_list["listPlayer"].append({"accountId": pid})

    payload = json.dumps(account_list)
    log.critical(payload)
    log.debug("Created payload: %s", payload)

    log.debug("Creating trophy session.")
    trophy_session = aiohttp.ClientSession(headers=request_headers)
    trophy_session_response = await trophy_session.post(
        url="https://live-services.trackmania.nadeo.live/api/token/leaderboard/trophy/player",
        data=payload,
    )

    log.debug("Closing trophy session")
    await trophy_session.close()

    log.critical(await trophy_session_response.text())

    log.debug("Status Code: %s", trophy_session_response.status)
    trophy_data = await trophy_session_response.json()

    player_trophy_data = {"players": []}

    log.critical(trophy_data)

    for player in trophy_data.get("rankings", []):
        log.debug("Adding player: %s", player.get("accountId", None))
        account_id = player.get("accountId", None)
        trophy_count = player.get("countPoint", 0)

        player_trophy_data["players"].extend(
            [
                {
                    "username": None,
                    "player_id": account_id,
                    "score": trophy_count,
                }
            ]
        )

    for p in player_trophy_data.get("players", []):
        log.critical(p.get("username", None))

    return player_trophy_data
