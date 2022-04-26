import discord
from discord import ApplicationContext
from discord.commands import Option, permissions
from discord.ext import commands

import bot.utils.commons as commons
import bot.utils.quote as quote_functions
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class SaveQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="quote",
        description="Saves a Quote, Only Usable by Mods",
        default_permissions=False,
    )
    @commands.has_permissions(manage_messages=True)
    async def _save_quote(
        self,
        ctx: ApplicationContext,
        *,
        message: Option(str, "Message to Quote", required=True),
        author: Option(str, "The author of the message", required=True),
        message_link: Option(
            str, "The Link to the Message you want to quote", required=True
        ),
    ):
        log_command(ctx, "save_quote")

        log.info(f"Saving {message} by {author} from guild {ctx.guild.name}")

        log.debug("Deferring Response")
        await ctx.defer()
        log.debug("Deferred Response")

        if ctx.author.id == 901407301175484447:
            log.info(
                "%s tried to quote a message by t901407301175484447he bot",
                ctx.author.name,
            )
            await ctx.respond("Cannot quote a message by the Bot")
            return
        if ctx.message.content == "":
            log.info("%s tried to quote an empty message", ctx.author.name)
            await ctx.respond("Cannot quote an empty string")
            return

        quote_functions.save(message, author, message_link, ctx.guild.id)

        embed = create_embed(
            title=":white_check_mark: Saved",
            description=f'Saved "{message}" by {author} with [Jump!]({message_link})',
            color=commons.get_random_color(),
        )

        await ctx.send_followup(embed=embed)

    @commands.message_command(name="Quote Message")
    @commands.has_permissions(manage_messages=True)
    async def _save_quote_message_cmd(
        self,
        ctx: ApplicationContext,
        message: discord.Message,
    ):
        log_command(ctx, "save_quote_message")

        message = message
        author = message.author
        message_link = message.jump_url
        guild_id = ctx.guild.id

        log.debug("Deferring Response")
        await ctx.defer()
        log.debug("Deferred Response")

        if ctx.author.id == 901407301175484447:
            log.info(
                "%s tried to quote a message by t901407301175484447he bot",
                ctx.author.name,
            )
            await ctx.respond("Cannot quote a message by the Bot")
            return
        if message.content == "":
            log.info("%s tried to quote an empty message", ctx.author.name)
            await ctx.respond("Cannot quote an empty string")
            return

        quote_functions.save(message.content, f"{author.name}", message_link, guild_id)

        embed = create_embed(
            title=":white_check_mark: Saved",
            description=f'Saved "{message.content}" by {author.name} with [Jump!]({message_link})',
        )

        await ctx.send_followup(embed=embed)


def setup(bot: Bot):
    """Add the SaveQuote cog"""
    bot.add_cog(SaveQuote(bot))
