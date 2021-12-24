import discord
import requests
import cv2
import matplotlib.pyplot as plt
from util.logging import convert_logging
import util.discord.easy_embed as ezembed
from util import common_functions

import util.trackmania.tm2020.cotd.util as cotd_util

# Setting up Logging
log = convert_logging.get_logging()


def get_cotd_data(user_id: str, username: str) -> discord.Embed:
    log.debug(f"Requesting COTD Data for {user_id}")
    cotd_data = requests.get(
        f"http://localhost:3000/tm2020/player/{user_id}/cotd"
    ).json()

    try:
        if cotd_data["error"]:
            log.critical(f"{username} has never played a cotd")
            return (
                ezembed.create_embed(
                    title="This Player has never played a COTD", color=0xFF0000
                ),
                None,
            )
    except:
        pass
    log.debug("Parsing Best Rank Overall Data")
    best_rank_overall = cotd_util.get_best_rank_overall(cotd_data)
    best_div_overall = cotd_util.get_best_div_overall(cotd_data)
    best_div_rank_overall = cotd_util.get_best_div_rank_overall(cotd_data)
    log.debug("Parsed Best Rank Overall Data")

    log.debug("Parsing Best Rank Primary Data")
    best_rank_primary = cotd_util.get_best_rank_primary(cotd_data)
    best_div_primary = cotd_util.get_best_div_primary(cotd_data)
    best_div_rank_primary = cotd_util.get_best_div_rank_primary(cotd_data)
    log.debug("Parsed Best Rank Primary Data")

    log.debug("Parsing Average Rank Overall Data")
    average_rank_overall = cotd_util.get_average_rank_overall(cotd_data)
    average_div_overall = cotd_util.get_average_div_overall(cotd_data)
    average_div_rank_overall = cotd_util.get_average_div_rank_overall(cotd_data)
    log.debug("Parsed Average Rank Overall Data")

    log.debug("Parsing Average Rank Primary Data")
    average_rank_primary = cotd_util.get_average_rank_primary(cotd_data)
    average_div_primary = cotd_util.get_average_div_primary(cotd_data)
    average_div_rank_primary = cotd_util.get_average_div_rank_primary(cotd_data)
    log.debug("Parsed Average Rank Primary Data")

    log.debug("Creating Strings for Embed")
    best_data_overall = f"```Best Rank: {best_rank_overall}\nBest Div: {best_div_overall}\nBest Rank in Div: {best_div_rank_overall}\n```"
    best_data_primary = f"```Best Rank: {best_rank_primary}\nBest Div: {best_div_primary}\nBest Rank in Div: {best_div_rank_primary}\n```"
    average_data_overall = f"```Average Rank: {average_rank_overall}\nAverage Div: {average_div_overall}\nAverage Rank in Div: {average_div_rank_overall}\n```"
    average_data_primary = f"```Average Rank: {average_rank_primary}\nAverage Div: {average_div_primary}\nAverage Rank in Div: {average_div_rank_primary}\n```"
    log.debug("Created Strings for Embed")

    log.debug("Creating Embed Page")
    cotd_data_embed = ezembed.create_embed(
        title=f"COTD Data for {username}",
        color=common_functions.get_random_color(),
    )
    log.debug("Created Embed Page")
    log.debug("Adding Fields")

    cotd_data_embed.add_field(
        name="Best Data Overall", value=best_data_overall, inline=False
    )
    cotd_data_embed.add_field(
        name="Best Data Primary (No Reruns)", value=best_data_primary, inline=False
    )
    cotd_data_embed.add_field(
        name="Average Data Overall", value=average_data_overall, inline=False
    )
    cotd_data_embed.add_field(
        name="Average Data Primary (No Reruns)",
        value=average_data_primary,
        inline=False,
    )
    log.debug("Added Fields")

    cotd_data_embed.set_footer(
        text="This function does not include COTDs where the player has left after the 15mins qualifying"
    )

    log.debug("Getting Rank Data for Plots")
    ranks_overall = cotd_util.get_list_of_ranks_overall(cotd_data)
    ranks_primary = cotd_util.get_list_of_ranks_primary(cotd_data)

    log.debug("Getting IDs of Ranks for Plots")
    dates_overall = cotd_util.get_list_of_dates_overall(cotd_data)
    dates_primary = cotd_util.get_list_of_dates_primary(cotd_data)

    log.debug("Getting IDs for Plot")
    ids_overall = cotd_util.get_list_of_ids_overall(cotd_data)
    ids_primary = cotd_util.get_list_of_ids_primary(cotd_data)

    log.debug("Creating Plots for Ranks Overall and Ranks Primary")

    # Use Threading Here
    log.debug("Creating Plot for Overall")
    __create_rank_plot(
        ranks=ranks_overall,
        dates=dates_overall,
        ids=ids_overall,
        plot_name="Overall Ranks (With Reruns)",
        image_name="overallranks",
    )

    log.debug("Creating Plot for Primary")
    __create_rank_plot(
        ranks=ranks_primary,
        dates=dates_primary,
        ids=ids_primary,
        plot_name="Primary Rank Graph (No Reruns)",
        image_name="primaryranks",
    )

    log.debug("Concatenating Both Graphs into One")
    __concat_graphs()

    log.debug("Opening Concatenated Graphs")
    image = discord.File(
        "data/temp/concatenated_graphs.png", filename="concatenated_graphs.png"
    )
    log.debug("Opened Concatenated Graphs")

    log.debug("Adding the image to the Embed")
    cotd_data_embed.set_image(url="attachment://concatenated_graphs.png")

    return cotd_data_embed, image


def __create_rank_plot(
    ranks: list, dates: list, ids: list, plot_name: str, image_name: str
):
    log.debug("Clearing Plot")
    plt.clf()

    if len(dates) >= 40:
        log.debug(
            f"{plot_name} -> Player has played more than 40 COTDs, using ids instead of dates"
        )
        plt.plot(ids, ranks, label=plot_name)
        plt.xlabel("COTD IDs")
    else:
        log.debug(
            f"{plot_name} -> Player has less than 40 COTDs, using dates instead of ids"
        )
        plt.plot(dates, ranks, label=plot_name)
        plt.xlabel("COTD Dates")

    log.debug(f"{plot_name} -> Setting Plot Rotation to 90Deg")
    plt.xticks(rotation=90)

    log.debug(f"{plot_name} -> Setting YLabel to Ranks")
    plt.ylabel("Ranks")

    log.debug(f"{plot_name} -> Setting title to {plot_name}")
    plt.title(f"Rank Graph for {plot_name}")

    log.debug(f"{plot_name} -> Setting Tight Layout")
    plt.tight_layout()

    log.debug(f"{plot_name} -> Saving the Plot to Computer")
    plt.savefig("./data/temp/" + image_name)


def __concat_graphs():
    log.info("Concatenating Graphs")
    log.debug("Opening First Graph")
    first_graph = cv2.imread("./data/temp/overallranks.png")
    log.debug("First Graph Opened")
    log.debug("Opening Second Graph")
    second_graph = cv2.imread("./data/temp/primaryranks.png")
    log.debug("Second Graph Opened")

    log.debug("Concatenating Graphs")
    concatenated_graphs = cv2.hconcat([first_graph, second_graph])
    log.debug("Concatenated Graphs")

    log.info("Saving Graphs")
    cv2.imwrite("./data/temp/concatenated_graphs.png", concatenated_graphs)
