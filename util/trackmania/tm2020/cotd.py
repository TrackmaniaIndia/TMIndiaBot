import util.logging.convert_logging as convert_logging

log = convert_logging.get_logging()


def _remove_incomplete_cotds(cotd_data: dict) -> dict:
    """Removes the incomplete COTD from the given COTD_Data

    Args:
        cotd_data (dict): The initial COTD data

    Returns:
        dict: The cotd_data after all incomplete cotds have been removed
    """
    log.debug(f"Looping through COTD Data")
    for i, cotd in enumerate(cotd_data):
        if cotd["serverRank"] == "DNF":
            log.debug(f"Popping {cotd} at index: {i}")
            cotd_data.pop(i)

    log.debug(f"All Incomplete COTDs Popped, Returning Data")
    return cotd_data


def _get_num_completed_cotds(cotd_data: dict) -> int:
    """Returns the Number of Completed COTDs

    Args:
        cotd_data (dict): Initial COTD Data

    Returns:
        int: Number of completed COTDs
    """
    log.debug(f"Removing all incomplete COTDs")
    cotd_data = _remove_incomplete_cotds(cotd_data=cotd_data)
    log.debug(f"Removed all COTD Data, Returning Num of Completed")
    return len(cotd_data)


def _get_num_all_cotds(cotd_data: dict) -> int:
    """Returns the Number of COTDs the Player has participated in

    Args:
        cotd_data (dict): Initial COTD Data

    Returns:
        int: Number of participated COTDs
    """
    return len(cotd_data)


def _get_avg_div(cotd_data: dict) -> float:
    """Returns the Average Div of the player in Completed COTDs

    Args:
        cotd_data (dict): Initial COTD Data

    Returns:
        float: Average Div
    """
    log.debug(f"Removing all Incomplete COTDs")
    cotd_data = _remove_incomplete_cotds(cotd_data)
    log.debug(f"Removed all COTD Data")
    log.debug(f"Getting Num of Completed COTDs")
    num_completed = _get_num_completed_cotds(cotd_data)
    log.debug(f"Num of Completed COTDs: {num_completed}")

    div_total = 0
    log.debug(f"Looping Through Data")
    for i, cotd in enumerate(cotd_data):
        div_total += cotd["server"]
        print(f"Current Div_Total = {div_total}", end="\r")

    return round((div_total / num_completed), 2)


def _get_avg_global_rank(cotd_data: dict) -> float:
    """Gets the average global rank of a given player

    Args:
        cotd_data (dict): The initial cotd data

    Returns:
        float: Avg Global Rank
    """
    log.debug(f"Removing all Incomplete COTDs")
    cotd_data = _remove_incomplete_cotds(cotd_data)
    log.debug(f"Removed all COTD Data")
    log.debug(f"Getting Num of Completed COTDs")
    num_completed = _get_num_completed_cotds(cotd_data)
    log.debug(f"Num of Completed COTDs: {num_completed}")

    global_rank = 0
    log.debug(f"Looping Through Data")
    for i, cotd in enumerate(cotd_data):
        global_rank += cotd["globalRank"]
        print(f"Current Global_Rank = {global_rank}", end="\r")

    return round((global_rank / num_completed), 2)
