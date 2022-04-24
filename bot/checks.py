from discord.ext import commands
from discord.ext.commands import Context

from bot import constants


class TMIndiaOnly(commands.CheckFailure):
    pass


def predicate(ctx: Context):
    if ctx.guild and (
        ctx.guild.id == constants.Guild.tmi_server
        or ctx.guild.id == constants.Guild.testing_server
    ):
        return True
    raise TMIndiaOnly("This command can only be used in the Trackmania India server")


tmi_only = commands.check(predicate)
