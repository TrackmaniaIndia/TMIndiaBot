from discord import Embed
from discord.ext import commands

from bot import constants
from bot.bot import Bot

DESCRIPTIONS = ("Discord API latency",)
ROUND_LATENCY = 3


class Latency(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds, name="ping", description="Gets Latency"
    )
    async def _ping(self, ctx: commands.Context) -> None:
        discord_ping = f"{self.bot.latency * 1000:.{ROUND_LATENCY}f} ms"

        embed = Embed(title="Pong!")

        for desc, latency in zip(DESCRIPTIONS, [discord_ping]):
            embed.add_field(name=desc, value=latency, inline=False)

        await ctx.respond(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Latency(bot))
