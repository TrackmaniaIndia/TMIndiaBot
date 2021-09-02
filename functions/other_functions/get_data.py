import json


def get_version():
    with open("./json_data/config.json") as file:
        config = json.load(file)
        version = config["bot_version"]
        file.close()

    return version
