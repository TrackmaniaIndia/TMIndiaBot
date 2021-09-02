from re import L

from discord.ext.commands.core import after_invoke, before_invoke
from functions.tm_username_functions.username_functions import (
    check_trackmania_username,
    remove_trackmania_username,
)
import discord
from discord.ext import commands
import logging
from datetime import datetime
from dotenv import load_dotenv

import functions.logging.convert_logging as convert_logging
from functions.logging.usage import record_usage, finish_usage
from functions.tm_username_functions.username_functions import (
    store_trackmania_username,
    check_trackmania_username,
    remove_trackmania_username,
)
from functions.other_functions.get_data import get_version

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

version = get_version()

DEFAULT_PREFIX = "*"


class UsernameCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="storeusername",
        aliases=["setusername", "setname", "setuser"],
        help="Set your trackmania username to reduce amount of typing needed while using TM2020 commands",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def store_username(self, ctx: commands.Context, username: str):
        log.debug(f"Storing {username} for {ctx.author.name}. ID: {ctx.author.id}")
        store_trackmania_username(ctx, username)
        log.debug(f"Stored Username for {ctx.author.name}")

        #
        # Make sure to ping api and check for valid username
        #

        log.debug(f"Sending Success Message")
        await ctx.send(
            embed=discord.Embed(
                title="SUCCESS!", color=discord.Colour.green()
            ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url)
        )
        log.debug(f"Sent Success Message")

    @commands.command(
        name="checkusername",
        aliases=["usernamecheck", "namecheck", "checkname", "checkuser", "usercheck"],
        help="Checks if you have a username stored with the bot",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def check_username(self, ctx: commands.Context):
        if check_trackmania_username(ctx):
            log.debug(f"Username in json file")
            await ctx.send(
                embed=discord.Embed(
                    title="Your Username Exists", colour=discord.Colour.green()
                ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url)
            )
        else:
            log.debug(f"Username not in json file")
            await ctx.send(
                embed=discord.Embed(
                    title="Your Username does not Exist", colour=discord.Colour.red()
                ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url)
            )

    @commands.command(
        name="removeusername",
        aliases=["usernameremove", "userremove", "nameremove"],
        help="Removes your username from the bot",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def remove_username(self, ctx: commands.Context):
        if not check_trackmania_username(ctx):
            log.debug(f"User does not exist in file")
            await ctx.send(
                embed=discord.Embed(
                    title="User does not exist", colour=discord.Colour.red()
                ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url)
            )
            return

        log.debug(f"Removing Trackmania Username")
        remove_trackmania_username(ctx)
        log.debug(f"Removed Trackmania Username")

        await ctx.send(
            embed=discord.Embed(title="SUCCESS!!", colour=discord.Colour.green())
        )


def setup(client):
    client.add_cog(UsernameCommands(client))
