# -*- coding: utf-8 -*-
from re import findall
from time import sleep

from loguru import logger
from requests import Session


class IncorrectToken(Exception):
    pass


class IncorrectTokenType(Exception):
    pass


class Crypto:
    def __init__(self, vk_admin_token: str, user_agent: str) -> None:
        """
        vk_admin_token (str): VK Admin токен с vkhost.github.io.
        user_agent (str): User agent браузера.
        """
        self._s = Session()
        self._s.headers.update({"User-Agent": user_agent})
        r = self._s.get(
            f"https://api.vk.com/method/apps.get?access_token={vk_admin_token.split('access_token=')[-1].split('&expires_in')[0]}&v=5.131&app_id=7932067&platform=web"
        ).json()
        response = r.get("response")
        if not response:
            raise IncorrectToken("Неверный токен.")
        item = response["items"][0]
        webview_url = item.get("webview_url")
        if not webview_url:
            raise IncorrectTokenType(
                "Токен неверного типа. Нужен VK Admin токен."
            )
        origin, params = webview_url.split("/index.html?")
        self._PARAMS = params
        self._MY_ID = int(findall(r".*vk_user_id=(\d+)*", params)[0])
        self._s.headers.update({"Origin": origin, "Referer": f"{origin}/"})

    def get_profile(self) -> dict:
        return self._req(
            "1000", "", {"id": self._MY_ID, "params": self._PARAMS}
        )

    def get_balance(self) -> dict:
        return self._req("1000", "GetUserBalance", {"id": self._MY_ID})

    def get_top_100_users(self) -> dict:
        return self._req("1002", "GetTop100Users")

    def buy_upgrade_crypto(self, crypto: str) -> dict:
        return self._req(
            "1000",
            f"BuyUpgrade{crypto}",
            {"id": self._MY_ID, "params": self._PARAMS},
        )

    def get_amount_buy_upgrade_crypto(self, crypto: str) -> dict:
        return self._req(
            "1000",
            f"GetAmountBuyUpgrade{crypto}",
            {"id": self._MY_ID, "params": self._PARAMS},
        )

    def transfer(self, amount: str, recipient_id: str) -> dict:
        return self._req(
            "1000",
            "Transfer",
            {
                "params": self._PARAMS,
                "id": self._MY_ID,
                "recipient_id": recipient_id,
                "amount": amount,
            },
        )

    def buy_boost_x2(self) -> dict:
        return self._req(
            "1000", "BuyBoostX2", {"id": self._MY_ID, "params": self._PARAMS}
        )

    def buy_boost_x3(self) -> dict:
        return self._req(
            "1000", "BuyBoostX3", {"id": self._MY_ID, "params": self._PARAMS}
        )

    def _req(self, port: str, endpoint: str, json: dict = None) -> dict:
        """Метод для отправки запросов серверу игры."""
        try:
            r = self._s.post(
                f"https://baguette-game.com:{port}/{endpoint}", json=json
            )
        except Exception as e:
            logger.error(f"{endpoint}: {e}")
            sleep(3)
            return self._req(port, endpoint, json)
        # Too many requests
        if r.status_code == 429:
            sleep(3)
            return self._req(port, endpoint, json)
        return r.json()
