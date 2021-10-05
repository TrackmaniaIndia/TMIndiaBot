import os
import json
import logging
import functions.logging.convert_logging as convert_logging
import requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import PIL

from functions.other_functions.list_reverse import reverse

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

# Constants
# DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def get_cotd_data(user_id: str) -> dict:
    log.debug(f"Getting COTD Data for {user_id}")
    PLAYER_URL = BASE_API_URL + "/tm2020/player/" + user_id + "/cotd"
    cotd_data = requests.get(PLAYER_URL).json()
    log.debug(f"Got COTD Data")

    return cotd_data


def get_cotd_stats(user_id: str) -> dict:
    log.debug(f"Parsing COTD Data for {user_id}")

    log.debug(f"Requesting Data")
    cotd_data = get_cotd_data(user_id)
    log.debug(f"Received COTD Data")

    server_sum = 0
    server_rank_sum = 0
    global_rank_sum = 0
    total_played = len(cotd_data)
    log.debug(f"Looping Through Data")
    for i in range(0, total_played):
        if cotd_data[i]["serverRank"] == "DNF":
            continue

        server_sum += cotd_data[i]["server"]
        server_rank_sum += cotd_data[i]["serverRank"]
        global_rank_sum += cotd_data[i]["globalRankSum"]
    log.debug(f"Looped Through Data and Got Sums")

    log.debug(f"Finding Averages")

    server_avg = server_sum / total_played
    server_rank_avg = server_rank_sum / total_played
    global_rank_avg = global_rank_sum / total_played

    log.debug(f"Found Averages")
    log.debug(f"Making Dict")
    cotd_data_for_played = {
        "Average Division": server_avg,
        "Average Rank in Server": server_rank_avg,
        "Average Global Rank": global_rank_avg,
    }
    log.debug(f"Made Dict")
    log.debug(f"Returning Dict")

    return cotd_data_for_played


def get_average_global_rank(data: dict) -> float:
    log.debug(f'Looping through Data')
    sum = 0
    total_num_of_cotds = len(data)

    for cotd_dict in data:
        if cotd_dict['serverRank'] == "DNF":
            # log.debug(f'Player did not finish this COTD, reducing total num by 1')
            total_num_of_cotds -= 1
            continue
        else:
            sum += int(cotd_dict['globalRank'])

    log.debug(f'Average Global Rank is {round((sum / total_num_of_cotds), 2)}')
    return round((sum / total_num_of_cotds), 2)


def get_average_server_rank(data: dict) -> float:
    log.debug(f'Looping through data to get average server rank')
    sum = 0
    total_num_of_cotds = len(data)

    for cotd_dict in data:
        if cotd_dict['serverRank'] == "DNF":
            total_num_of_cotds -= 1
            continue
        else:
            sum += int(cotd_dict['serverRank'])
        
    log.debug(f'Average Server Rank is {round((sum / total_num_of_cotds), 2)}')
    return round((sum / total_num_of_cotds), 2)


def get_average_div(data: dict) -> float:
    log.debug(f'Looping through data to get average server rank')
    sum = 0
    total_num_of_cotds = len(data)

    for cotd_dict in data:
        if cotd_dict['serverRank'] == "DNF":
            total_num_of_cotds -= 1
            continue
        else:
            sum += int(cotd_dict['server'])
        
    log.debug(f'Average Division is {round((sum / total_num_of_cotds), 2)}')
    return round((sum / total_num_of_cotds), 2)


def get_total_cotds(data: dict) -> int:
    total_num_of_cotds = len(data)

    for cotd_dict in data:
        if cotd_dict['serverRank'] == "DNF":
            total_num_of_cotds -= 1
            continue
        
    log.debug(f'COTDs Participating in {total_num_of_cotds}')
    return total_num_of_cotds


def get_average_data(data: dict):
    return get_average_global_rank(data), get_average_server_rank(data), get_average_div(data), get_total_cotds(data)


def get_list_of_global_ranks(data: dict) -> list[int]:
    global_ranks = []
    
    for cotd_dict in data:
        if cotd_dict['serverRank'] == "DNF":
            continue
        global_ranks.append(cotd_dict['globalRank'])

    return global_ranks


def get_list_of_cotd_ids(data: dict) -> list[int]:
    cotd_ids = []

    for cotd_dict in data:
        if cotd_dict['serverRank'] == "DNF":
            continue
        cotd_ids.append(cotd_dict['compID'])

    return cotd_ids


def make_global_rank_plot_graph(data: dict):
    log.debug(f'Getting List of Global Ranks and COTD Ids')
    global_ranks = reverse(get_list_of_global_ranks(data))
    cotd_ids = reverse(get_list_of_cotd_ids(data))
    y_axis = 'Rank'
    x_axis = 'COTD Ids'

    log.debug(f'Creating Line Plot')
    # plt.plot(global_ranks, cotd_ids)
    plt.plot(cotd_ids, global_ranks)
    plt.title(f'COTD Graph for Player')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.xticks(rotation=90)
    plt.grid(True)
    log.debug(f'Created Line Plot')
    # plot_image = PLT.Image.from_bytes('RGB', plt.canvas.get_width_height(), plt.canvas.tostring_rgb())
    log.debug(f'Saving Plot to File')
    plt.savefig('./data/cotddata.png')
    log.debug(f'Saved Plot to File')

    plt.clf()
    plt.cla()
    plt.close()
        
    return "DONE"
    # except:
        # return None