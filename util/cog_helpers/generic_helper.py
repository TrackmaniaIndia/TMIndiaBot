import json
import platform

import psutil

from util.logging import convert_logging

log = convert_logging.get_logging()


def print_system_info():
    """Print's System Information to the console"""
    architecture = platform.machine()
    hostname = "tmindiabot@" + platform.node()
    platform_details = platform.platform()
    processor = platform.processor()
    # python_build = platform.python_build()
    system = str(platform.system()) + " " + str(platform.release())
    avail_ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"

    log.info("------------------------------")
    log.info(f"Hostname: {hostname}")
    log.info(f"Platform: {platform_details}")
    log.info(f"Processor: {processor}")
    log.info(f"System: {system}")
    log.info(f"Architecture: {architecture}")
    log.info(f"Available Ram: {avail_ram}")
    log.info("------------------------------")


def get_version():
    """Get's Current Version of the Bot"""
    with open("./data/config.json", encoding="UTF-8") as file:
        config = json.load(file)
        version = config["bot_version"]
        file.close()

    return version
