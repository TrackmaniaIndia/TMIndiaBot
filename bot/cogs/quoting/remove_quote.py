import json

import discord
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands

import bot.utils.commons as commons
import bot.utils.quote as quote_functions
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed
from bot.utils.moderation import send_in_mod_logs

log = get_logger(__name__)


class RemoveQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="remove-quote",
        description="Removes the quote from the server's guild file",
    )
    @commands.has_permissions(manage_messages=True)
    async def _remove_quote(
        self,
        ctx: ApplicationContext,
        number: Option(
            SlashCommandOptionType.integer,
            "The number of the quote you want to remove",
            required=True,
        ),
    ):
        log_command(ctx, "remove-quote")

        await ctx.defer()

        log.info("Removing Quote #%s from %s", number, ctx.guild.name)
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/quotes.json",
            "r",
            encoding="UTF-8",
        ) as file:
            aquotes = json.load(file)

        log.debug("Popping the quote.")
        try:
            aquotes["quotes"].pop(number - 1)
        except IndexError:
            await ctx.respond("Invalid Number Given.", ephemeral=True)
            return

        log.debug("Fixing numbers.")
        for i, _ in enumerate(aquotes["quotes"]):
            aquotes["quotes"][i]["Number"] = i + 1

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/quotes.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(aquotes, file, indent=4)

        await send_in_mod_logs(
            self.bot,
            ctx.guild.id,
            msg=f"Quote #{number} has been removed by {ctx.author.mention}.",
        )

        await ctx.respond("Successfully Removed!", ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(RemoveQuote(bot))
