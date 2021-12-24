import discord
from discord.commands import permissions
from discord.ext import commands
from discord.commands.commands import Option
from util.logging import convert_logging
import util.quoting.quote as quote_functions
import util.discord.easy_embed as ezembed

from util.logging.command_log import log_command

# Creating a logger
log = convert_logging.get_logging()


class Quote(commands.Cog, description="Quoting Functions"):
    def __init__(self, client):
        self.client = client
        log.info("cogs.quote has finished initializing")

    @commands.slash_command(
        name="quote",
        description="Saves a Quote, Only Usable by Mods",
        default_permission=False,
    )
    @permissions.has_any_role(
        "Moderator",
        "Admin",
        "Bot Developer",
        "admin",
    )
    async def _quote(
        self,
        ctx: commands.Context,
        *,
        message: Option(
            str,
            "Message to quote",
            required=True,
        ),
        author: Option(
            str,
            "Author who wrote the above message",
            required=True,
        ),
        message_link: Option(
            str,
            "The link to the message",
            required=True,
        ),
    ):
        log_command(ctx, ctx.command.name)
        # Saves a quote given in the parameters
        log.debug(f"Saving {message} by {author} from guild {ctx.guild.id}")

        log.debug("Deferring Response")
        await ctx.defer()
        log.debug("Deferred Response")

        # Saving the Quote
        quote_functions.save(message, author, message_link, ctx.guild.id)
        embed = ezembed.create_embed(
            title=":white_check_mark: Saved",
            description=f'Saved "{message}" by {author} with [Jump!]({message_link})',
            color=discord.Colour.green(),
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name="randquote", description="Shows a random saved quote")
    async def _rand_quote(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        # Gets a random quote from the file
        # Random Number Generator is not very consistent, need to work on an alternative

        # Getting the random quote in a dictionary
        log.debug("Getting Random Quote")
        rand_quote = quote_functions.get_random_quote_dict(ctx.guild.id)

        # Converting the Quote Dictionary into a discord.Embed
        log.debug("Getting Quote Embed")
        embed = quote_functions.quote_dict_to_embed(rand_quote)

        # Sending the Quote
        log.debug("Sending Random Quote")
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="lastquote",
        description="Displays the last quote saved",
    )
    async def _last_quote(self, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        # This command sends the last quote that was saved
        log.debug("Getting the Last Quote Saved")
        quote_embed = quote_functions.get_last_quote(ctx.guild.id)

        await ctx.respond(embed=quote_embed)


def setup(client: discord.Bot):
    client.add_cog(Quote(client))
