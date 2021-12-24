from util.logging import convert_logging

log = convert_logging.get_logging()


def get_best_rank_primary(cotd_data) -> int:
    log.debug(
        "Getting Best Primary Best Rank -> {}".format(
            cotd_data["stats"]["bestprimary"]["bestrank"]
        )
    )
    return cotd_data["stats"]["bestprimary"]["bestrank"]


def get_best_div_primary(cotd_data) -> int:
    log.debug(
        "Getting Primary Best Div -> {}".format(
            cotd_data["stats"]["bestprimary"]["bestdiv"]
        )
    )
    return cotd_data["stats"]["bestprimary"]["bestdiv"]


def get_best_rank_primary_time(cotd_data) -> int:
    log.debug(
        "Getting the time of Primary Best -> {}".format(
            cotd_data["stats"]["bestprimary"]["bestranktime"]
        )
    )
    return cotd_data["stats"]["bestprimary"]["bestranktime"]


def get_best_div_primary_time(cotd_data) -> int:
    log.debug(
        "Getting the time of Primary Best Div -> {}".format(
            cotd_data["stats"]["bestprimary"]["bestdivtime"]
        )
    )
    return cotd_data["stats"]["bestprimary"]["bestdivtime"]


def get_best_div_rank_primary(cotd_data) -> int:
    log.debug(
        "Getting the Best Rank in Div -> {}".format(
            cotd_data["stats"]["bestprimary"]["bestrankindiv"]
        )
    )
    return cotd_data["stats"]["bestprimary"]["bestrankindiv"]


def get_best_rank_overall(cotd_data) -> int:
    log.debug(
        "Getting the Overall Best Rank -> {}".format(
            cotd_data["stats"]["bestoverall"]["bestrank"]
        )
    )
    return cotd_data["stats"]["bestoverall"]["bestrank"]


def get_best_div_overall(cotd_data) -> int:
    log.debug(
        "Getting the Overall Best Div -> {}".format(
            cotd_data["stats"]["bestoverall"]["bestdiv"]
        )
    )
    return cotd_data["stats"]["bestoverall"]["bestdiv"]


def get_best_rank_overall_time(cotd_data) -> int:
    log.debug(
        f'Getting the time of Overall Best Rank -> {cotd_data["stats"]["bestoverall"]["bestranktime"]}'
    )
    return cotd_data["stats"]["bestoverall"]["bestranktime"]


def get_best_div_overall_time(cotd_data) -> int:
    log.debug(
        "Getting the time of Overall Best Div -> {}".format(
            cotd_data["stats"]["bestoverall"]["bestdivtime"]
        )
    )
    return cotd_data["stats"]["bestoverall"]["bestdivtime"]


def get_best_div_rank_overall(cotd_data) -> int:
    log.debug(
        "Getting the Best Rank in Div Overall -> {}".format(
            cotd_data["stats"]["bestoverall"]["bestrankindiv"]
        )
    )
    return cotd_data["stats"]["bestoverall"]["bestrankindiv"]


def return_cotds(cotd_data):
    log.debug("Returning all COTDs")
    return cotd_data["cotds"]


def return_cotds_without_reruns(cotd_data):
    log.debug("Returning COTDs without reruns")
    cotds_safe = []

    for cotd in cotd_data["cotds"]:
        if "#2" in cotd["name"] or "#3" in cotd["name"]:
            continue
        cotds_safe.append(cotd)

    return cotds_safe


def get_num_cotds_played(cotds):
    log.debug(f"Number of COTDs Played -> {len(cotds)}")
    return len(cotds)


def remove_unfinished_cotds(cotds):
    log.debug("Looping around COTDs")
    cotds_safe = []

    for cotd in cotds:
        if not cotd["score"] == 0:
            cotds_safe.append(cotd)

    log.debug(f"{len(cotds_safe)} COTDs Finished out of Given Set")
    return cotds_safe


def get_average_rank_overall(cotd_data):
    cotds = return_cotds(cotd_data)

    cotds_played = get_num_cotds_played(cotds)

    rank_total = 0

    # Looping Through COTDs
    for cotd in cotds:
        rank_total += int(cotd["rank"])

    log.debug(f"Average Rank Overall -> {round(rank_total / cotds_played, 2)}")
    return round(rank_total / cotds_played, 2)


