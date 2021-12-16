import discord
import os

from discord.ui import view

import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from discord.ext import commands
from discord.commands import permissions
from util.discord.paginator import Paginator
from util.discord.confirmation import Confirmer
from util.discord.view_adder import ViewAdder
from util.logging.command_log import log_command
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
        log_command(ctx, ctx.command.name)
        await ctx.respond("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.slash_command(
        guild_ids=GUILD_IDS, name="version", description="Displays bot version"
    )
    async def _version(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        await ctx.respond(f"Bot Version is {self.version}", ephemeral=True)

    @commands.slash_command(
        guild_ids=GUILD_IDS, name="source", description="Displays Github Source Code"
    )
    async def _source(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        log.debug(f"Creating Button for Source Code")
        source_code_button = discord.ui.Button(
            label="Source Code (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot",
        )
        log.debug(f"Created Button for Source Code, Sending a message")
        await ctx.respond(
            content="Hey!\nHere is the source code. The bot is open source and licensed under the MIT License. It is currently developed and maintained by NottCurious and Artifex.\nAll Issues/Feature Requests/Bug Reports and Pull Requests are welcome and appreciated!",
            view=ViewAdder([source_code_button]),
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="invite",
        description="Gives you an invite link for the server",
    )
    async def _server_invite(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
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
        log_command(ctx, ctx.command.name)
        log.debug(f"Creating Button for Hall of Fame")
        hall_of_fame_button = discord.ui.Button(
            label="TMI Hall of Fame (Google Sheets)",
            style=discord.ButtonStyle.url,
            url="https://tinyurl.com/TMIndiaLB",
        )
        log.debug(f"Created Button for Hall of Fame, Sending a message")
        await ctx.respond(
            f"Please click the button to be redirected to the hall of fame",
            view=ViewAdder([hall_of_fame_button]),
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="nextproject",
        description="A Github link to the next project, has planned, in progress and finished features.",
    )
    async def _next_project(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        log.debug(f"Creating Button for Next Project")
        next_project_button = discord.ui.Button(
            label="Next Project - v1.6.1 (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot/projects/6",
        )
        await ctx.respond(
            f"Here is the link to the next project",
            view=ViewAdder([next_project_button]),
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="invitebot",
        description="Give an invite link for the bot",
    )
    async def _invite_bot(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)

        await ctx.respond(
            embed=ezembed.create_embed(
                title="Bot Invite",
                description="Hey! Thanks for your interest in TMI Bot. This bot may have lots of bugs and issues to be ironed out. If the bot suddenly stops working please contact NottCurious#4351 immediately.\n\n[Click Here to Invite the Bot!](https://discord.com/api/oauth2/authorize?client_id=901407301175484447&permissions=534925274176&scope=bot%20applications.commands)",
            ),
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="testingserver",
        description="Get an invite to the testing server",
    )
    async def _testing_server_invite(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)

        await ctx.respond(
            f"Here is an invite to the testing server\nhttps://discord.gg/REEUs3CPND",
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="suggestions",
        description="Got a Suggestion? Send it here!",
    )
    async def _suggest(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)

        log.debug(f"Creating button for new github issue")
        suggestion_button = discord.ui.Button(
            label="Suggest Here! (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot/issues/new",
        )
        log.debug(f"Created Button")

        await ctx.respond(
            content='Hey!\nPlease click the link below to open an "issue" where you can send your suggestion. Please put a short title and expand in the description and NottCurious will get back to you shortly',
            view=ViewAdder([suggestion_button]),
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="reloadall",
        description="Reloads all cogs",
        hidden=True,
    )
    @permissions.is_owner()
    async def _reload_all(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                log.info(f"Reloading cogs.{filename[:-3]}")
                self.client.unload_extension(f"cogs.{filename[:-3]}")
                self.client.load_extension(f"cogs.{filename[:-3]}")
        await ctx.respond("Reloaded all cogs")

    @commands.slash_command(guild_ids=[876042400005505066], name="testpagination")
    @permissions.is_owner()
    async def _test(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
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

    @commands.slash_command(guild_ids=[876042400005505066], name="testconfirm")
    @permissions.is_owner()
    async def _test_confirm(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        # Creating the Confirmer
        my_confirmer = Confirmer()
        my_confirmer.change_cancel_button("Cancel Me Senpai")
        my_confirmer.change_confirm_button("Confirm Me pls")
        await ctx.respond("Do You Want to Continue", view=my_confirmer)

        # Awaiting a response
        await my_confirmer.wait()

        await ctx.send(my_confirmer.value)

    @commands.slash_command(guild_ids=[876042400005505066], name="causeerror")
    @permissions.is_owner()
    async def _cause_error(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        # await ctx.send("This is a test error")
        raise discord.ApplicationCommandError("This is a test error")


def setup(client: discord.Bot):
    client.add_cog(Generic(client))
