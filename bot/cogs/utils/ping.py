import discord.ext.commands as commands
from discord import ApplicationContext

from bot.bot import Bot
from bot.utils.discord import create_embed

DESCRIPTIONS = ("Discord API latency",)
ROUND_LATENCY = 3


class Latency(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="ping", description="Gets Latency")
    async def _ping(self, ctx: ApplicationContext) -> None:
        discord_ping = f"{self.bot.latency * 1000:.{ROUND_LATENCY}f} ms"

        embed = create_embed(title="Pong!")

        for desc, latency in zip(DESCRIPTIONS, [discord_ping]):
            embed.add_field(name=desc, value=latency, inline=False)

        await ctx.respond(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Latency(bot))
