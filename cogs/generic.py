import discord
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import os

from discord.ext import commands
from discord.commands import permissions
from util.discord.paginator import Paginator
from util.discord.confirmation import Confirmer
from util.cog_helpers.generic_helper import get_version
from util.constants import GUILD_IDS


log = convert_logging.get_logging()


class Generic(commands.Cog, description="Generic Functions"):
    statuses = []
    version = ""

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
            "Here is the source code\nhttps://github.com/NottCurious/TMIndiaBot",
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

    @commands.slash_command(guild_ids=GUILD_IDS, name="testpagination")
    @permissions.is_owner()
    async def _test(self, ctx: commands.Context):
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

        immediate_message = await ctx.respond("Please Wait, I am working...")

        my_pag = Paginator(pages=embed_list, sending=True)
        await immediate_message.delete_original_message()
        await my_pag.run(ctx)

    @commands.slash_command(guild_ids=GUILD_IDS, name="testconfirm")
    @permissions.is_owner()
    async def _test_confirm(self, ctx: commands.Context):
        my_confirmer = Confirmer()
        my_confirmer.change_cancel_button("Cancel Me Senpai")
        my_confirmer.change_confirm_button("Confirm Me pls")
        await ctx.respond("Do You Want to Continue", view=my_confirmer)
        await my_confirmer.wait()

        await ctx.send(my_confirmer.value)


def setup(client):
    client.add_cog(Generic(client))
