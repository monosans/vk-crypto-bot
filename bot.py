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
    def __init__(
        self,
        client: Crypto,
        amount_name: str,
        buy_name: str,
        profile_name: str,
        income: int,
    ) -> None:
        """
        buy_name (str): Имя криптовалюты для buy_upgrade_crypto
        amount_name (str): Имя криптовалюты для get_amount_buy_upgrade_crypto
        profile_name (str): Имя криптовалюты в get_profile
        income (int): Доход криптовалюты
        """
        self._client = client
        self.AMOUNT_NAME = amount_name
        self.BUY_NAME = buy_name
        self.PROFILE_NAME = profile_name
        self.INCOME = income
        self.set_price_profit()

    def buy(self) -> None:
        while True:
            r = self._client.buy_upgrade_crypto(self.BUY_NAME)
            if r["status"] == "Успешная покупка":
                break
            sleep(uniform(15, 20))
        sleep(uniform(1, 2))
        self.set_price_profit()

    def set_price_profit(self) -> None:
        self.price = self._client.get_amount_buy_upgrade_crypto(
            self.AMOUNT_NAME
        )["amount"]
        self.profit = self.INCOME / self.price
        sleep(uniform(0.34, 0.5))


def run_bot(client: Crypto, account_number: int = None) -> None:
    cryptos = [
        Cryptocurrency(client, amount_name, buy_name, profile_name, income)
        for amount_name, buy_name, profile_name, income in (
            ("Bitcoin", "Bitcoin", "bitcoin", 1),
            ("Ethereum", "Ethereum", "ethereum", 3),
            ("Cardano", "Cardano", "cardano", 5),
            ("BinanceCoin", "BinanceCoin", "binanceCoin", 10),
            ("Tether", "Tether", "tether", 15),
            ("XRP", "XRP", "xrp", 23),
            ("Dogecoin", "Dogecoin", "dogecoin", 34),
            ("Polkadot", "Polkadot", "polkadot", 45),
            ("USDCoin", "USD", "usdCoin", 55),
            ("Solana", "Solana", "solana", 65),
            ("Uniswap", "Uniswap", "uniswap", 98),
            ("Chaincoin", "Chaincoin", "chaincoin", 125),
            ("Terra", "Terra", "terra", 160),
            ("Litecoin", "Litecoin", "litecoin", 225),
            ("Filecoin", "Filecoin", "filecoin", 267),
            ("Tron", "Tron", "tron", 340),
            ("Monero", "Monero", "monero", 450),
            ("Theta", "Theta", "theta", 540),
            ("Aave", "Aave", "aave", 677),
            ("Kusama", "Kusama", "kusama", 799),
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
            optimal_cryptos = []
            for crypto in cryptos:
                optimal_cryptos.append(crypto)
                if profile[crypto.PROFILE_NAME] == 0:
                    break
            most_profitable = max(
                optimal_cryptos, key=lambda crypto: crypto.profit
            )
        balance = profile["balance"]

        string = (
            f"""Баланс: {balance:,}
Кол-во крипты: {profile['sum']}
Прибыль в минуту: {income}"""
            if account_number is None
            else f"""Аккаунт №{account_number} (id{client.MY_ID})
Баланс: {balance:,}
Кол-во крипты: {profile['sum']}
Прибыль в минуту: {income}"""
        )

        logger.info(string)
        price = most_profitable.price
        if balance < price:
            time_to_wait = int((price - balance) / income) or 1
            string = (
                f"Коплю {price:,} баланса на {most_profitable.AMOUNT_NAME} (~{time_to_wait} мин.)"
                if account_number is None
                else f"""Аккаунт №{account_number} (id{client.MY_ID})
Коплю {price:,} баланса на {most_profitable.AMOUNT_NAME} (~{time_to_wait} мин.)"""
            )
            logger.info(string)
        most_profitable.buy()
        sleep(uniform(0.66, 1.66))


def run_multibot(tokens: set, user_agent: str) -> None:
    for account_number, token in enumerate(tokens):
        Thread(
            target=run_bot, args=(Crypto(token, user_agent), account_number)
        ).start()


def setup_logging() -> None:
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<level>{message}</level>",
        colorize=True,
    )


def main() -> None:
    setup_logging()
    logger.info("github.com/monosans/vk-crypto-bot\nВерсия 20210910.2")
    if isinstance(VK_ADMIN_TOKEN, str):
        run_bot(Crypto(VK_ADMIN_TOKEN, USER_AGENT))
    elif isinstance(VK_ADMIN_TOKEN, (list, tuple, set)):
        if len(VK_ADMIN_TOKEN) == 1:
            for token in VK_ADMIN_TOKEN:
                run_bot(Crypto(token, USER_AGENT))
        else:
            run_multibot(set(VK_ADMIN_TOKEN), USER_AGENT)


if __name__ == "__main__":
    main()
