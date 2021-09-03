#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import uniform
from sys import stderr
from time import sleep

from loguru import logger

from api import Crypto
from config import USER_AGENT, VK_ADMIN_TOKEN


class Cryptocurrency:
    def __init__(self, client: Crypto, name: str, income: int) -> None:
        self._client = client
        self.NAME = name
        self.INCOME = income
        self.set_price_profit()

    def buy(self) -> None:
        r = self._client.buy_upgrade_crypto(
            "USD" if self.NAME == "USDCoin" else self.NAME
        )
        if r["status"] == "Недостаточно средств":
            sleep(uniform(1, 2))
            return self.buy()
        sleep(uniform(1, 2))
        self.set_price_profit()

    def set_price_profit(self) -> None:
        price = self._client.get_amount_buy_upgrade_crypto(self.NAME)
        self.price = price["amount"]
        self.profit = self.INCOME / self.price
        sleep(uniform(0.34, 0.5))


def run_bot(client: Crypto) -> None:
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
            ("Uniswap", 110),
            ("Chaincoin", 150),
            ("Terra", 200),
            ("Litecoin", 250),
            ("Filecoin", 300),
        )
    ]
    while True:
        profile = client.get_profile()
        sleep(uniform(1, 2))
        income = profile["in_minute_mining"]
        if income == 0:
            most_profitable = cryptos[0]
        elif income == 1:
            most_profitable = cryptos[1]
        else:
            most_profitable = max(cryptos, key=lambda x: x.profit)
        balance = profile["balance"]
        logger.info(
            f"""Баланс: {balance}
Кол-во крипты: {profile['sum']}
Прибыль в минуту: {income}"""
        )
        price = most_profitable.price
        if balance < price:
            minutes_to_wait = int((price - balance) / income)
            logger.info(
                "Жду {} минут, чтобы накопить на {}...",
                minutes_to_wait,
                most_profitable.NAME,
            )
            sleep(minutes_to_wait * 60)
        most_profitable.buy()
        sleep(uniform(0.66, 1.66))


def main() -> None:
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<level>{message}</level>",
        colorize=True,
    )
    logger.info("github.com/monosans/vk-crypto-bot\nВерсия 20210903.1")
    run_bot(Crypto(VK_ADMIN_TOKEN.strip(), USER_AGENT.strip()))


if __name__ == "__main__":
    main()
