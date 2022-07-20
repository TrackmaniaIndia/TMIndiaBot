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
    account_list = {"listPlayer": []}

    for pid in account_ids:
        account_list["listPlayer"].append({"accountId": pid})

    payload = json.dumps(account_list)
    log.debug("Created payload: %s", payload)

    log.debug("Creating trophy session.")
    trophy_session = aiohttp.ClientSession(headers=request_headers)
    trophy_session_response = await trophy_session.post(
        url="https://live-services.trackmania.nadeo.live/api/token/leaderboard/trophy/player",
        data=payload,
    )

    log.debug("Closing trophy session")
    await trophy_session.close()

    log.debug("Status Code: %s", trophy_session_response.status)
    trophy_data = await trophy_session_response.json()

    player_trophy_data = {"players": []}

    log.debug("Getting usernames")
    account_ids_string = ",".join(account_ids)

    api_client = APIClient()
    usernames = await api_client.get(
        "https://prod.trackmania.core.nadeo.online/accounts/displayNames/?accountIdList="
        + account_ids_string
    )
    await api_client.close()

    for player in trophy_data.get("rankings", []):
        log.debug("Adding player: %s", player.get("accountId", None))
        account_id = player.get("accountId", None)
        trophy_count = player.get("countPoint", 0)

        for p in usernames:
            if p.get("accountId", None) == account_id:
                username = p.get("displayName", None)
                break

        log.debug("Adding Player %s with Score %s", username, trophy_count)

        player_trophy_data["players"].extend(
            [
                {
                    "username": username,
                    "player_id": account_id,
                    "score": trophy_count,
                }
            ]
        )

    return player_trophy_data
