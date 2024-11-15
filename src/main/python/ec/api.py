import http.client
import logging
import os
import sys
from typing import Any

import requests
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


class API:
    """Hat tip to https://github.com/CodingAP/everybody-codes"""

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

    def get_seed(self) -> str:
        if self.seed is None:
            response = requests.get(
                f"{self.API_URL}/user/me", headers=self.headers, timeout=10
            )
            logger.debug(response.json())
            self.seed = str(response.json()["seed"])
        return self.seed

    def get_encryption_keys(self, year: int, day: int) -> Any:
        response = requests.get(
            f"{self.API_URL}/event/{year}/quest/{day}",
            headers=self.headers,
            timeout=10,
        )
        logger.debug(response.text)
        return response.json()

    def get_title(self, year: int, day: int) -> str | None:
        keys = self.get_encryption_keys(year, day)
        response = requests.get(
            f"{self.ASSET_URL}/{year}/{day}/description.json", timeout=10
        )
        if "key1" not in keys:
            return None
        return self.decrypt_text(response.json()["title"], keys["key1"])

    def get_input(self, year: int, day: int, part: int) -> str | None:
        keys = self.get_encryption_keys(year, day)
        key = f"key{part}"
        if key not in keys:
            return None
        seed = self.get_seed()
        response = requests.get(
            f"{self.ASSET_URL}/{year}/{day}/input/{seed}.json", timeout=10
        )
        logger.debug(response.text)
        return self.decrypt_text(response.json()[str(part)], keys[key])

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
