import util.trackmania.trackmania_username.retrieving as ret
import util.trackmania.trackmania_username.storing as stor
import discord
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from discord.commands.commands import Option
from discord.commands import permissions
from discord.ext import commands
from util.constants import guild_ids
from util.trackmania.tm2020.player import get_player_id
from util.discord.confirmation import Confirmer

log = convert_logging.get_logging()


class UsernameSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        guild_ids=guild_ids,
        name="storeusername",
        description="Stores Username in JSON File for Future Use and Speed",
    )
    async def _store_username(
        self,
        ctx: commands.Context,
        username: Option(str, "Your Trackmania2020 Username", required=True),
    ):
        log.debug(f"Checking Username")
        if not stor.check_valid_trackmania_username(username):
            log.debug(f"Username not found")
            embed = ezembed.create_embed(
                title=":negative_squared_cross_mark: Username not Found or does not exist.",
                color=discord.Colour.red(),
            )
            await ctx.respond(embed=embed)
            return None
        log.debug(f"User Exists, Continuing")
        
        log.debug(f'Creating a Confirmation Prompt')
        confirm_add_username = Confirmer()
        
        log.debug(f'Changing Button Labels')
        confirm_add_username.change_cancel_button(label='No, Do NOT Add This Username')
        confirm_add_username.change_confirm_button(label='Yes, Add this Username')
        log.debug(f'Changed the Button Labels')
        
        log.debug(f'Sending Confirmation Prompt')
        message = await ctx.respond(embed=ezembed.create_embed(title='Is This Your Username?', description=f'Username: {username}', color=discord.Colour.red()), view=confirm_add_username)
        log.debug(f'Sent Confirmation Prompt')
        log.debug(f'Awaiting a Response from User')
        await confirm_add_username.wait()
        log.debug(f'Response Received')
        
        log.debug(f'Deleting Message')
        await message.delete_original_message()
        log.debug(f'Deleted Message')
        
        if confirm_add_username.value == False:
            log.debug(f'User does not want his username added')
            return
        
        log.debug(f'User wants his username added')

        log.debug(f"Storing {username} for {ctx.author.name}. ID: {ctx.author.id}")
        stor.store_trackmania_username(ctx.author.id, username)
        log.debug(f"Stored Username for {ctx.author.name}")

        log.debug(f"Sending Success Message")
        embed = ezembed.create_embed(
            title=":white_check_mark: Successfully Stored Username",
            description=f'Requestor: {ctx.author.name}',
            color=discord.Color.green(),
        )
        await ctx.respond(embed=embed)
        log.debug(f"Sent Success Message")

    @commands.slash_command(
        guild_ids=guild_ids,
        name="checkusername",
        description="Checks if your username is in the file",
    )
    async def _check_username(self, ctx: commands.Context):
        if ret.check_discord_id_in_file(str(ctx.author.id)):
            log.debug(f"Username in json file")
            embed = ezembed.create_embed(
                title=":white_check_mark: Your Username Exists",
                color=discord.Colour.green(),
            )
            await ctx.respond(embed=embed)
        else:
            log.debug(f"Username not in json file")
            embed = ezembed.create_embed(
                title=":negative_squared_cross_mark: Your Username does not Exist",
                color=discord.Colour.red(),
            )
            await ctx.respond(embed=embed)

    @commands.slash_command(
        guild_ids=guild_ids,
        name="removeusername",
        description="Removes your username from the file if present",
    )
    async def _remove_username(self, ctx: commands.Context):
        # Add Double Check
        log.debug(f'Creating a Confirmation Prompt')
        confirm_remove_username = Confirmer()
        
        log.debug(f'Changing Button Labels')
        confirm_remove_username.change_cancel_button(label='No, Do NOT remove my username')
        confirm_remove_username.change_confirm_button(label='Yes, Remove my username')
        log.debug(f'Changed the Button Labels')
        
        log.debug(f'Sending Confirmation Prompt')
        message = await ctx.respond(embed=ezembed.create_embed(title='Are you sure you want to delete your username from the database?', color=discord.Colour.red()), view=confirm_remove_username)
        log.debug(f'Sent Confirmation Prompt')
        log.debug(f'Awaiting a Response from User')
        await confirm_remove_username.wait()
        log.debug(f'Response Received')
        
        log.debug(f'Deleting Message')
        await message.delete_original_message()
        log.debug(f'Deleted Message')
        
        if confirm_remove_username.value == False:
            log.debug(f'User does not want his username removed')
            return
        
        log.debug(f'User wants his username removed')
        
        if not ret.check_discord_id_in_file(str(ctx.author.id)):
            log.debug(f"User does not exist in file")
            embed = ezembed.create_embed(
                title=":negative_squared_cross_mark: User does not exist",
                color=discord.Colour.red(),
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return

        log.debug(f"Removing Trackmania Username")
        stor.remove_trackmania_username(ctx.author.id)
        log.debug(f"Removed Trackmania Username")
        embed = ezembed.create_embed(
            title=":white_check_mark: Successfully Removed Your Username from the File.",
            description=f'Requester: {ctx.author.name}',
            color=discord.Colour.green(),
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(
        guild_ids=guild_ids,
        name="getid",
        description="Gets the Trackmania ID of A Player",
    )
    @permissions.is_owner()
    async def _get_id(
        self,
        ctx: commands.Context,
        username: Option(str, "The Trackmania2020 Username", required=True),
    ):
        log.info(f"Getting Data of {username}")
        embed = ezembed.create_embed(
            title="ID",
            description=get_player_id(username),
            color=discord.Color.random(),
        )
        log.debug(f"Got Data and Created Embed, Sending")
        # await ctx.respond(get_player_id(username))
        await ctx.respond(embed=embed, ephemeral=True)
        log.debug(f"Sent Embed")


def setup(client):
    client.add_cog(UsernameSlash(client))
