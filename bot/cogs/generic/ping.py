import arrow
from aiohttp import client_exceptions
from discord import Embed
from discord.ext import commands

from bot.bot import Bot
from bot import constants

DESCRIPTIONS = (
    "Command processing time",
    "Discord API latency",
)
ROUND_LATENCY = 3


class Latency(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds, name="ping", description="Gets Latency"
    )
    async def _ping(self, ctx: commands.Context) -> None:
        bot_ping = (arrow.utcnow() - ctx.message.created_at).total_seconds() * 1000

        if bot_ping <= 0:
            bot_ping = "Your clock is out of sync, could not calculate ping."
        else:
            bot_ping = f"{bot_ping:.{ROUND_LATENCY}f}ms"

        discord_ping = f"{self.bot.latency * 1000:.{ROUND_LATENCY}f} ms"

        embed = Embed(title="Pong!")

        for desc, latency in zip(DESCRIPTIONS, [bot_ping, discord_ping]):
            embed.add_field(name=desc, value=latency, inline=False)

        await ctx.respond(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Latency(bot))
