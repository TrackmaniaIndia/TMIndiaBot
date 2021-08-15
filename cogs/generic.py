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
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level, version = '', '', ''

with open("./config.json") as file:
    config = json.load(file)

    log_level = config['log_level']
    discord_log_level = config['discord_log_level']
    version = config['bot_version']

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)

DEFAULT_PREFIX = "*"

async def record_usage(self, ctx):
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )

    logcheck = ''

    with open('./config.json') as file:
        data = json.load(file)
        logcheck = data['log_function_usage']

    if not logcheck:
        log.debug(f'Logcheck is False, Returning')
        return
    log.debug(f'Logcheck is True, Sending Message')

    log.debug(f'Sending Message to Error Channel')
    channel = self.client.get_channel(876442289382248468)
    
    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":clapper: Command Used", color=0x23FFFF)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)
    log.debug(f"Created Embed")

    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


async def finish_usage(self, ctx):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")

    logcheck = ''

    with open('./config.json') as file:
        data = json.load(file)
        logcheck = data['log_function_usage']

    if not logcheck:
        log.debug(f'Logcheck is False, Returning')
        return
    log.debug(f'Logcheck is True, Sending Message')

    log.debug(f'Sending Message to Error Channel')
    channel = self.client.get_channel(876442289382248468)
    
    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":medal: Command Finished", color=0x00FF00)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)
    log.debug(f"Created Embed")

    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


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

        channel = self.client.get_channel(876335103146623016)
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
        prefixes[str(ctx.guild.id)] = [prefix, DEFAULT_PREFIX]
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
