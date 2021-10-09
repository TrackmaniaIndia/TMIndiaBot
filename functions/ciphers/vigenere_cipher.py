import logging
import random
import functions.logging.convert_logging as convert_logging

# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = convert_logging.get_logging()

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt(input_string: str):
    """Encrypts the Given String With Vigenere Cipher

    Args:
        input_string (str): [description]

    Returns:
        [type]: [description]
    """
    log.debug(f"Getting Random Number")
    encryption_key_int = random.randint(1, 26) - 1
    log.debug(f"Random Key is {LETTERS[encryption_key_int]}")

    encryption_key = LETTERS[encryption_key_int]

    return translate_message(input_string, encryption_key, "encrypt"), encryption_key


def decrypt(input_string: str, decryption_key: str):
    """Decrypts the given string with Vigenere Cipher

    Args:
        input_string (str): [description]
        decryption_key (str): [description]

    Returns:
        [type]: [description]
    """
    return translate_message(input_string, decryption_key, "decrypt")


def translate_message(message: str, key: str, mode: str) -> str:
    """It's Been so Long I fucking Forgot About this command and what it does

    Args:
        message (str): [description]
        key (str): [description]
        mode (str): [description]

    Returns:
        str: [description]
    """
    translated = []
    key_index = 0
    key = key.upper()

    for symbol in message:
        num = LETTERS.find(symbol.upper())

        if num != -1:
            if mode == "encrypt":
                num += LETTERS.find(key[key_index])
            elif mode == "decrypt":
                num -= LETTERS.find(key[key_index])

            num %= len(LETTERS)

            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            key_index += 1
            if key_index == len(key):
                key_index = 0

        else:
            translated.append(symbol)

    return "".join(translated)
