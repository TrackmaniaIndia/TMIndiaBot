from bot.utils.database import Database

from bot.api import APIClient
from bot.log import get_logger

log = get_logger(__name__)


class TrackmaniaUtils:
    """Functions relating to a specific Trackmania player who is given while creating the object"""

    def __init__(self, username: str):
        self.username = username
        self.api_client = APIClient()

    async def close(self):
        """Closes the API Client"""
        await self.api_client.close()
        return

    async def get_id(self) -> str:
        """Gets the ID of the Player from the API

        Raises:
            NotAValidUsername: If the username is not valid, this exception is raised.

        Returns:
            str: The ID of the player
        """
        log.debug("Checking if the ID is in the file")
        id = Database.retrieve_id(self.username)

        if id is None:
            log.debug("Getting the data from the TMIndiaBotAPI")
            id_data = await self.api_client.get(
                f"http://localhost:3000/tm2020/player/{self.username}/id"
            )

            try:
                id = id_data["id"]
            except KeyError:
                id = None

            log.debug("Storing the Username and ID to the file")
            Database.store_id(self.username, id)

        else:
            log.debug("Username exists in file")

        return id


class NotAValidUsername(Exception):
    """Raised when the Username given is not valid.

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, excp: Exception):
        self.message = excp.message

    def __str__(self):
        return self.message if self.message is not None else None
