"""Class gotten from python-discord/bot which is licensed under MIT License"""

"""
Loads bot configuration from YAML files.
By default, this simply loads the default
configuration located at `config-default.yml`.
If a file called `config.yml` is found in the
project directory, the default configuration
is recursively updated with any settings from
the custom configuration. Any settings left
out in the custom user configuration will stay
their default values from `config-default.yml`.
"""
import os

import yaml

try:
    import dotenv

    dotenv.load_dotenv()
except ModuleNotFoundError:
    pass


def _env_var_constructor(loader, node):
    """
    Implements a custom YAML tag for loading optional environment
    variables. If the environment variable is set, returns the
    value of it. Otherwise, returns `None`.
    Example usage in the YAML configuration:
                    # Optional app configuration. Set `MY_APP_KEY` in the environment to use it.
                    application:
                                    key: !ENV 'MY_APP_KEY'
    """

    default = None

    # Check if the node is a plain string value
    if node.id == "scalar":
        value = loader.construct_scalar(node)
        key = str(value)
    else:
        # The node value is a list
        value = loader.construct_sequence(node)

        if len(value) >= 2:
            # If we have at least two values, then we have both a key and a default value
            default = value[1]
            key = value[0]
        else:
            # Otherwise, we just have a key
            key = value[0]

    return os.getenv(key, default)


def _join_var_constructor(loader, node):
    """
    Implements a custom YAML tag for concatenating other tags in
    the document to strings. This allows for a much more DRY configuration
    file.
    """

    fields = loader.construct_sequence(node)
    return "".join(str(x) for x in fields)


yaml.SafeLoader.add_constructor("!ENV", _env_var_constructor)
yaml.SafeLoader.add_constructor("!JOIN", _join_var_constructor)


with open("./config.yaml", encoding="UTF-8") as file:
    _CONFIG_YAML = yaml.safe_load(file)


def check_required_keys(keys):
    """
    Verifies that keys that are set to be required are present in the
    loaded configuration.
    """
    for key_path in keys:
        lookup = _CONFIG_YAML
        try:
            for key in key_path.split("."):
                lookup = lookup[key]
                if lookup is None:
                    raise KeyError(key)
        except KeyError:
            raise KeyError(
                f"A configuration for `{key_path}` is required, but was not found. "
                "Please set it in `config.yml` or setup an environment variable and try again."
            )


try:
    required_keys = _CONFIG_YAML["config"]["required_keys"]
except KeyError:
    pass
else:
    check_required_keys(required_keys)


class YAMLGetter(type):
    """
    Implements a custom metaclass used for accessing
    configuration data by simply accessing class attributes.
    Supports getting configuration from up to two levels
    of nested configuration through `section` and `subsection`.
    `section` specifies the YAML configuration section (or "key")
    in which the configuration lives, and must be set.
    `subsection` is an optional attribute specifying the section
    within the section from which configuration should be loaded.
    Example Usage:
                    # config.yml
                    bot:
                                    prefixes:
                                                    direct_message: ''
                                                    guild: '!'
                    # config.py
                    class Prefixes(metaclass=YAMLGetter):
                                    section = "bot"
                                    subsection = "prefixes"
                    # Usage in Python code
                    from config import Prefixes
                    def get_prefix(bot, message):
                                    if isinstance(message.channel, PrivateChannel):
                                                    return Prefixes.direct_message
                                    return Prefixes.guild
    """

    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return _CONFIG_YAML[cls.section][cls.subsection][name]
            return _CONFIG_YAML[cls.section][name]
        except KeyError as e:
            dotted_path = ".".join(
                (cls.section, cls.subsection, name)
                if cls.subsection is not None
                else (cls.section, name)
            )
            print(
                f"Tried accessing configuration variable at `{dotted_path}`, but it could not be found."
            )
            raise AttributeError(repr(name)) from e

    def __getitem__(cls, name):
        return cls.__getattr__(name)

    def __iter__(cls):
        """Return generator of key: value pairs of current constants class' config values."""
        for name in cls.__annotations__:
            yield name, getattr(cls, name)


class Bot(metaclass=YAMLGetter):
    section = "bot"

    prefix: str
    token: str
    default_guilds: list
    debug_guild: int
    version: str


class Error(metaclass=YAMLGetter):
    section = "error"

    show_stack_trace: bool
    print_errors: bool
    totd_reminders: bool


class Channels(metaclass=YAMLGetter):
    section = "channels"

    general: int
    tm2020: int
    tmnf: int
    media: int

    bot_updates: int
    tmi_bot_channel: int

    commands_allowed: list
    announcement_channels: list
    error_channel: int
    keep_alive_channel: int


class Roles(metaclass=YAMLGetter):
    section = "roles"

    cotd_reminder_one: int
    cotd_reminder_three: int

    cotd_reminder_one_testing: int
    cotd_reminder_three_testing: int

    bypass_roles: list


class Guild(metaclass=YAMLGetter):
    section = "guild"

    tmi_server: int
    testing_server: int


class Colours(metaclass=YAMLGetter):
    section = "style"
    subsection = "colours"

    blue: int
    bright_green: int
    orange: int
    pink: int
    purple: int
    soft_green: int
    soft_orange: int
    soft_red: int
    white: int
    yellow: int


class Emotes(metaclass=YAMLGetter):
    section = "style"
    subsection = "emojis"

    twitch: str
    twitter: str
    youtube: str
    tmio: str

    author_medal: str
    gold_medal: str
    silver_medal: str
    bronze_medal: str


class TMIAPI(metaclass=YAMLGetter):
    section = "urls"

    tmiapi: str


# Debug Mode
DEBUG_MODE: bool = _CONFIG_YAML["debug"].lower() == "true"
FILE_LOGS: bool = _CONFIG_YAML["file_logs"].lower() == "true"

# Paths
BOT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BOT_DIR, os.pardir))


class RedirectOutput(metaclass=YAMLGetter):
    section = "redirect_output"

    delete_delay: int
    delete_invocation: bool
