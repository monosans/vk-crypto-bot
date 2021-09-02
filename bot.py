#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import stderr
from time import sleep

from loguru import logger

from api import Crypto
from config import PARAMS, USER_AGENT


class Cryptocurrency:
    def __init__(self, client: Crypto, name: str, income: int) -> None:
        self.client = client
        self.NAME = name
        self.INCOME = income
        self.set_price_profit()

    def buy(self) -> None:
        self.client.buy_upgrade_crypto(
            "USD" if self.NAME == "USDCoin" else self.NAME
        )
        sleep(1 / 3)
        self.set_price_profit()

    def set_price_profit(self) -> None:
        price = self.client.get_amount_buy_upgrade_crypto(self.NAME)
        self.price = price["amount"]
        self.profit = self.INCOME / self.price
        sleep(1 / 3)


def main():
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<level>{message}</level>",
        colorize=True,
    )
    logger.info("github.com/monosans/vk-crypto-bot\nВерсия 20210902")
    client = Crypto(PARAMS.strip(), USER_AGENT.strip())
    cryptos = [
        Cryptocurrency(client, name, income)
        for name, income in (
            ("Bitcoin", 1),
            ("Ethereum", 5),
            ("Cardano", 10),
            ("BinanceCoin", 15),
            ("Tether", 20),
            ("XRP", 30),
            ("Dogecoin", 40),
            ("Polkadot", 50),
            ("USDCoin", 60),
            ("Solana", 80),
        )
    ]
    while True:
        most_profitable = max(cryptos, key=lambda x: x.profit)
        profile = client.get_profile()
        sleep(1)
        if profile:
            balance = profile["balance"]
            income = profile["in_minute_mining"]
            logger.info(
                f"""Баланс: {balance}
Кол-во крипты: {profile['sum']}
Прибыль в минуту: {income}"""
            )
            price = most_profitable.price
            if balance < price:
                minutes_to_wait = int((price - balance) / income)
                logger.info(
                    "Жду {} минут, чтобы накопить на {}",
                    minutes_to_wait,
                    most_profitable.NAME,
                )
                sleep(minutes_to_wait * 60)
                while True:
                    balance = client.get_profile().get("balance", balance)
                    if balance >= price:
                        sleep(1)
                        break
                    else:
                        sleep(3)
            most_profitable.buy()
            sleep(1)


if __name__ == "__main__":
    main()
