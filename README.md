# vk-crypto-bot

Бот для мини-игры ["Crypto"](https://vk.com/app7932067) ВКонтакте.

## Что делает бот?

Автоматически покупает самую выгодную криптовалюту.

## Установка на Windows

- Устанавливаем [Python](https://python.org/downloads/windows) (Для Windows 7 нужен Python 3.8.X). Во время установки обязательно ставим галочку `Add Python to PATH (Добавить Python в PATH)`.
- [Скачиваем архив с ботом](https://github.com/monosans/vk-crypto-bot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Редактируем файл `config.py` через любой текстовый редактор:

| Настройка      | Инструкция (описание)                                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| VK_ADMIN_TOKEN | 1. Открываем https://vkhost.github.io                                                                                                   |
|                | 2. Выбираем `VK Admin`                                                                                                                  |
|                | 3. Авторизуемся в аккаунт ВК, если не авторизованы                                                                                      |
|                | 4. Нажимаем `Разрешить`                                                                                                                 |
|                | 5. Копируем часть адресной строки от `access_token=` до `&expires_in`                                                                   |
|                | 6. Вставляем скопированный текст в значение `VK_ADMIN_TOKEN` в `config.py` между кавычками.                                             |
| USER_AGENT     | User agent браузера. Рекомендуется поставить свой, чтобы уменьшить вероятность бана. Получить можно через [сайт](https://юзерагент.рф). |

Запуск: `start.bat`. Если после запуска ничего не происходит или выходит ошибка, связанная с Python или pip:

- Откройте `cmd`
- Напишите `python -V`
- Вывод должен соответстовать виду: `Python версия`. При этом версия должна быть выше 3.6.X.
- Если вывод не соответствует виду, нужно заново выполнить первый пункт инструкции (переустановить Python).

## Установка в Termux (Android)

- Устанавливаем [Termux с F-Droid](https://f-droid.org/ru/packages/com.termux/), т. к. в Google Play разработчик его больше не обновляет.
- Запускаем Termux.
- Пишем по порядку:
  ```bash
  cd
  pkg update -y
  pkg install -y git python
  git clone https://github.com/monosans/vk-crypto-bot
  ```
- Редактируем файл `config.py` командой `nano vk-crypto-bot/config.py` по инструкции для Windows.
- После редактирования файла, для сохранения нажмите Ctrl-O, Enter, Ctrl-X.

Запуск: `sh vk-crypto-bot/start.sh`

## Переустановка в Termux

Ввести команды по порядку:

```bash
cd
rm -rf vk-crypto-bot
```

После этого заново установить по инструкции.

## License / Лицензия

[MIT](LICENSE)
