from bot.api import APIClient


class TrackmaniaUtils:
    def __init__(self, username: str):
        self.username = username
        self.api_client = APIClient()

    async def close(self):
        await self.api_client.close()
        return

    async def get_id(self):
        id_data = await self.api_client.get(
            f"http://localhost:3000/tm2020/player/{self.username}/id"
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
