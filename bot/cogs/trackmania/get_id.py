from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands
from trackmania import Player

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class GetID(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="get-id",
        description="Gets an ID for a specific username",
    )
    async def _get_id(
        self,
        ctx: ApplicationContext,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "get_id")

        await ctx.defer()

        log.info(f"Getting ID for {username}")
        id = await Player.get_id(username)

        await ctx.respond(
            embed=EZEmbed.create_embed(
                title=f"Here is the ID for {username}",
                description=id if id is not None else "Invalid Username.",
            ),
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="getchannel",
    )
    async def _get_channel(self, ctx: ApplicationContext):
        await ctx.defer()

        channel = self.bot.get_channel(constants.Channels.tm2020)
        print(channel.name)

        embed = EZEmbed.create_embed(
            title="Hi, This is just a test. Please ignore if you can see this",
            color=0xFF00FF,
        )

        log.warn("Sending Message")
        await channel.send(embed=embed, delete_after=3)
        log.warn("Sent Message")

        await ctx.respond("hi")


def setup(bot: Bot):
    """Add the GetID Cog"""
    bot.add_cog(GetID(bot))