def get_average_rank_primary(cotd_data):
    cotds = return_cotds_without_reruns(cotd_data)

    cotds_played = get_num_cotds_played(cotds)

    rank_total = 0

    for cotd in cotds:
        rank_total += int(cotd["rank"])

    try:
        log.debug(f"Average Rank Primary -> {round(rank_total / cotds_played, 2)}")
        return round(rank_total / cotds_played, 2)
    except:
        log.debug("Average Rank Primary -> 0")
        return 0


def get_average_div_overall(cotd_data):
    cotds = return_cotds(cotd_data)

    cotds_played = get_num_cotds_played(cotds)

    div_total = 0

    # Looping Through COTDs
    for cotd in cotds:
        div_total += int(cotd["div"])

    log.debug(f"Average Div Overall -> {round(div_total / cotds_played, 2)}")
    return round(div_total / cotds_played, 2)


def get_average_div_primary(cotd_data):
    cotds = return_cotds_without_reruns(cotd_data)

    cotds_played = get_num_cotds_played(cotds)

    div_total = 0

    for cotd in cotds:
        div_total += int(cotd["div"])

    try:
        log.debug(f"Average Div Primary -> {round(div_total / cotds_played, 2)}")
        return round(div_total / cotds_played, 2)
    except:
        log.debug("Average Div Primary -> 0")
        return 0


def get_average_div_rank_overall(cotd_data):
    cotds = return_cotds(cotd_data)

    cotds_played = get_num_cotds_played(cotds)

    div_rank_total = 0

    for cotd in cotds:
        div_rank_total += int(cotd["div"])

    log.debug(f"Average Div Rank Overall -> {round(div_rank_total / cotds_played, 2)}")
    return round(div_rank_total / cotds_played, 2)


def get_average_div_rank_primary(cotd_data):
    cotds = return_cotds_without_reruns(cotd_data)

    cotds_played = get_num_cotds_played(cotds)

    div_rank_total = 0

    for cotd in cotds:
        div_rank_total += int(cotd["divrank"])

    try:
        log.debug(
            f"Average Div Rank Primary -> {round(div_rank_total / cotds_played, 2)}"
        )
        return round(div_rank_total / cotds_played, 2)
    except:
        log.debug("Average Div Rank Primary -> 0")
        return 0


def get_list_of_ranks_overall(cotd_data):
    cotds = return_cotds(cotd_data)
    cotds = remove_unfinished_cotds(cotds)

    ranks = []

    for cotd in cotds:
        ranks.append(cotd["rank"])

    log.debug(f"Ranks are {ranks[::-1]}")
    return ranks[::-1]


def get_list_of_ranks_primary(cotd_data):
    cotds = return_cotds_without_reruns(cotd_data)
    cotds = remove_unfinished_cotds(cotds)

    ranks = []

    for cotd in cotds:
        ranks.append(cotd["rank"])

    log.debug(f"Ranks are {ranks[::-1]}")
    return ranks[::-1]


def get_list_of_dates_overall(cotd_data):
    cotds = return_cotds(cotd_data)
    cotds = remove_unfinished_cotds(cotds)

    timestamps = []

    for cotd in cotds:
        timestamps.append(cotd["name"][15:])

    log.debug(f"Timestamps are {timestamps[::-1]}")
    return timestamps[::-1]


def get_list_of_dates_primary(cotd_data):
    cotds = return_cotds_without_reruns(cotd_data)
    cotds = remove_unfinished_cotds(cotds)

    timestamps = []

    for cotd in cotds:
        timestamps.append(cotd["name"][15:])

    log.debug(f"Timestamps are {timestamps[::-1]}")
    return timestamps[::-1]


def get_list_of_ids_overall(cotd_data):
    cotds = return_cotds(cotd_data)
    cotds = remove_unfinished_cotds(cotds)

    ids = []

    for cotd in cotds:
        ids.append(cotd["id"])

    log.debug(f"IDs are {ids[::-1]}")
    return ids[::-1]


def get_list_of_ids_primary(cotd_data):
    cotds = return_cotds_without_reruns(cotd_data)
    cotds = remove_unfinished_cotds(cotds)

    ids = []

    for cotd in cotds:
        ids.append(cotd["id"])

    log.debug(f"IDs are {ids[::-1]}")
    return ids[::-1]


def get_num_wins(cotd_data):
    log.debug("Getting number of wins -> {}".format(cotd_data["stats"]["totalwins"]))
    return cotd_data["stats"]["totalwins"]
