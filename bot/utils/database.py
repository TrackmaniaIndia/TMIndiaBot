import typing
import json

from bot.log import get_logger

log = get_logger(__name__)


class Database:
    """Functions relating to accessing and retrieving data from files stored on the computer"""

    @staticmethod
    def retrieve_id(player_username: str) -> typing.Union[str, None]:
        """Retrieves the ID of the Username from the file, if the Username is not in the file, returns `None`

        Args:
            player_username (str): The username of the player

        Returns:
            str: The ID of the player from the computer's JSON file, if it does not exist it returns `None`
        """

        log.debug("Opening the Username, ID file")
        with open("./bot/resources/json/ids.json", "r", encoding="UTF-8") as file:
            ids = json.load(file)["IDS"]

        log.debug("Looping through the IDs Array")
        for player in ids:
            if player["Username"].lower() == player_username.lower():
                log.info(
                    f'Returning the ID of Username: {player["Username"]} and ID: {player["ID"]}'
                )
                return player["ID"]

        log.debug("Username not in file")
        return None

    @staticmethod
    def store_id(player_username: str, player_id: str) -> bool:
        """Stores the Player's Username and ID to the `ids.json` file

        Args:
            player_username (str): The player's username
            player_id (str): The player's id

        Returns:
            bool: `True` if success else `False`
        """

        try:
            with open("./bot/resources/json/ids.json", "r", encoding="UTF-8") as file:
                ids_data = json.load(file)["IDS"]

            ids_data.append({"Username": player_username, "ID": player_id})

            with open("./bot/resources/json/ids.json", "w", encoding="UTF-8") as file:
                json.dump({"IDS": ids_data}, file, indent=4)

            return True
        except:
            return False
