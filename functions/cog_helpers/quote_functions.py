import os
import json
import logging
import functions.logging.convert_logging as convert_logging
from datetime import datetime

log = logging.getLogger(__name__)
log = convert_logging.get_logging()

def save(message, author):
    log.debug(f'Saving {message} by {author} at {datetime.now()}')
    log.debug(f'Opening JSON File')

    quotes = []
    date_created_unformatted = datetime.now()
    # date_created = date_created_unformatted.strftime('%d %B, %Y - %I:%M:%S %p')
    date_created = date_created_unformatted.strftime('%c')

    with open('./json_data/quotes.json', 'r') as file:
        log.debug(f'Loading JSON file')
        quotes = json.load(file)
        log.debug(f'Opened JSON File')

    new_quote_dict = {
        "Message": message,
        "Author": author,
        "Date Created": date_created,
        "Number": int(get_number_of_quotes() + 1)
    }

    quotes['quotes'].append(new_quote_dict)

    log.debug(f'Dumping to File')
    with open('./json_data/quotes.json', 'w') as file:
        json.dump(quotes, file, indent=4)
    log.debug(f'Dumped to File')
    log.debug(f'Returning')
    return None

def get_number_of_quotes():
    log.debug(f'Opening JSON File')
    with open('./json_data/quotes.json', 'r') as file:
        log.debug(f'Loading JSON file')
        quotes = json.load(file)
        log.debug(f'Read JSON file, returning length of quotes array')

        return len(quotes['quotes'])

