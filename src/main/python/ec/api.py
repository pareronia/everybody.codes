import http.client
import logging
import os
import sys
from typing import Any
from typing import Callable
from typing import ReadOnly
from typing import TypedDict

import requests
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


EVERYBODY_CODES_ONLINE = "EVERYBODY_CODES_ONLINE"


def check_online[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> Any:
        if EVERYBODY_CODES_ONLINE not in os.environ:
            print("= OFFLINE =", file=sys.stderr)
            return None
        return func(*args, **kwargs)

    return inner


class API:
    """See: https://old.reddit.com/r/everybodycodes/wiki/index"""

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

    def do_get(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers, timeout=10)

    @check_online
    def get_seed(self) -> str:
        if self.seed is None:
            response = self.do_get(f"{self.API_URL}/user/me")
            logger.debug(response.json())
            self.seed = str(response.json()["seed"])
        return self.seed

    @check_online
    def get_quest_data(self, year: int, day: int) -> QuestData:
        response = self.do_get(f"{self.API_URL}/event/{year}/quest/{day}")
        logger.debug(response.text)
        quest_data: API.QuestData = response.json()
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
        return self.decrypt_text(response.json()["title"], quest_data["key1"])

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
        logger.debug(response.text)
        return self.decrypt_text(response.json()[str(part)], key)

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


http.client.HTTPConnection.debuglevel = 0

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.INFO)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.INFO)
requests_log.propagate = True

logger = logging.getLogger(API.__name__)
logger.setLevel(os.getenv("LOGLEVEL", "INFO"))

if __name__ == "__main__":

    api = API(sys.argv[1])
    print(f"Title 1: {api.get_title(2024, 1)}")
    print(f"Title 10: {api.get_title(2024, 10)}")
    print(f"Input 5/1: {api.get_input(2024, 5, 1)}")
    print(f"Input 9/1: {api.get_input(2024, 9, 1)}")
    print(f"Input 10/1: {api.get_input(2024, 10, 1)}")
