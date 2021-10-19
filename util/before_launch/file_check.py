import os
import util.logging.convert_logging as cl
import json

DEFAULT_PREFIX = "--"

log = cl.get_logger()


def file_check():
    log.info(f"Starting File Check")
    if not os.path.exists("./data/config.json"):
        log.critical(f"Config File Does Not Exist, Please Create it and Run Again")
        exit()
    if not os.path.exists("./data/json/prefixes.json"):
        log.critical(
            "Prefixes.json Doesn't Exist, Creating and Dumping Testing Server Stuff"
        )
        log.critical("Edit Prefixes.json to add your own Testing Server ID")

        prefixes = {"876042400005505066": DEFAULT_PREFIX}

        with open("./data/json_data/prefixes.json", "w") as file:
            json.dump(prefixes, file, indent=4)
            file.close()

        log.critical("Prefixes.json Created, Please Restart the Program")
        exit()
