import os
import sys

from util.logging import convert_logging

# Create Logger
log = convert_logging.get_logging()


def file_check():
    """Checks for Important Files
    Important Files:
        config.json (file)
        /data (directory)
        times_run.txt (file)
    """
    log.info("Starting File Check")
    if not os.path.exists("./data/config.json"):
        log.critical("Config File Does Not Exist, Please Create it and Run Again")
        sys.exit()
    log.debug("Checking for Times Run File")
    if not os.path.exists("./data"):
        log.critical("Data Directory doesn't Exist, Creating")
        os.mkdir("./data")
    if not os.path.exists("./data/times_run.txt"):
        log.critical("Times Run File doesn't Exist, Creating")
        with open("./data/times_run.txt", "w", encoding="UTF-8") as file:
            print(0, file=file)
    if not os.path.exists("./logs"):
        log.critical("Logs Folder does not exist, Creating")
        os.mkdir("./logs")
    if not os.path.exists("./logs/commands.log"):
        log.critical("Command Logs File does not exist, Creating")
        with open("./logs/commands.log", "w", encoding="UTF-8") as file:
            print("", file=file)
