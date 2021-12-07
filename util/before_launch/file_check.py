import os

import util.logging.convert_logging as convert_logging

# Create Logger
log = convert_logging.get_logging()


def file_check():
    """Checks for Important Files
    Important Files:
        config.json (file)
        /data (directory)
        times_run.txt (file)
    """
    log.info(f"Starting File Check")
    if not os.path.exists("./data/config.json"):
        log.critical(f"Config File Does Not Exist, Please Create it and Run Again")
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
