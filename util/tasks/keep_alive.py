import os
import threading
from datetime import datetime
from logging import raiseExceptions

import discord
import requests
from discord.ext import tasks
from dotenv import load_dotenv

from util.logging import convert_logging

log = convert_logging.get_logging()


@tasks.loop(minutes=10)
async def keep_alive(client: discord.Bot):
    log.debug(f"10 Minutes have passed, Task activated - at {datetime.utcnow()}")
    log.debug("Pinging API")
    try:
        ping_api()
        log.debug("API Ping Successful")
    except:
        log.error("API is Offline")
    log.debug("Sending Message to Channel to Keep This Damned Thing Alive")
    log.debug("Got Channel Successfully")
    channel = client.get_channel(881732050451849216)
    log.debug("Sending Message to Channel")
    await channel.send(f"Bot is still alive at {datetime.utcnow()}")
    log.debug("Sent Message to Channel")


def ping_api():
    log.debug("Loading Dotenv")
    load_dotenv()
    base_api_url = os.getenv("base_api_url")

    log.info("Requesting from API")
    try:
        log.debug("Creating Thread for API Ping")
        request_thread = threading.Thread(
            target=requests.get, args=(str(base_api_url),)
        )
        log.info("Created Thread for Pinging API, Starting")
        my_request = request_thread.start()
        del my_request
        log.info("Request Successful, Joining Thread")
        request_thread.join()
        log.debug("Thread Joined")
    except:
        raise Exception("API is OFFLINE")
    log.info("Successfully Received Data from API")
