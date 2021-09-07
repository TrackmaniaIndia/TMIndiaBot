from functions.tm_username_functions.username_functions import (
    check_trackmania_username,
    remove_trackmania_username,
)
from os import stat
import discord
from discord import activity
from discord.ext import commands, tasks
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from itertools import cycle

import functions.logging.convert_logging as convert_logging
import functions.common_functions.common_functions as common_functions
import functions.cog_helpers.generic_functions
from functions.logging.usage import record_usage, finish_usage
from functions.task_helpers.pingapi import ping_api
from functions.other_functions.get_data import get_version

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

version = get_version()

DEFAULT_PREFIX = "*"


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        aliases=["purge"],
        help="Clears Given Amount of Messages from Channel",
        brief="Clears Messages",
        enabled=False,
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_any_role(
        "moderator", "admin", "administrator", "mod", "bot developer"
    )
    async def clear(self, ctx: commands.Context, amount: int) -> None:
        await ctx.channel.purge(limit=amount)
        log.debug(f"Cleared {amount} messages")

        log.debug(f"Creating and Sending Embed")
        await ctx.send(
            embed=discord.Embed(
                title=f"Cleared {amount} message(s) from {ctx.channel}",
                color=discord.Colour.red(),
            ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url),
            delete_after=4,
        )
        log.debug(f"Sent Embed")

    @commands.command(help="Kicks Given Member from the Server", enabled=False)
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_any_role(
        "administrator", "admin", "moderator", "mod", "bot developer"
    )
    async def kick(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        await member.kick(reason=reason)
        log.debug(f"Kicked {member}")

        log.debug(f"Creating and Sending Embed")
        await ctx.send(
            embed=discord.Embed(
                title=f"Kicked {member}", color=discord.Colour.red()
            ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url),
            delete_after=4,
        )
        log.debug(f"Sent Embed")

    @commands.command(help="Bans Given Member from the Server", enabled=False)
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_any_role("administrator", "admin", "bot developer")
    async def ban(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        await member.ban(reason=reason)
        log.debug(f"Banned {member}")

        log.debug(f"Creating Embed")
        embed = discord.Embed(
            title=f"Banned {member}", color=discord.Colour.red()
        ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url)
        log.debug(f"Created Embed")

        log.debug(f"Sending Embed")
        await ctx.send(embed=embed, delete_after=4)
        log.debug(f"Sent Embed")

    @commands.command(help="Unbans Given Member from the Server", enabled=False)
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_any_role(
        "administrator", "admin", "moderator", "mod", "bot developer"
    )
    async def unban(self, ctx: commands.Context, *, member: str):
        log.debug("Requesting Ban List")
        banned_users = await ctx.guild.bans()
        log.debug("Received Ban List")

        log.debug("Splitting Given Username")
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            log.debug(f"Checking {user} for {ctx.guild}")
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                log.debug("User Found in Ban List")

                await ctx.guild.unban(user)

                log.debug(f"[Successful] - Creating Embed")
                embed = discord.Embed(
                    title=f"Unbanned {user}", color=discord.Colour.red()
                ).set_footer(text=datetime.utcnow(), icon_url=ctx.author.avatar_url)
                log.debug(f"[Successful] - Created Embed")

                log.debug(f"[Successful] - Sending Embed")
                await ctx.send(embed=embed, delete_after=4)
                log.debug(f"[Successful] - Sent Embed")
                return

        log.critical(f"User: {member} is not found in Ban List")

        log.debug(f"[Unsuccessful] - Creating Embed")
        embed = discord.Embed(
            title=f"User Not Found in Ban List", color=discord.Colour.red()
        )
        log.debug(f"[Unsuccessful] - Created Embed")

        log.debug(f"[Unsuccessful] - Sending Embed")
        await ctx.send(embed=embed, delete_after=4)
        log.debug(f"[Unsuccessful] - Sent Embed")

    # Errors
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Enter the Amount of Messages to Delete")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have a required role")
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Disabled Command")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You Cannot Kick Someone With a Higher Role Priority")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Tag a Person To Kick")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have a required role")
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Disabled Command")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You Cannot Ban Someone With a Higher Role Priority")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Tag a Person To Ban")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have a required role")
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Disabled Command")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You Cannot Ban Someone With a Higher Role Priority")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Tag a Person To Ban")
        if isinstance(error, ValueError):
            await ctx.send("Invalid Name Format")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You do not have a required role")
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Disabled Command")


def setup(client):
    client.add_cog(Moderation(client))
