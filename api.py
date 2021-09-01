# -*- coding: utf-8 -*-
from re import findall
from time import sleep

from loguru import logger
from requests import Session


class Crypto:
    def __init__(self, authorization: str, user_agent: str) -> None:
        """
        authorization (str): vk_access_token_settings...
        user_agent (str): User agent браузера.
        """
        self._s = Session()
        self._s.headers.update(
            {
                "Origin": "https://prod-app7932067-1ab286148664.pages-ac.vk-apps.com",
                "Referer": "https://prod-app7932067-1ab286148664.pages-ac.vk-apps.com/",
                "User-Agent": user_agent,
            }
        )
        self._AUTHORIZATION = authorization
        self._MY_ID = int(findall(r".*vk_user_id=(\d+)*", authorization)[0])

    def get_profile(self) -> dict:
        return self._req(
            "1000", "", {"id": self._MY_ID, "params": self._AUTHORIZATION}
        )

    def get_balance(self) -> dict:
        return self._req("1000", "GetUserBalance", {"id": self._MY_ID})

    def get_top_100_users(self) -> dict:
        return self._req("1002", "GetTop100Users")

    def buy_upgrade_crypto(self, crypto: str) -> dict:
        return self._req(
            "1000",
            f"BuyUpgrade{crypto}",
            {"id": self._MY_ID, "params": self._AUTHORIZATION},
        )

    def get_amount_buy_upgrade_crypto(self, crypto: str) -> dict:
        return self._req(
            "1000",
            f"GetAmountBuyUpgrade{crypto}",
            {"id": self._MY_ID, "params": self._AUTHORIZATION},
        )

    def _req(self, port: str, endpoint: str, json: dict = None) -> dict:
        """Метод для отправки запросов серверу игры."""
        try:
            return self._s.post(
                f"https://baguette-game.com:{port}/{endpoint}", json=json
            ).json()
        except Exception as e:
            logger.error(f"{endpoint}: {e}")
            sleep(1)
            return self._req(port, endpoint, json)
