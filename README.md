# vk-crypto-bot

Бот для мини-игры ["Crypto"](https://vk.com/app7932067) ВКонтакте.

## Установка на Windows

- Устанавливаем [Python](https://python.org/downloads/windows) (Для Windows 7 нужен Python 3.8.X). Во время установки обязательно ставим галочку `Add Python to PATH (Добавить Python в PATH)`.
- [Скачиваем архив с ботом](https://github.com/monosans/vk-crypto-bot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Редактируем файл `config.py` через любой текстовый редактор:

| Настройка  | Инструкция (описание)                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| PARAMS     | 1. Открываем [игру](https://vk.com/app7932067);                                                                                         |
|            | 2. Нажимаем `F12` (Для Chromium браузеров);                                                                                             |
|            | 3. Перезагружаем страницу горячей клавишей `F5`;                                                                                        |
|            | 4. В появившейся панели выбираем вкладку `Network`;                                                                                     |
|            | 5. Находим кнопку `Filter` (в виде воронки);                                                                                            |
|            | 6. В появившемся поле пишем `bag`;                                                                                                      |
|            | 7. В панели появится поле `baguette-game.com`, нажимаем по нему;                                                                        |
|            | 8. Появится ещё одна панель, выбираем в ней вкладку `Headers`;                                                                          |
|            | 9. Листаем эту панель до самого низа;                                                                                                   |
|            | 10. Снизу находим поле `params:`. Копируем его значение (начинается с vk_access_token_settings);                                        |
|            | 11. Вставляем скопированный текст в значение `PARAMS` в `config.py` между кавычками.                                                    |
| USER_AGENT | User agent браузера. Рекомендуется поставить свой, чтобы уменьшить вероятность бана. Получить можно через [сайт](https://юзерагент.рф). |

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
- Редактируем файл `config.py` командой `nano vk-crypto-bot/config.py`:
  - Чтобы получить `PARAMS` с телефона, используем [приложение F12](https://play.google.com/store/apps/details?id=com.asfmapps.f12):
    1. Открываем приложение F12, заходим на [сайт мобильного ВКонтакте](https://m.vk.com) и авторизуемся.
    2. Открываем [игру](https://m.vk.com/app7932067) через тот же F12.
    3. Нажимаем кнопку F12, переходим на вкладку `Network` (3-я по счёту).
    4. Ставим галочку около `Advance`.
    5. Сворачиваем панель и нажимаем на стрелочку для перезагрузки страницы.
    6. Вновь нажимаем кнопку F12, переходим на вкладку `Network`.
    7. Немного листаем вверх и находим запись `baguette-game.com`, нажимаем по ней.
    8. Появится ещё одна панель. Под записью Request Payload находим поле `params`.
    9. Копируем его значение (начинается c vk_access_token_settings)
    10. Вставляем скопированный текст в значение `PARAMS` в `config.py` между кавычками.
  - Про остальные настройки можно прочитать в инструкции для Windows.
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
