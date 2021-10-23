import util.logging.convert_logging as cl
import psutil
import platform
import json
from discord.ext import commands

log = cl.get_logging()
DEFAULT_PREFIX = "--"


def print_system_info():
    architecture = platform.machine()
    hostname = "tmindiabot@" + platform.node()
    platform_details = platform.platform()
    processor = platform.processor()
    # python_build = platform.python_build()
    system = str(platform.system()) + " " + str(platform.release())
    avail_ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"

    full_system_info = (
        "------------------------------\n"
        + f"Hostname: {hostname}\n"
        + f"Platform: {platform_details}\n"
        + f"Processor: {processor}\n"
        + f"System: {system}\n"
        + f"Architecture: {architecture}\n"
        + f"Available Ram: {avail_ram}\n"
        + f"------------------------------"
    )

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
    with open("./data/config.json") as file:
        config = json.load(file)
        version = config["bot_version"]
        file.close()

    return version


def change_prefix(ctx: commands.Context, prefix: str) -> bool:
    """Changes the Prefix for a Given Server

    Args:
        ctx (commands.Context): Application Context for ID and Name
        prefix (str): The Prefix to Change to

    Returns:
        bool: > True if Success, > False if failure
    """
    log.info(f"Changing Prefix in {ctx.guild}")

    with open("./data/json/prefixes.json", "r") as file:
        log.debug("Opening Prefixes JSON")
        prefixes = json.load(file)
        file.close()

    log.debug(f"Changing Prefix")
    if prefix != "":
        prefixes[str(ctx.guild.id)] = [prefix, DEFAULT_PREFIX]
    else:
        prefixes[str(ctx.guild.id)] = DEFAULT_PREFIX
    log.debug(f"Changed Prefix")

    with open("./data/json/prefixes.json", "w") as file:
        log.debug("Dumping Prefixes to File")
        json.dump(prefixes, file, indent=4)
        file.close()
