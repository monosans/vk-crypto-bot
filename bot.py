#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import uniform
from sys import stderr
from threading import Thread
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
            sleep(uniform(3, 5))
            return self.buy()
        sleep(uniform(1, 2))
        self.set_price_profit()

    def set_price_profit(self) -> None:
        price = self._client.get_amount_buy_upgrade_crypto(self.NAME)
        self.price = price["amount"]
        self.profit = self.INCOME / self.price
        sleep(uniform(0.34, 0.5))


def run_bot(client: Crypto, account_number: int = None) -> None:
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
            ("Tron", 400),
            ("Monero", 500),
            ("Theta", 600),
            ("Aave", 750),
            ("Kusama", 1000),
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
            most_profitable = max(cryptos, key=lambda crypto: crypto.profit)
        balance = profile["balance"]

        string = (
            f"""Баланс: {balance:,}
Кол-во крипты: {profile['sum']}
Прибыль в минуту: {income}"""
            if account_number is None
            else f"""Аккаунт №{account_number}
Баланс: {balance:,}
Кол-во крипты: {profile['sum']}
Прибыль в минуту: {income}"""
        )

        logger.info(string)
        price = most_profitable.price
        if account_number is None and balance < price:
            logger.info(
                f"Коплю {price:,} баланса на {most_profitable.NAME}..."
            )
        most_profitable.buy()
        sleep(uniform(0.66, 1.66))


def run_multibot(tokens: set, user_agent: str) -> None:
    for account_number, token in enumerate(tokens):
        Thread(
            target=run_bot,
            args=(Crypto(token.strip(), user_agent), account_number),
        ).start()


def main() -> None:
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<level>{message}</level>",
        colorize=True,
    )
    logger.info("github.com/monosans/vk-crypto-bot\nВерсия 20210904.1")
    if isinstance(VK_ADMIN_TOKEN, str):
        run_bot(Crypto(VK_ADMIN_TOKEN.strip(), USER_AGENT.strip()))
    elif isinstance(VK_ADMIN_TOKEN, (list, tuple, set)):
        if len(VK_ADMIN_TOKEN) == 1:
            for token in VK_ADMIN_TOKEN:
                run_bot(Crypto(token.strip(), USER_AGENT.strip()))
        else:
            run_multibot(set(VK_ADMIN_TOKEN), USER_AGENT.strip())


if __name__ == "__main__":
    main()
