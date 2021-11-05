import util.logging.convert_logging as convert_logging
import re

log = convert_logging.get_logging()


def remove_mania_text_formatting(text: str) -> str:
    log.debug(f"Removing Mania Text Formatting from {text}")
    regex = r"(\$[0-9a-fA-F]{3})|(\$[wWtTzZiIoOsSgGnNmM])|(\$[hHlL](\[.*\])?)"
    result = re.sub(regex, "", text)

    log.debug(f"Final String -> {str(result.strip())}")
    return str(result.strip())
