import discord
from discord.ext import commands
import json
import logging
import os
from dotenv import load_dotenv

try:
    import cogs.convertLogging as cl
    import cogs.commonFunctions as cf
except:
    import commonFunctions as cf
    import convertLogging as cl

load_dotenv()
log_level = os.getenv("LOG_LEVEL")
version = os.getenv("VERSION")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)


async def record_usage(self, ctx):
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )
    # embed = discord.Embed(
    #     title=f"We're Working on {ctx.command}, Please Wait...",
    #     color=cf.getRandomColor(),
    # )

    # await ctx.send(embed=embed, delete_after=0.5)


async def finish_usage(self, ctx):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")


# Generic Class
class Generic(commands.Cog, description="Generic Functions"):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Version: {version}! Online and Ready"),
        )
        log.critical("Bot Logged In")

        channel = self.client.get_channel(876043157303861299)
        await channel.send(f"Bot is Ready, Version: {version}")

    # Commands
    @commands.command(
        aliases=["latency", "pong", "connection"],
        help="Shows the Ping/Latency of the Bot in milliseconds.",
        brief="Shows Bot Ping.",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def ping(self, ctx):
        await ctx.send("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.command(help="Changes Prefix to Given prefix", brief="Changes Prefix")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str):
        log.info(f"Changing Prefix in {ctx.guild}")

        with open("prefixes.json", "r") as file:
            log.debug("Opening Prefixes JSON")
            prefixes = json.load(file)
            file.close()

        log.debug(f"Changing Prefix")
        prefixes[str(ctx.guild.id)] = [prefix, "*"]
        log.debug(f"Changed Prefix")

        with open("prefixes.json", "w") as file:
            log.debug("Dumping Prefixes to File")
            json.dump(prefixes, file, indent=4)
            file.close()

        await ctx.send("Prefix Changed to {}".format(prefix))

    @commands.command(help="Displays Bot Version", brief="Bot Version")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def version(self, ctx):
        from dotenv import load_dotenv
        import os

        load_dotenv()
        version = os.getenv("BOTVERSION")

        await ctx.send(f"Bot Version is {version}")

    @commands.command()
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def causeError(self, ctx):
        await ctx.send("Causing error")

        raise commands.CommandError(message='Caused error')

    # Error Management
    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Prefix Not Given")

            emb = discord.Embed(
                title=":warning: Prefix not given",
                description="Usage: prefix <new-prefix>\nExample: !prefix $",
                color=cf.getRandomColor(),
            )
            await ctx.send(embed=emb)

        if isinstance(error, commands.MissingPermissions):
            log.error("Caller Doesn't Have Required Permissions")
            emb = discord.Embed(
                title=":warning: You dont have the required permissions: Administrator",
                color=cf.getRandomColor(),
            )
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(Generic(client))
