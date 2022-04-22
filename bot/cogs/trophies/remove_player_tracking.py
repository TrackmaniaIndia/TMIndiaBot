import json

import discord as discord
from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class RemovePlayerTracking(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="remove-player-tracking",
        description="Adds a player to the trophy tracking list",
    )
    @discord.has_any_role(
        805318382441988096, 858620171334057994, guild_id=constants.Guild.tmi_server
    )
    @discord.has_any_role(
        940194181731725373, 941215148222341181, guild_id=constants.Guild.testing_server
    )
    async def _remove_player_tracking(
        self,
        ctx: ApplicationContext,
        username: Option(str, "The username of the player to remove.", required=True),
    ):
        log_command(ctx, "remove_player_tracking")

        await ctx.defer()

        log.debug("Sending Message to Mod Logs")
        mod_logs_channel = self.bot.get_channel(constants.Channels.mod_logs)
        if mod_logs_channel is not None:
            await mod_logs_channel.send(
                content=f"Requestor: {ctx.author} is removing {username} from trophy player tracking."
            )

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
