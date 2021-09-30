import os
import logging
import functions.logging.convert_logging as cl

log = logging.getLogger(__name__)
log = cl.get_logging()


def check():
    log.debug(f"Checking files")

    json_files = (
        "./json_data/announcement_channels.json",
        "./json_data/config.json",
        "./json_data/prefixes.json",
        "./json_data/statuses.json",
        "./json_data/tm2020_usernames.json",
    )
    cog_files = (
        "./cogs/channel_commands.py",
        "./cogs/cotd.py",
        "./cogs/generic.py",
        "./cogs/moderation.py",
        "./cogs/owner.py",
        "./cogs/tm_commands.py",
        "./cogs/username_commands.py",
    )
    data_files = ("./data/times_run.txt",)
    functions = (
        ("./functions/ciphers/vigenere_cipher.py",),  # Ciphers
        (
            "./functions/cog_helpers/cotd_functions.py",
            "./functions/cog_helpers/generic_functions.py",
            "./functions/cog_helpers/tm_commands_functions.py",
        ),  # Cog Helpers
        ("./functions/common_functions/common_functions.py",),  # Common Functions
        ("./functions/custom_errors/custom_errors.py",),  # Custom Errors
        (
            "./functions/logging/convert_logging.py",
            "./functions/logging/usage.py",
        ),  # Logging
        ("./functions/other_functions/get_data.py",),  # Other Functions
        ("./functions/task_helpers/pingapi.py",),  # Task Helpers
        (
            "./functions/tm_username_functions/username_functions.py",
        ),  # TM Username Functions
    )

    log.debug(f"Beginning Check")
    log.debug(f"Checking all JSON Files")

    for filename in json_files:
        if not os.path.exists(filename):
            log.error(f"{filename} does not exist, exiting")
            exit()
        else:
            log.debug(f"{filename} exists")

    log.debug(f"Checked all JSON Files")
    log.debug(f"Checking all Cog Files")

    for filename in cog_files:
        if not os.path.exists(filename):
            log.error(f"{filename} does not exist, exiting")
            exit()
        else:
            log.debug(f"{filename} exists")

    log.debug(f"Checked all Cog Files")
    log.debug(f"Checking all Data Files")

    for filename in data_files:
        if not os.path.exists(filename):
            log.error(f"{filename} does not exist, exiting")
            exit()
        else:
            log.debug(f"{filename} exists")

    log.debug(f"Checked all Data Files")
    log.debug(f"Checking all Functions")

    for function_group in functions:
        for filename in function_group:
            if not os.path.exists(filename):
                log.error(f"{filename} does not exist, exiting")
                exit()
            else:
                log.debug(f"{filename} exists")

    log.debug(f"Checked all Functions")
    log.debug(f"All files exist, goodluck")
