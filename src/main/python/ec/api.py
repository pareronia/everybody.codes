from __future__ import annotations

import http.client
import json
import logging
import os
import sys
from enum import Enum
from enum import auto
from enum import unique
from typing import Any
from typing import Callable
from typing import NamedTuple
from typing import ReadOnly
from typing import TypedDict

import requests
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from termcolor import colored

if __name__ == "__main__":
    from __init__ import is_online  # type:ignore
else:
    from . import is_online

logger = logging.getLogger(__name__)


def check_online[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> Any:
        if not is_online():
            print("= OFFLINE =", file=sys.stderr)
            return None
        return func(*args, **kwargs)

    return inner


def check_http_response[
    **P, T
](func: Callable[P, requests.Response]) -> Callable[P, API.Response]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> API.Response:
        response = func(*args, **kwargs)
        logger.debug((response.status_code, response.reason, response.text))
        response_type = API.ResponseType.from_http_status_code(
            response.status_code
        )
        if response_type == API.ResponseType.OK:
            return API.Response(API.ResponseType.OK, "OK", response)
        else:
            raise RuntimeError(response_type)

    return inner


class SubmitResponse(TypedDict, total=False):
    correct: ReadOnly[bool]
    lengthCorrect: ReadOnly[bool]
    firstCorrect: ReadOnly[bool]
    time: ReadOnly[int]
    localTime: ReadOnly[int]
    globalTime: ReadOnly[int]
    globalPlace: ReadOnly[int]
    globalScore: ReadOnly[int]
    error: RuntimeError


class QuestUserStats(TypedDict, total=True):
    time: ReadOnly[int]
    localTime: ReadOnly[int]
    globalPlace: ReadOnly[int]
    globalScore: ReadOnly[int]


class QuestStats(TypedDict, total=True):
    opened: ReadOnly[int]
    p1: ReadOnly[int]
    p2: ReadOnly[int]
    p3: ReadOnly[int]


class API:
    """See: https://old.reddit.com/r/everybodycodes/wiki/index"""

    @unique
    class ResponseType(Enum):
        OK = auto()
        EMPTY = auto()
        BAD_TOKEN = auto()
        ALREADY_SUBMITTED = auto()
        NOT_OPENED = auto()
        LOCKED_OUT = auto()
        BAD_QUEST = auto()
        UNCATEGORIZED_ERROR = auto()

        @classmethod
        def from_http_status_code(_, code: int) -> API.ResponseType:
            match code:
                case 200:
                    return API.ResponseType.OK
                case 409:
                    return API.ResponseType.ALREADY_SUBMITTED
                case 412:
                    return API.ResponseType.NOT_OPENED
                case 418:
                    return API.ResponseType.BAD_TOKEN
                case 423:
                    return API.ResponseType.LOCKED_OUT
                case 425:
                    return API.ResponseType.BAD_QUEST
                case _:
                    return API.ResponseType.UNCATEGORIZED_ERROR

    class Response(NamedTuple):
        type: API.ResponseType
        message: str
        response: requests.Response | None = None

    class QuestData(TypedDict, total=False):
        key1: ReadOnly[str]
        key2: ReadOnly[str]
        key3: ReadOnly[str]
        answer1: ReadOnly[str]
        answer2: ReadOnly[str]
        answer3: ReadOnly[str]

    API_URL = "https://everybody.codes/api"
    ASSET_URL = "https://everybody-codes.b-cdn.net/assets"
    USER_AGENT = (
        "github:pareronia https://github.com/pareronia/everybody.codes"
    )

    def __init__(self, cookie: str):
        self.headers = {
            "Cookie": f"everybody-codes={cookie}",
            "User-Agent": self.USER_AGENT,
        }
        self.seed: str | None = None

    @check_http_response
    def do_get(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers, timeout=10)

    @check_http_response
    def do_post(self, url: str, json: dict[str, str]) -> requests.Response:
        return requests.post(url, headers=self.headers, timeout=10, json=json)

    @check_online
    def get_seed(self) -> str:
        if self.seed is not None:
            return self.seed
        response = self.do_get(f"{self.API_URL}/user/me")
        response_: requests.Response = (
            response.response  # type:ignore[assignment]
        )
        logger.debug(response_.json())
        self.seed = str(response_.json()["seed"])
        return self.seed

    @check_online
    def get_quest_data(self, year: int, day: int) -> QuestData:
        response = self.do_get(f"{self.API_URL}/event/{year}/quest/{day}")
        response_: requests.Response = (
            response.response  # type:ignore[assignment]
        )
        logger.debug(response_.text)
        quest_data: API.QuestData = response_.json()
        return quest_data

    @check_online
    def get_answer(self, year: int, day: int, part: int) -> str | None:
        quest_data = self.get_quest_data(year, day)
        match part:
            case 1:
                return quest_data.get("answer1", None)
            case 2:
                return quest_data.get("answer2", None)
            case 3:
                return quest_data.get("answer3", None)
            case _:
                raise ValueError()

    @check_online
    def get_title(self, year: int, day: int) -> str | None:
        quest_data = self.get_quest_data(year, day)
        if "key1" not in quest_data:
            return None
        response = self.do_get(
            f"{self.ASSET_URL}/{year}/{day}/description.json"
        )
        response_: requests.Response = (
            response.response  # type:ignore[assignment]
        )
        return self.decrypt_text(response_.json()["title"], quest_data["key1"])

    @check_online
    def get_input(self, year: int, day: int, part: int) -> str | None:
        quest_data = self.get_quest_data(year, day)
        match part:
            case 1:
                key = quest_data.get("key1", None)
            case 2:
                key = quest_data.get("key2", None)
            case 3:
                key = quest_data.get("key3", None)
            case _:
                raise ValueError()
        if key is None:
            return None
        seed = self.get_seed()
        response = self.do_get(
            f"{self.ASSET_URL}/{year}/{day}/input/{seed}.json"
        )
        response_: requests.Response = (
            response.response  # type:ignore[assignment]
        )
        logger.debug(response_.text)
        return self.decrypt_text(response_.json()[str(part)], key)

    @check_online
    def submit_answer(
        self, year: int, day: int, part: int, answer: Any
    ) -> SubmitResponse:
        submit_response: SubmitResponse
        if answer is None or len(str(answer).strip()) == 0:
            submit_response = json.loads("{}")
            submit_response["error"] = RuntimeError(API.ResponseType.EMPTY)
            return submit_response
        try:
            url = f"{self.API_URL}/event/{year}/quest/{day}/part/{part}/answer"
            payload = {"answer": str(answer)}
            response = self.do_post(url, payload)
        except RuntimeError as error:
            submit_response = json.loads("{}")
            submit_response["error"] = error
        else:
            response_: requests.Response = (
                response.response  # type:ignore[assignment]
            )
            submit_response = response_.json()
        finally:
            return submit_response

    @check_online
    def get_user_stats(
        self, year: int
    ) -> dict[int, dict[int, QuestUserStats]]:
        response = self.do_get(f"{self.API_URL}/event/{year}/my")
        response_: requests.Response = (
            response.response  # type:ignore[assignment]
        )
        user_stats = dict[int, dict[int, QuestUserStats]]()
        quests = response_.json()["quests"]
        for quest in quests:
            quest_stats = dict[int, QuestUserStats]()
            for part in quests[quest]:
                stats: QuestUserStats = quests[quest][part]
                quest_stats[int(part)] = stats
            user_stats[int(quest)] = quest_stats
        return user_stats

    @check_online
    def get_quest_stats(self, year: int) -> dict[int, QuestStats]:
        response = self.do_get(f"{self.API_URL}/event/{year}/stats/general")
        response_: requests.Response = (
            response.response  # type:ignore[assignment]
        )
        quest_stats = dict[int, QuestStats]()
        quests = response_.json()
        for quest in quests:
            stats: QuestStats = quests[quest]
            quest_stats[int(quest)] = stats
        return quest_stats

    def decrypt_text(self, cipher_text: str, key_string: str) -> str:
        key = key_string[:20] + "~" + key_string[21:]
        decryptor = Cipher(
            algorithms.AES(key=key.encode("utf-8")),
            modes.CBC(initialization_vector=key[:16].encode("utf-8")),
        ).decryptor()

        decrypted = (
            decryptor.update(bytes.fromhex(cipher_text)) + decryptor.finalize()
        )
        padding_bytes = decrypted[-1]
        return str(decrypted[:-padding_bytes].decode("utf-8"))


class SubmitResponseFormatter:
    @classmethod
    def box(cls, lines: list[str], color: Any) -> list[str]:
        width = max(len(line) for line in lines) + 4
        box = list[str]()
        box.append(
            colored(
                chr(0x2554) + chr(0x2550) * (width - 2) + chr(0x2557), color
            )
        )
        for line in lines:
            box.append(
                (
                    colored(chr(0x2551), color)
                    + " "
                    + line.ljust(width - 4, " ")
                    + " "
                    + colored(chr(0x2551), color)
                )
            )
        box.append(
            colored(
                chr(0x255A) + chr(0x2550) * (width - 2) + chr(0x255D), color
            )
        )
        return box

    @classmethod
    def format(cls, response: SubmitResponse) -> list[str]:
        if response is None:
            return []
        if "error" in response:
            messages = {
                API.ResponseType.EMPTY: "Tried to submit empty answer.",
                API.ResponseType.ALREADY_SUBMITTED: "Already submitted.",
                API.ResponseType.NOT_OPENED: "Quest/part not opened yet.",  # noqa E501
                API.ResponseType.BAD_TOKEN: "Missing/wrong/expired token",
                API.ResponseType.LOCKED_OUT: "Too soon / Submitted in lock out period.",  # noqa E501
                API.ResponseType.BAD_QUEST: "Quest/part does not exist.",  # noqa E501
                API.ResponseType.UNCATEGORIZED_ERROR: "Uncategorized error.",
            }
            code = response["error"].args[0]
            return cls.box(
                [
                    "What the Quack?",
                    "",
                    f"{messages[code]}",
                ],
                "yellow",
            )
        if response["correct"]:
            return cls.box(
                [
                    "Quack yeah!," "",
                    "",
                    f"Place: {response["globalPlace"]}, "
                    + f"Score: {response["globalScore"]}",
                ],
                "green",
            )
        else:
            return cls.box(
                [
                    "Quacked up!," "",
                    "",
                    f"Correct length: {response["lengthCorrect"]}",
                    f"First letter correct: {response["firstCorrect"]}",
                ],
                "red",
            )


if __name__ == "__main__":
    http.client.HTTPConnection.debuglevel = 0
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.INFO)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.INFO)
    requests_log.propagate = True
    logger.setLevel(os.getenv("LOGLEVEL", "INFO"))

    api = API(sys.argv[1])
    # print(f"Title 1: {api.get_title(2024, 1)}")
    # print(f"Title 10: {api.get_title(2024, 10)}")
    # print(f"Input 5/1: {api.get_input(2024, 5, 1)}")
    # print(f"Input 9/1: {api.get_input(2024, 9, 1)}")
    # print(f"Input 10/1: {api.get_input(2024, 10, 1)}")
    # response = api.submit_answer(2024, 11, 1, "")
    # for line in SubmitResponseFormatter.format(response):
    #     print(line)
    # try:
    #     api.submit_answer(2023, 1, 1, "123")
    # except RuntimeError as e:
    #     print(e)
    # print(f"{api.get_user_stats(2024)}")
    print(api.get_quest_stats(2024))
