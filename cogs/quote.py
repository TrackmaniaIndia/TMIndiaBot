import discord
import util.logging.convert_logging as convert_logging
import util.quoting.quote as quote_functions
import util.discord.easy_embed as ezembed
import os

from util.constants import GUILD_IDS, MAIN_SERVER_ID, TESTING_SERVER_ID
from discord.commands import permissions
from discord.ext import commands
from discord.commands.commands import Option

log = convert_logging.get_logging()


class Quote(commands.Cog, description="Quoting Functions"):
    def __init__(self, client):
        self.client = client
        log.info(f"cogs.quote has finished initializing")

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="quote",
        description="Saves a Quote, Only Usable by Mods",
        default_permission=False,
    )
    @permissions.has_any_role(
        "Moderator",
        "Admin",
        "Bot Developer",
        "admin",
    )
    async def _quote(
        self,
        ctx: commands.Context,
        *,
        message: Option(
            str,
            'Message you want to quote in format "Message - Author"',
            required=True,
        ),
    ):
        message, author = message.split(" - ")

        log.debug(f"Saving {message} by {author}")

        quote_functions.save(message, author)
        embed = ezembed.create_embed(
            title=":white_check_mark: Saved",
            description=f"Saved {message} by {author}",
            color=discord.Colour.green(),
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(
        guild_ids=GUILD_IDS, name="randquote", description="Shows a random saved quote"
    )
    async def _rand_quote(self, ctx: commands.Context):
        log.debug(f"Getting Random Quote")
        rand_quote = quote_functions.get_random_quote_dict()

        log.debug(f"Getting Quote Embed")
        embed = quote_functions.quote_dict_to_embed(rand_quote)

        log.debug(f"Sending Random Quote")
        await ctx.respond(embed=embed)

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="lastquote",
        description="Displays the last quote saved",
    )
    async def _last_quote(self, ctx: commands.Context):
        log.debug(f"Getting the Last Quote Saved")
        quote_embed = quote_functions.get_last_quote()

        await ctx.respond(embed=quote_embed)


def setup(client: discord.Bot):
    client.add_cog(Quote(client))
