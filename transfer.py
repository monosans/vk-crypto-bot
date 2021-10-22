#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import stderr

from loguru import logger

from api import Crypto
from config import USER_AGENT, VK_ADMIN_TOKEN


def transfer(client: Crypto, recipient_id: str) -> None:
    profile = client.get_profile()
    logger.info(client.transfer(profile["balance"], str(recipient_id)))


def main() -> None:
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<level>{message}</level>",
        colorize=True,
    )
    try:
        recipient_id = int(input("Числовой id получателя: "))
    except ValueError:
        logger.error("Нужен числовой id. Получить можно через regvk.com/id.")
        return
    if isinstance(VK_ADMIN_TOKEN, str):
        client = Crypto(VK_ADMIN_TOKEN, USER_AGENT)
        if client.MY_ID == recipient_id:
            logger.error("Нельзя отправить самому себе")
        else:
            transfer(client, str(recipient_id))
    elif isinstance(VK_ADMIN_TOKEN, (list, tuple, set)):
        for token in VK_ADMIN_TOKEN:
            client = Crypto(token, USER_AGENT)
            if client.MY_ID != recipient_id:
                transfer(client, str(recipient_id))


if __name__ == "__main__":
    main()
