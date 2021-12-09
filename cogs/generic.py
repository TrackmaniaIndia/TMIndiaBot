import discord

import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from discord.ext import commands
from discord.commands import permissions
from util.discord.paginator import Paginator
from util.discord.confirmation import Confirmer
from util.cog_helpers.generic_helper import get_version
from util.constants import GUILD_IDS

# Creating Logger
log = convert_logging.get_logging()


class Generic(commands.Cog, description="Generic Functions"):
    # Statuses for the bot, will be gotten by a function.
    version = ""

    # Init Generic Cog
    def __init__(self, client):
        self.client = client
        self.version = get_version()

        log.info(f"cogs.generic has finished initializing")

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="ping",
        description="Get ping of bot to discord api in milliseconds",
    )
    async def _ping(self, ctx: commands.Context):
        await ctx.respond("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.slash_command(
        guild_ids=GUILD_IDS, name="version", description="Displays bot version"
    )
    async def _version(self, ctx: commands.Context):
        await ctx.respond(f"Bot Version is {self.version}", ephemeral=True)

    @commands.slash_command(
        guild_ids=GUILD_IDS, name="source", description="Displays Github Source Code"
    )
    async def _source(self, ctx: commands.Context):
        await ctx.respond(
            "Here is the source code\n<https://github.com/NottCurious/TMIndiaBot>",
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="invite",
        description="Gives you an invite link for the server",
    )
    async def _server_invite(self, ctx: commands.Context):
        await ctx.respond(
            "Here is an invite for you to share with your friends\nhttps://discord.gg/yvgFYsTKNr",
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="halloffame",
        description="Gives you the link for the TMI Hall of Fame",
    )
    async def _link_to_hall_of_fame(self, ctx: commands.Context):
        await ctx.respond(
            f"Here is the link to the TMI Hall of Fame\n<https://tinyurl.com/TMIndiaLB>",
            ephemeral=True,
        )

    @commands.slash_command(guild_ids=GUILD_IDS, name="testpagination")
    @permissions.is_owner()
    async def _test(self, ctx: commands.Context):
        # Creating 4 Embeds for Paginator
        embed1 = ezembed.create_embed(
            title="Testing 1", description="Testing 1's Description"
        )
        embed2 = ezembed.create_embed(
            title="Testing 2", description="Testing 2's Description"
        )
        embed3 = ezembed.create_embed(
            title="Testing 3",
            description="adjskbabdjasdjlaskbdawkudbuiwabdiwbdkbsgfrduidgbufdjklasljkdwbaldlalkds",
        )
        embed4 = ezembed.create_embed(
            title="Testing 4", description="Testing 4's Description"
        )
        embed_list = [embed1, embed2, embed3, embed4]

        # Deferring the Bot, Allows a lot more time for the bot to do its stuff
        log.debug(f"Deferring the Bot Response")
        await ctx.defer()
        log.debug(f"Deferred the Bot Response")

        # Creating and running the Paginator
        my_pag = Paginator(pages=embed_list, sending=True)
        await my_pag.run(ctx)

    @commands.slash_command(guild_ids=GUILD_IDS, name="testconfirm")
    @permissions.is_owner()
    async def _test_confirm(self, ctx: commands.Context):
        # Creating the Confirmer
        my_confirmer = Confirmer()
        my_confirmer.change_cancel_button("Cancel Me Senpai")
        my_confirmer.change_confirm_button("Confirm Me pls")
        await ctx.respond("Do You Want to Continue", view=my_confirmer)

        # Awaiting a response
        await my_confirmer.wait()

        await ctx.send(my_confirmer.value)


def setup(client: discord.Bot):
    client.add_cog(Generic(client))
