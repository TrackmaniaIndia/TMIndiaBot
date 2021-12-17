import discord
import requests

import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

import util.trackmania.tm2020.cotd.util as cotd_util

# Setting up Logging
log = convert_logging.get_logging()


def get_cotd_data(user_id: str, username: str) -> discord.Embed:
    log.debug(f"Requesting COTD Data for {user_id}")
    cotd_data = requests.get(
        "http://localhost:3000/tm2020/player/{}/cotd".format(user_id)
    ).json()

    log.debug(f"Parsing Best Rank Overall Data")
    best_rank_overall = cotd_util._get_best_rank_overall(cotd_data)
    best_div_overall = cotd_util._get_best_div_overall(cotd_data)
    best_div_rank_overall = cotd_util._get_best_div_rank_overall(cotd_data)
    log.debug(f"Parsed Best Rank Overall Data")

    log.debug(f"Parsing Best Rank Primary Data")
    best_rank_primary = cotd_util._get_best_rank_primary(cotd_data)
    best_div_primary = cotd_util._get_best_div_primary(cotd_data)
    best_div_rank_primary = cotd_util._get_best_div_rank_primary(cotd_data)
    log.debug(f"Parsed Best Rank Primary Data")

    log.debug(f"Parsing Average Rank Overall Data")
    average_rank_overall = cotd_util._get_average_rank_overall(cotd_data)
    average_div_overall = cotd_util._get_average_div_overall(cotd_data)
    average_div_rank_overall = cotd_util._get_average_div_rank_overall(cotd_data)
    log.debug(f"Parsed Average Rank Overall Data")

    log.debug(f"Parsing Average Rank Primary Data")
    average_rank_primary = cotd_util._get_average_rank_primary(cotd_data)
    average_div_primary = cotd_util._get_average_div_primary(cotd_data)
    average_div_rank_primary = cotd_util._get_average_div_rank_primary(cotd_data)
    log.debug(f"Parsed Average Rank Primary Data")

    log.debug(f"Creating Strings for Embed")
    best_data_overall = (
        "```Best Rank: {}\nBest Div: {}\nBest Rank in Div: {}\n```".format(
            best_rank_overall, best_div_overall, best_div_rank_overall
        )
    )
    best_data_primary = (
        "```Best Rank: {}\nBest Div: {}\nBest Rank in Div: {}\n```".format(
            best_rank_primary, best_div_primary, best_div_rank_primary
        )
    )
    average_data_overall = (
        "```Average Rank: {}\nAverage Div: {}\nAverage Rank in Div: {}\n```".format(
            average_rank_overall, average_div_overall, average_div_rank_overall
        )
    )
    average_data_primary = (
        "```Average Rank: {}\nAverage Div: {}\nAverage Rank in Div: {}\n```".format(
            average_rank_primary, average_div_primary, average_div_rank_primary
        )
    )
    log.debug(f"Created Strings for Embed")

    log.debug(f"Creating Embed Page 1")
    cotd_data_page_one = ezembed.create_embed(
        title="COTD Data for {} - Page 1".format(username),
        color=discord.Colour.random(),
    )
    log.debug(f"Created Embed Page 1")
    log.debug(f"Adding Fields")

    cotd_data_page_one.add_field(
        name="Best Data Overall", value=best_data_overall, inline=False
    )
    cotd_data_page_one.add_field(
        name="Best Data Primary (No Reruns)", value=best_data_primary, inline=False
    )
    cotd_data_page_one.add_field(
        name="Average Data Overall", value=average_data_overall, inline=False
    )
    cotd_data_page_one.add_field(
        name="Average Data Primary (No Reruns)",
        value=average_data_primary,
        inline=False,
    )
    log.debug(f"Added Fields")

    cotd_data_page_one.set_footer(
        text="This function does not include COTDs where the player has left after the 15mins qualifying"
    )

    return cotd_data_page_one
