import os

from dateutil.tz import gettz

EVERYBODY_CODES_DIR = "EVERYBODY_CODES_DIR"
EVERYBODY_CODES_TOKEN = "EVERYBODY_CODES_TOKEN"  # noqa:S105
EVERYBODY_CODES_ONLINE = "EVERYBODY_CODES_ONLINE"
EVERYBODY_CODES_TZ = gettz("Europe/Warsaw")


def is_online() -> bool:
    return EVERYBODY_CODES_ONLINE in os.environ
