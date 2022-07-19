# https://gist.github.com/codecat/4dfd3719e1f8d9e5ef439d639abe0de4

import asyncio
import json
import sys

import aiohttp
import discord.ext.tasks as tasks
from trackmania import Client

from bot import constants
from bot.log import get_logger

log = get_logger(__name__)


async def authenticate() -> list[str]:
    log.info("Authenticating with Nadeo Servers...")

    authentication_headers = {
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
        "User-Agent": Client.USER_AGENT,
        "audience": "NadeoLiveServices",
    }
    auth = aiohttp.BasicAuth(
        constants.Consts.tm_dedi_server_login, constants.Consts.tm_dedi_server_password
    )

    log.debug("Sending authentication request to Nadeo Servers...")
    authentication_session = aiohttp.ClientSession(
        auth=auth, headers=authentication_headers
    )
    authentication_response = await authentication_session.post(
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic"
    )

    log.debug("Closing authentication session")
    await authentication_session.close()

    log.debug("Parsing authentication data")
    authentication_json = await authentication_response.json()

    access_token = authentication_json.get("accessToken", None)
    refresh_token = authentication_json.get("refreshToken", None)

    log.debug("Writing Tokens")
    _write_token_file(access_token, refresh_token)

    log.info(
        "Received access token: %s and refresh token: %s", access_token, refresh_token
    )
    return [access_token, refresh_token]


async def _refresh_token(refresh_token: str) -> list[str]:
    log.info("Refreshing Access Token...")

    refresh_headers = {
        "Content-Type": "application/json",
        "Authorization": f"nadeo_v1 t={refresh_token}",
        "User-Agent": Client.USER_AGENT,
    }

    log.debug("Sending refresh request to Nadeo servers...")
    refresh_session = aiohttp.ClientSession(headers=refresh_headers)
    refresh_response = await refresh_session.post(
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh"
    )

    log.debug("Closing refresh session")
    await refresh_session.close()

    log.debug("Parsing refresh data")
    refresh_json = await refresh_response.json()

    access_token = refresh_json.get("accessToken", None)
    refresh_token = refresh_json.get("refreshToken", None)

    log.debug("Writing Tokens")
    _write_token_file(access_token, refresh_token)

    log.info(
        "Received access token: %s and refresh token: %s", access_token, refresh_token
    )
    return [access_token, refresh_token]


def _write_token_file(access_token: str, refresh_token: str) -> None:
    with open("./bot/resources/temp/token.txt", "w") as token_file:
        token_file.write(f"{access_token}\n{refresh_token}")


def _read_token_file() -> list[str]:
    with open("./bot/resources/temp/token.txt", "r") as token_file:
        return token_file.read().splitlines()


@tasks.loop(minutes=45)
async def refresh_ubisoft_token():
    log.debug("Refreshing the ubisoft token")
    log.debug("Getting access_token and refresh_token")
    tokens = _read_token_file()
    refresh_token = tokens[1]

    log.debug("Refreshing...")
    _refresh_token(refresh_token)
