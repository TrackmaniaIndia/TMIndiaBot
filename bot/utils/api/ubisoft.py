# https://gist.github.com/codecat/4dfd3719e1f8d9e5ef439d639abe0de4

import asyncio
import base64
import json
import sys

import aiohttp
import discord.ext.tasks as tasks
from trackmania import Client

from bot import constants
from bot.log import get_logger

log = get_logger(__name__)


async def deprecated_authentication() -> list[str]:
    # ----- First Step -----
    log.info("Authenticating with Ubisoft.")

    ubi_auth_headers = {
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
        "User-Agent": Client.USER_AGENT,
    }

    auth = aiohttp.BasicAuth(
        constants.Consts.tm_dedi_server_login, constants.Consts.tm_dedi_server_password
    )

    log.debug("Sending authentication request to Nadeo Servers...")
    authentication_session = aiohttp.ClientSession(auth=auth, headers=ubi_auth_headers)
    # authentication_response = await authentication_session.post(
    #     "https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic"
    # )
    # ^ This is for dedicated accounts

    authentication_response = await authentication_session.post(
        "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    )

    auth_response_json = await authentication_response.json()
    ticket = auth_response_json.get("ticket")
    log.critical("Ubisoft Authentication Finished.")
    log.debug("Closing Ubisoft Authentication Session")
    await authentication_session.close()

    # ----- Second Part -----
    log.critical("Authenticating with Nadeo.")

    nadeo_headers = {
        "Content-Type": "application/json",
        "User-Agent": Client.USER_AGENT,
        "Authorization": "ubi_v1 t=" + ticket,
    }

    nadeo_session = aiohttp.ClientSession(
        headers=nadeo_headers,
    )

    nadeo_response = await nadeo_session.post(
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices",
    )
    nadeo_response_json = await nadeo_response.json()
    log.critical("Authenticated with Nadeo.")

    access_token = nadeo_response_json.get("accessToken", None)
    refresh_token = nadeo_response_json.get("refreshToken", None)

    await nadeo_session.close()

    log.debug("Writing Tokens")
    _write_token_file(access_token, refresh_token)

    log.info(
        "Received access token: %s and refresh token: %s", access_token, refresh_token
    )
    return [access_token, refresh_token]


async def authenticate() -> list[str]:
    # ----- Authenticating with Ubisoft -----
    log.info("Authenticating with Ubisoft.")
    auth_headers = {
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
        "User-Agent": "TMIndia Discord Bot | NottCurious#4351 on Discord.",
        "audience": "NadeoLiveServices",
    }

    # Creating the aiohttp session.
    log.debug("Creating the aiohttp session.")
    auth_session = aiohttp.ClientSession(
        auth=aiohttp.BasicAuth(
            constants.Consts.tm_dedi_server_login,
            constants.Consts.tm_dedi_server_password,
        ),
        headers=auth_headers,
    )

    # Making the POST request.
    log.debug("Making the POST request to Nadeo.")
    auth_response = await auth_session.request(
        "POST",
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic",
    )
    auth_response = await auth_session.post(
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic",
        data=json.dumps({"audience": "NadeoLiveServices"}),
    )

    # Closing Authentication Session
    log.debug("Closing Authentication Session.")
    await auth_session.close()

    # Getting the accessToken and refreshToken.
    log.debug("Getting access and refresh tokens from response.")
    auth_json = await auth_response.json()
    access_token = auth_json.get("accessToken")
    refresh_token = auth_json.get("refreshToken")

    log.debug("Received accessToken: %s" % (access_token))
    log.debug("Received refreshToken: %s" % (refresh_token))

    # Writing Tokens to Files.
    log.debug("Writing Tokens to Files.")
    _write_token_file(access_token, refresh_token)

    # returning tokens
    log.info("Returning Tokens.")
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
