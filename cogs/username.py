import discord
from discord.commands.commands import Option
from discord.commands import permissions
from discord.ext import commands

import util.trackmania.trackmania_username.retrieving as ret
import util.trackmania.trackmania_username.storing as stor
from util.logging import convert_logging
import util.discord.easy_embed as ezembed
from util.trackmania.tm2020.player import get_player_id
from util.discord.confirmation import Confirmer
from util.logging.command_log import log_command

# Creating Logger
log = convert_logging.get_logging()


class Username(commands.Cog):
    def __init__(self, client):
        self.client = client
        log.info("cogs.username has finished initializing")

    @classmethod
    @commands.slash_command(
        name="storeusername",
        description="Stores Username in JSON File for Future Use and Speed",
    )
    async def _store_username(
        cls,
        ctx: commands.Context,
        username: Option(str, "Your Trackmania2020 Username", required=True),
    ):
        log_command(ctx, ctx.command.name)
        # Storing Username
        if username.lower() == "kaizer_tm":
            # For some reason, kaizer's username totally breaks the bot and causes it to exit. This is just a temporary
            # if statement to prevent that from happening. It might be something wrong with the API.
            await ctx.respond(
                "For some unknown reason, this username breaks the bot completely. So it cannot be saved"
            )
            return

        # Checking if the Username is Valid
        log.debug("Checking Username")
        if not stor.check_valid_trackmania_username(username):
            log.debug("Username not found")
            embed = ezembed.create_embed(
                title=":negative_squared_cross_mark: Username not Found or does not exist.",
                color=0xFF0000,
            )
            await ctx.respond(embed=embed)
            return None
        log.debug("User Exists, Continuing")

        # Creating a Confirmation Prompt
        log.debug("Creating a Confirmation Prompt")
        confirm_add_username = Confirmer()

        # Changing Button Labels
        log.debug("Changing Button Labels")
        confirm_add_username.change_cancel_button(label="No, Do NOT Add This Username")
        confirm_add_username.change_confirm_button(label="Yes, Add this Username")
        log.debug("Changed the Button Labels")

        log.debug("Sending Confirmation Prompt")
        message = await ctx.respond(
            embed=ezembed.create_embed(
                title="Is This Your Username?",
                description=f"Username: {username}",
                color=0xFF0000,
            ),
            view=confirm_add_username,
        )

        # Waiting for confirmation response
        log.debug("Sent Confirmation Prompt")
        log.debug("Awaiting a Response from User")
        await confirm_add_username.wait()
        log.debug("Response Received")

        # Deleting the confirmation message
        log.debug("Deleting Message")
        await message.delete_original_message()
        log.debug("Deleted Message")

        # Checking if the user responded negatively to the confirmation prompt
        if confirm_add_username.value is False:
            log.debug("User does not want his username added")
            return

        log.debug("User wants his username added")

        # Storing the username
        log.debug(f"Storing {username} for {ctx.author.name}. ID: {ctx.author.id}")
        stor.store_trackmania_username(ctx.author.id, username)
        log.debug(f"Stored Username for {ctx.author.name}")

        log.debug("Sending Success Message")
        embed = ezembed.create_embed(
            title=":white_check_mark: Successfully Stored Username",
            description=f"Requestor: {ctx.author.name}",
            color=discord.Color.green(),
        )
        await ctx.respond(embed=embed)
        log.debug("Sent Success Message")

    @classmethod
    @commands.slash_command(
        name="checkusername",
        description="Checks if your username is stored in the file",
    )
    async def _check_username(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        # Checking if the given username is stored in the JSON file
        if ret.check_discord_id_in_file(str(ctx.author.id)):
            log.debug("Username in json file")
            embed = ezembed.create_embed(
                title=":white_check_mark: Your Username Exists",
                color=discord.Colour.green(),
            )
            await ctx.respond(embed=embed)
        else:
            log.debug("Username not in json file")
            embed = ezembed.create_embed(
                title=":negative_squared_cross_mark: Your Username does not Exist",
                color=0xFF0000,
            )
            await ctx.respond(embed=embed)

    @classmethod
    @commands.slash_command(
        name="removeusername",
        description="Removes your username from the file if present",
    )
    async def _remove_username(cls, ctx: commands.Context):
        log_command(ctx, ctx.command.name)
        # Removes a username from the JSON file
        # Confirmation prompt to check if the user really wants to remove their username

        # Creating the Confirmation Prompt
        log.debug("Creating a Confirmation Prompt")
        confirm_remove_username = Confirmer()

        # Changing the Button Labels
        log.debug("Changing Button Labels")
        confirm_remove_username.change_cancel_button(
            label="No, Do NOT remove my username"
        )
        confirm_remove_username.change_confirm_button(label="Yes, Remove my username")
        log.debug("Changed the Button Labels")

        # Sending the Confirmation Prompt
        log.debug("Sending Confirmation Prompt")
        message = await ctx.respond(
            embed=ezembed.create_embed(
                title="Are you sure you want to delete your username from the database?",
                color=0xFF0000,
            ),
            view=confirm_remove_username,
        )
        log.debug("Sent Confirmation Prompt")

        # Awaiting a response to the confirmation prompt from the user
        log.debug("Awaiting a Response from User")
        await confirm_remove_username.wait()
        log.debug("Response Received")

        # Deleting the confirmation message
        log.debug("Deleting Message")
        await message.delete_original_message()
        log.debug("Deleted Message")

        # Checking if the user really wanted his username removed
        if confirm_remove_username.value is False:
            log.debug("User does not want his username removed")
            return

        log.debug("User wants his username removed")

        # Checking if the username is already stored in the file
        if not ret.check_discord_id_in_file(str(ctx.author.id)):
            log.debug("User does not exist in file")
            embed = ezembed.create_embed(
                title=":negative_squared_cross_mark: User does not exist",
                color=0xFF0000,
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return

        # Removing the Trackmania Username from the JSON File
        log.debug("Removing Trackmania Username")
        stor.remove_trackmania_username(ctx.author.id)
        log.debug("Removed Trackmania Username")
        embed = ezembed.create_embed(
            title=":white_check_mark: Successfully Removed Your Username from the File.",
            description=f"Requester: {ctx.author.name}",
            color=discord.Colour.green(),
        )
        await ctx.respond(embed=embed)

    @classmethod
    @commands.slash_command(
        name="getid",
        description="Gets the Trackmania ID of A Player",
    )
    @permissions.is_owner()
    async def _get_id(
        cls,
        ctx: commands.Context,
        username: Option(str, "The Trackmania2020 Username", required=True),
    ):
        log_command(ctx, ctx.command.name)
        log.info(f"Getting Data of {username}")
        embed = ezembed.create_embed(
            title="ID",
            description=get_player_id(username),
            color=discord.Color.random(),
        )
        log.debug("Got Data and Created Embed, Sending")
        # await ctx.respond(get_player_id(username))
        await ctx.respond(embed=embed, ephemeral=True)
        log.debug("Sent Embed")


def setup(client: discord.Bot):
    client.add_cog(Username(client))
