import os
import util.logging.convert_logging as cl
import json

DEFAULT_PREFIX = "--"

log = cl.get_logging()


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

        with open("./data/json/prefixes.json", "w") as file:
            json.dump(prefixes, file, indent=4)
            file.close()

        log.critical("Prefixes.json Created, Please Restart the Program")
        exit()
    log.debug(f"Checking for Times Run File")
    if not os.path.exists("./data"):
        log.critical("Data Directory doesn't Exist, Creating")
        os.mkdir("./data")
    if not os.path.exists("./data/times_run.txt"):
        log.critical("Times Run File doesn't Exist, Creating")
        with open("./data/times_run.txt", "w") as file:
            print(0, file=file)

    return
    log.info("All Files Exist")
