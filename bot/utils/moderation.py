import json

from discord import ApplicationContext, Embed

from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


async def send_in_mod_logs(
    bot: Bot, guild_id: int | ApplicationContext, *, msg: str | Embed
) -> None:
    """Sends a message in the given mod logs channel of the server.

    Args:
        guild_id (int): The ID of the guild.
        msg (str): The message to send.
    """
    if isinstance(guild_id, ApplicationContext):
        guild_id = guild_id.guild.id

    log.debug(f"Sending {msg} to mod-logs channel of {guild_id}.")
    with open(
        f"./bot/resources/guild_data/{guild_id}/config.json", "r", encoding="UTF-8"
    ) as file:
        config_data = json.load(file)

    mod_logs_id = config_data.get("mod_logs_channel", 0)

    if mod_logs_id == 0:
        log.debug("Mod Logs channel is not set for the server.")
        return

    mod_logs_channel = await bot.fetch_channel(mod_logs_id)

    try:
        if isinstance(msg, Embed):
            await mod_logs_channel.send(embed=msg)
        else:
            await mod_logs_channel.send(content=msg)
    except Exception as e:
        log.error("Failed to send a message to mod-logs channel")
