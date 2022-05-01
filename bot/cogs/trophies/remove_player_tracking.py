import json

from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.moderation import send_in_mod_logs

log = get_logger(__name__)


class RemovePlayerTracking(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="remove-player-tracking",
        description="Adds a player to the trophy tracking list",
    )
    @commands.has_permissions(manage_guild=True)
    async def _remove_player_tracking(
        self,
        ctx: ApplicationContext,
        username: Option(
            SlashCommandOptionType.string,
            "The username of the player to remove.",
            required=True,
        ),
    ):
        log_command(ctx, "remove_player_tracking")

        await ctx.defer(ephemeral=True)

        log.debug("Sending Message to Mod Logs")
        await send_in_mod_logs(
            self.bot,
            ctx.guild.id,
            msg=f"Requestor: {ctx.author.mention} is removing {username} from trophy player tracking.",
        )

        log.debug("Opening JSON File")
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/trophy_tracking.json", "r"
        ) as file:
            tracking_data = json.load(file)

        log.debug("Looping through list to remove the player")
        for player in tracking_data.get("tracking", []):
            if player.get("username").lower() == username.lower():
                log.debug("Found Player")
                tracking_data["tracking"].pop(tracking_data["tracking"].index(player))
                break

        log.debug("Writing JSON File")
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/trophy_tracking.json", "w"
        ) as file:
            json.dump(tracking_data, file, indent=4)

        await ctx.respond(
            f"{username} has been removed from the trophy tracking list.",
            ephemeral=True,
        )


def setup(bot: Bot):
    bot.add_cog(RemovePlayerTracking(bot))
