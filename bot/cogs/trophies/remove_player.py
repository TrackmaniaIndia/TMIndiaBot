import json
from typing import Dict

from discord import ApplicationContext, Bot
from discord.commands import Option, permissions
from discord.ext import commands
from trackmania import Player

from bot import constants
from bot.log import get_logger, log_command

log = get_logger(__name__)


class RemovePlayerTracking(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="removeplayertracking",
        description="Adds a player to the trophy tracking list",
    )
    @permissions.has_any_role(
        "Moderator", "Admin", "Bot Developer", "Bot Testing", "Manager"
    )
    async def _remove_player_tracking(
        self,
        ctx: ApplicationContext,
        username: Option(str, "The username of the player to add.", required=True),
    ):
        log_command(ctx, "remove_player_tracking")

        await ctx.defer()

        log.debug("Opening JSON File")
        with open("./bot/resources/json/trophy_tracking.json", "r") as file:
            tracking_data = json.load(file)

        log.debug("Looping through list to remove the player")
        for player in tracking_data["tracking"]:
            if player.get("username").lower() == username.lower():
                log.debug("Found Player")
                tracking_data["tracking"].pop(tracking_data["tracking"].index(player))
                break

        log.debug("Writing JSON File")
        with open("./bot/resources/json/trophy_tracking.json", "w") as file:
            json.dump(tracking_data, file, indent=4)

        await ctx.respond(f"{username} has been removed from the trophy tracking list.")


def setup(bot: Bot):
    bot.add_cog(RemovePlayerTracking(bot))
