import discord
from bot.api import APIClient


class TrackmaniaUtils:
    def __init__(self, username: str):
        self.username = usernames
        self.api_client = APIClient()

    def get_id(self):
        id_data = self.api_client.request(
            "GET", f"http://localhost:3000/tm2020/player/{self.username}/id"
        )

        try:
            return id_data["id"]
        except KeyError:
            raise NotAValidUsername


class NotAValidUsername(Exception):
    def __init__(self, excp: Exception):
        self.message = excp.message

    def __str__(self):
        return self.message if self.message is not None else None
