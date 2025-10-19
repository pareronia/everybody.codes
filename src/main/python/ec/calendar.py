import calendar
from datetime import datetime
from datetime import timedelta

from . import EVERYBODY_CODES_TZ

OFFSET = {
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
STORIES = {1, 2}


def now() -> datetime:
    return datetime.now(tz=EVERYBODY_CODES_TZ)


def days(year: int) -> dict[int, datetime]:
    month = 11
    last_day_num = calendar.monthrange(year, month)[1]
    last_weekday_num = calendar.weekday(year, month, last_day_num)
    last_friday_num = last_day_num - ((7 - (4 - last_weekday_num)) % 7)
    last_friday = datetime(
        year, month, last_friday_num, tzinfo=EVERYBODY_CODES_TZ
    )
    return {
        day: last_friday + timedelta(days=offset)
        for day, offset in OFFSET.items()
    }


def is_released(event: int, day: int) -> bool:
    return (valid_story(event)) or (
        valid_year(event) and now() > days(event)[day]
    )


def contest_started(year: int) -> bool:
    return now() > days(year)[1]


def valid_year(year: int) -> bool:
    return 2024 <= year <= now().year


def valid_story(story: int) -> bool:
    return story in STORIES
