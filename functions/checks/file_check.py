import os
import logging
import functions.logging.convert_logging as cl

log = logging.getLogger(__name__)
log = cl.get_logging()


def check():
    """Checks if the Files Exists"""
    log.debug(f"Checking files")

    # dictionary of all files
    files = {
        "json": (
                 "./data/json_data/announcement_channels.json",
                 "./data/json_data/config.json",
                 "./data/json_data/prefixes.json",
                 "./data/json_data/statuses.json",
                 "./data/json_data/tm2020_usernames.json",
                 ),
        "cog": (
                "./cogs/channel_commands.py",
                "./cogs/cotd.py",
                "./cogs/generic.py",
                "./cogs/moderation.py",
                "./cogs/owner.py",
                "./cogs/tm_commands.py",
                "./cogs/username_commands.py",
                ),
        "data": (
                 "./data/times_run.txt",
                 ),
        "functions": (
                      "./functions/ciphers/vigenere_cipher.py", # ciphers
                      "./functions/cog_helpers/cotd_functions.py", #            \
                      "./functions/cog_helpers/generic_functions.py", #         | Cog Helpers
                      "./functions/cog_helpers/tm_commands_functions.py", #     /
                      "./functions/common_functions/common_functions.py", # common functions
                      "./functions/custom_errors/custom_errors.py", # custom errors
                      "./functions/logging/convert_logging.py", #  \
                      "./functions/logging/usage.py", #            / Logging
                      "./functions/other_functions/get_data.py", # other functions
                      "./functions/task_helpers/pingapi.py", # task helpers
                      "./functions/tm_username_functions/username_functions.py", # TM username functions
                      ),
    }

    print(f"Beginning Check")
    print(f"Checking all JSON Files")

    # checking for the existence of files
    for types in files:
        for file in files[types]:
            if not os.path.exists(file):
                log.error(f"{file} does not exist")
        log.debug(f"{types} checked")

    log.debug(f"Checked all files")
