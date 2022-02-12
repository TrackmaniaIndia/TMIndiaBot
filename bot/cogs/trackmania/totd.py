import discord
from discord import ApplicationContext
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.cotd_util import TOTDUtils
from bot.utils.discord import ViewAdder

log = get_logger(__name__)


class TOTD(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds, name="totd", description="Latest TOTD"
    )
    @discord.ext.commands.cooldown(1, 30, commands.BucketType.guild)
    async def _totd_slash(self, ctx: ApplicationContext):
        log_command(ctx, "totd_slash")

        log.debug("Deferring Response")
        await ctx.defer()
        log.debug("Deferred Response, Awaiting Information")

        log.info("Getting TOTD Information")
        (
            totd_embed,
            image,
            download_link,
            tmio_link,
            tmx_link,
        ) = await TOTDUtils.today()
        log.info("Got Information, Sending Response")

        log.info("Creating Buttons to Add")
        download_map = discord.ui.Button(
            label="Download Map!", style=discord.ButtonStyle.primary, url=download_link
        )
        tmio_button = discord.ui.Button(
            label="TMIO", style=discord.ButtonStyle.url, url=tmio_link
        )

        log.info("Sending the Embed")
        if tmx_link is not None:
            tmx_button = discord.ui.Button(
                label="TMX", style=discord.ButtonStyle.url, url=tmx_link
            )

            await ctx.respond(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button, tmx_button]),
            )
        else:
            await ctx.respond(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button]),
            )

    @commands.command(name="totd", description="Latest TOTD")
    @discord.ext.commands.cooldown(1, 30, commands.BucketType.guild)
    async def _totd(self, ctx: commands.Context):
        log_command(ctx, "totd")

        log.info("Getting TOTD Information")
        (
            totd_embed,
            image,
            download_link,
            tmio_link,
            tmx_link,
        ) = await TOTDUtils.today()
        log.info("Got Information, Sending Response")

        log.info("Creating Buttons to Add")
        download_map = discord.ui.Button(
            label="Download Map!", style=discord.ButtonStyle.primary, url=download_link
        )
        tmio_button = discord.ui.Button(
            label="TMIO", style=discord.ButtonStyle.url, url=tmio_link
        )

        log.info("Sending the Embed")
        if tmx_link is not None:
            tmx_button = discord.ui.Button(
                label="TMX", style=discord.ButtonStyle.url, url=tmx_link
            )

            await ctx.send(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button, tmx_button]),
            )
        else:
            await ctx.send(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button]),
            )


def setup(bot: Bot):
    bot.add_cog(TOTD(bot))
