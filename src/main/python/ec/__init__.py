import calendar
import os
from datetime import datetime
from datetime import timedelta

from dateutil.tz import gettz

EVERYBODY_CODES_DIR = "EVERYBODY_CODES_DIR"
EVERYBODY_CODES_TOKEN = "EVERYBODY_CODES_TOKEN"  # nosec B105
EVERYBODY_CODES_ONLINE = "EVERYBODY_CODES_ONLINE"
EVERYBODY_CODES_TZ = gettz("Europe/Warsaw")


def is_online() -> bool:
    return EVERYBODY_CODES_ONLINE in os.environ


def is_released(year: int, day: int) -> bool:
    now = datetime.now(tz=EVERYBODY_CODES_TZ)
    if year < now.year:
        return True
    if year > now.year:
        return False
    if now > datetime(year, 12, 1, tzinfo=EVERYBODY_CODES_TZ):
        return True
    month = 11
    last_day_num = calendar.monthrange(year, month)[1]
    last_weekday_num = calendar.weekday(year, month, last_day_num)
    last_friday_num = last_day_num - ((7 - (4 - last_weekday_num)) % 7)
    last_friday = datetime(
        year, month, last_friday_num, tzinfo=EVERYBODY_CODES_TZ
    )
    offset = {
        20: 1,
        19: 0,
        18: -1,
        17: -2,
        16: -3,
        15: -6,
        14: -7,
        13: -8,
        12: -9,
        11: -10,
        10: -13,
        9: -14,
        8: -15,
        7: -16,
        6: -17,
        5: -20,
        4: -21,
        3: -22,
        2: -23,
        1: -24,
    }
    released = last_friday + timedelta(days=offset[day])
    return now > released
