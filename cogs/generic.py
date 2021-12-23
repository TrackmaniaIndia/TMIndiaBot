"""Generic Functions of the Bot"""

import os
import discord
from discord.ext import commands
from discord.commands import permissions

from util.logging import convert_logging
import util.discord.easy_embed as ezembed

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
    def __init__(self, client: commands.Bot):
        self.client = client
        self.version = get_version()

        log.info("cogs.generic has finished initializing")

    @classmethod
    @commands.slash_command(
        name="ping",
        description="Get ping of bot in ms",
    )
    async def _ping(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        await ctx.respond(f"Pong! {round(cls.client.latency * 1000, 2)}ms")

    @classmethod
    @commands.slash_command(name="version", description="Gives the current bot version")
    async def _version(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        await ctx.respond(f"Bot Version is {cls.version}", ephemeral=True)

    @classmethod
    @commands.slash_command(
        name="sourcecode",
        description="Sends you a link to the bot source code on github",
    )
    async def _source(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        log.debug("Creating Button for Source Code")
        source_code_button = discord.ui.Button(
            label="Source Code (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot",
        )
        log.debug("Created Button for Source Code, Sending a message")
        await ctx.respond(
            content="Hey!\nHere is the source code. The bot is open source and licensed under the MIT License. It is currently developed and maintained by NottCurious and Artifex.\nAll Issues/Feature Requests/Bug Reports and Pull Requests are welcome and appreciated!",
            view=ViewAdder([source_code_button]),
        )

    @classmethod
    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="invitelink",
        description="Gives you an invite link for the Trackmania India discord server",
    )
    async def _server_invite(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        await ctx.respond(
            "Here is an invite for you to share with your friends\nhttps://discord.gg/yvgFYsTKNr",
            ephemeral=True,
        )

    @classmethod
    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="halloffame",
        description="Gives you the link for the TMI Hall of Fame",
    )
    async def _link_to_hall_of_fame(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        log.debug("Creating Button for Hall of Fame")
        hall_of_fame_button = discord.ui.Button(
            label="TMI Hall of Fame (Google Sheets)",
            style=discord.ButtonStyle.url,
            url="https://tinyurl.com/TMIndiaLB",
        )
        log.debug("Created Button for Hall of Fame, Sending a message")
        await ctx.respond(
            "Please click the button to be redirected to the hall of fame",
            view=ViewAdder([hall_of_fame_button]),
            ephemeral=True,
        )

    @classmethod
    @commands.slash_command(
        name="nextproject",
        description="A Github link to the next project, has planned, in progress and finished features.",
    )
    async def _next_project(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        log.debug("Creating Button for Next Project")
        next_project_button = discord.ui.Button(
            label="Next Project - v1.6.1 (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot/projects/6",
        )
        await ctx.respond(
            "Here is the link to the next project",
            view=ViewAdder([next_project_button]),
            ephemeral=True,
        )

    @classmethod
    @commands.slash_command(
        name="invitebot",
        description="Give an invite link for the bot",
    )
    async def _invite_bot(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)

        await ctx.respond(
            embed=ezembed.create_embed(
                title="Bot Invite",
                description="Hey! Thanks for your interest in TMI Bot. This bot may have lots of bugs and issues to be ironed out. If the bot suddenly stops working please contact NottCurious#4351 immediately.\n\n[Click Here to Invite the Bot!](https://discord.com/api/oauth2/authorize?client_id=901407301175484447&permissions=534925274176&scope=bot%20applications.commands)",
            ),
            ephemeral=True,
        )

    @classmethod
    @commands.slash_command(
        name="testingserver",
        description="Get an invite to the TMI Bot Testing Server",
    )
    async def _testing_server_invite(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)

        await ctx.respond(
            "Here is an invite to the testing server\nhttps://discord.gg/REEUs3CPND",
            ephemeral=True,
        )

    @classmethod
    @commands.slash_command(
        name="suggest",
        description="Got a Suggestion? Send it here!",
    )
    async def _suggest(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)

        log.debug("Creating button for new github issue")
        suggestion_button = discord.ui.Button(
            label="Suggest Here! (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot/issues/new",
        )
        log.debug("Created Button")

        await ctx.respond(
            content='Hey!\nPlease click the link below to open an "issue" where you can send your suggestion. Please put a short title and expand in the description and NottCurious will get back to you shortly',
            view=ViewAdder([suggestion_button]),
            ephemeral=True,
        )

    @classmethod
    @commands.slash_command(
        name="commandlist",
        description="Gives you a link to the command list",
    )
    async def _command_list(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        log.debug("Creating Button for Command List")
        command_list_button = discord.ui.Button(
            label="Command List (Github)",
            style=discord.ButtonStyle.url,
            url="https://gist.github.com/NottCurious/f9b618bbfd8aa133d0de2655b94bfca6",
        )

        await ctx.respond(
            content="Here is the command list for this bot!",
            view=ViewAdder([command_list_button]),
        )

    @classmethod
    @commands.slash_command(
        guild_ids=[GUILD_IDS[0]],
        name="reloadall",
        description="Reloads all cogs",
        hidden=True,
    )
    @permissions.is_owner()
    async def _reload_all(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                log.info(f"Reloading cogs.{filename[:-3]}")
                cls.client.unload_extension(f"cogs.{filename[:-3]}")
                cls.client.load_extension(f"cogs.{filename[:-3]}")
        await ctx.respond("Reloaded all cogs")


def setup(client: discord.Bot):
    client.add_cog(Generic(client))
