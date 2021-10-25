from requests.api import request
import util.logging.convert_logging as cl
from discord.ext import tasks, commands
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import threading

log = cl.get_logging()


@tasks.loop(minutes=30)
async def keep_alive(client: commands.Bot):
    log.debug(f"30 Minutes have passed, Task activated - at {datetime.utcnow()}")
    log.debug(f"Pinging API")
    try:
        ping_api()
        log.debug(f"API Ping Successful")
    except:
        log.error("API is Offline")
    log.debug(f"Sending Message to Channel to Keep This Damned Thing Alive")
    log.debug(f"Got Channel Successfully")
    channel = client.get_channel(881732050451849216)
    log.debug(f"Sending Message to Channel")
    await channel.send(f"Bot is still alive at {datetime.utcnow()}")
    log.debug(f"Sent Message to Channel")


def ping_api():
    log.debug(f"Loading Dotenv")
    load_dotenv()
    BASE_API_URL = os.getenv("BASE_API_URL")

    log.info(f"Requesting from API")
    try:
        log.debug(f'Creating Thread for API Ping')
        request_thread = threading.Thread(target=requests.get, args=(str(BASE_API_URL),))
        log.info(f'Created Thread for Pinging API, Starting')
        my_request = request_thread.start()
        log.info(f'Request Successful, Joining Thread')
        request_thread.join()
        log.debug(f'Thread Joined')
    except:
        raise Exception("API is OFFLINE")
    log.info(f"Successfully Received Data from API")
