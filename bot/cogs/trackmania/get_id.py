from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands
from trackmania import Player

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class GetID(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="get-id",
        description="Gets an ID for a specific username",
    )
    async def _get_id(
        self,
        ctx: ApplicationContext,
        username: Option(
            SlashCommandOptionType.string, "The username of the player", required=True
        ),
    ):
        log_command(ctx, "get_id")

        await ctx.defer()

        log.info(f"Getting ID for {username}")
        id = await Player.get_id(username)

        await ctx.respond(
            embed=create_embed(
                title=f"Here is the ID for {username}",
                description=id if id is not None else "Invalid Username.",
            ),
            ephemeral=True,
        )


def setup(bot: Bot):
    """Add the GetID Cog"""
    bot.add_cog(GetID(bot))
