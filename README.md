# Telegram Bot Message Tester

Простой Python-скрипт для автоматической отправки строк из текстового файла в Telegram-бота и сохранения ответов.

Скрипт работает через библиотеку [Telethon](https://codeberg.org/Lonami/Telethon) и авторизуется в Telegram как обычный пользователь.

## Что делает скрипт

Скрипт:

1. Читает входной `.txt` файл построчно.
2. Каждую непустую строку отправляет указанному Telegram-боту.
3. Ждёт ответ бота.
4. Сохраняет исходный текст и ответ в отдельные файлы.
5. Ждёт заданное количество секунд.
6. Переходит к следующей строке.

Например, если входной файл содержит:

```text
Hello
How are you?
Привет мир
```

то в каталоге результатов будут созданы файлы:

```text
results/
├── input_00001.txt
├── output_00001.txt
├── input_00002.txt
├── output_00002.txt
├── input_00003.txt
└── output_00003.txt
```

Например:

```text
input_00001.txt
Hello
```

```text
output_00001.txt
olleH
```

Номер имеет фиксированную длину из пяти цифр:

```text
00001
00002
00003
...
```

## Требования

Необходимо:

- Python 3.10 или новее
- доступ к Telegram
- обычный Telegram-аккаунт
- `api_id`
- `api_hash`
- библиотека `Telethon`

Bot Token для этого скрипта **не нужен**, потому что скрипт работает не от имени бота, а от имени обычного Telegram-пользователя.

## Установка Python

### Ubuntu / Debian

Обновите список пакетов:

```bash
sudo apt update
```

Установите Python, `pip` и поддержку виртуальных окружений:

```bash
sudo apt install -y python3 python3-pip python3-venv
```

Проверьте версию:

```bash
python3 --version
```

### Windows

Скачайте Python с официального сайта:

https://www.python.org/downloads/

Во время установки включите опцию:

```text
Add Python to PATH
```

После установки откройте PowerShell и проверьте:

```powershell
python --version
```

## Создание виртуального окружения

Рекомендуется запускать скрипт внутри отдельного Python virtual environment.

### Linux

Перейдите в каталог проекта:

```bash
cd telegram-test
```

Создайте окружение:

```bash
python3 -m venv .venv
```

Активируйте его:

```bash
source .venv/bin/activate
```

После активации в начале строки терминала обычно появится:

```text
(.venv)
```

### Windows PowerShell

Создайте окружение:

```powershell
python -m venv .venv
```

Активируйте:

```powershell
.venv\Scripts\Activate.ps1
```

Если PowerShell запрещает запуск скриптов, можно разрешить их для текущего пользователя:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

После этого снова выполните:

```powershell
.venv\Scripts\Activate.ps1
```

## Установка зависимостей

После активации виртуального окружения установите Telethon:

```bash
pip install telethon
```

Проверить установку можно командой:

```bash
pip show telethon
```

При желании можно сохранить зависимости:

```bash
pip freeze > requirements.txt
```

На другой машине их можно установить так:

```bash
pip install -r requirements.txt
```

## Получение TELEGRAM_API_ID и TELEGRAM_API_HASH

Для работы Telethon нужны две специальные величины:

```text
api_id
api_hash
```

Это **не Bot Token**.

Они идентифицируют приложение, которое подключается к Telegram API.

### Шаг 1. Открыть Telegram API Development Tools

Перейдите на:

https://my.telegram.org/

### Шаг 2. Войти в аккаунт

Введите номер телефона, который используется в вашем обычном Telegram-аккаунте.

Telegram отправит код подтверждения. Введите этот код на сайте.

### Шаг 3. Открыть API Development Tools

После входа выберите вкладку `API` и листайте до `Telegram API`, там выбрать [`Creating an application`](https://core.telegram.org/api#creating-an-application)

### Шаг 4. Создать приложение

Если приложение ещё не создано, Telegram попросит заполнить несколько полей.

Например:

```text
App title:
Telegram Test Client

Short name:
telegramtest

Platform:
Desktop
```

### Шаг 5. Скопировать api_id и api_hash

После создания приложения Telegram покажет примерно следующее:

```text
App api_id:
12345678

App api_hash:
0123456789abcdef0123456789abcdef
```

Сохраните эти значения.

`api_hash` является секретом. Не публикуйте его в GitHub, GitLab и других открытых репозиториях.

## Настройка переменных окружения

Скрипт ожидает две переменные:

```text
TELEGRAM_API_ID
TELEGRAM_API_HASH
```

### Linux

```bash
export TELEGRAM_API_ID="12345678"
export TELEGRAM_API_HASH="0123456789abcdef0123456789abcdef"
```

Проверить:

```bash
echo $TELEGRAM_API_ID
echo $TELEGRAM_API_HASH
```

Эти переменные действуют только для текущего терминала.

### Windows PowerShell

```powershell
$env:TELEGRAM_API_ID="12345678"
$env:TELEGRAM_API_HASH="0123456789abcdef0123456789abcdef"
```

Проверка:

```powershell
echo $env:TELEGRAM_API_ID
echo $env:TELEGRAM_API_HASH
```

## Первый запуск

При первом запуске Telethon попросит войти в Telegram.

Обычно появится запрос:

```text
Please enter your phone (or bot token):
```

Введите номер телефона вашего обычного Telegram-аккаунта, например:

```text
+381XXXXXXXXX
```

После этого Telegram отправит код подтверждения. Telethon попросит:

```text
Please enter the code you received:
```

Введите код.

Если на Telegram-аккаунте включён двухфакторный пароль, Telethon также попросит его ввести.

После успешного входа рядом со скриптом будет создан файл примерно такого вида:

```text
telegram_session.session
```

Он позволяет не вводить телефон и код при каждом запуске.

Этот файл также является секретным. Не добавляйте его в Git.

Рекомендуемый `.gitignore`:

```gitignore
.venv/
*.session
*.session-journal
results/
```

## Подготовка входного файла

Создайте файл, например:

```text
messages.txt
```

Каждая строка — отдельное сообщение:

```text
Hello
How are you?
This is a test.
Привет мир
```

Пустые строки скрипт пропускает.

## Запуск

Пример:

```bash
python telegram_test.py messages.txt \
    --bot @my_reverse_bot \
    --output-dir results \
    --delay 1
```

Где:

- `messages.txt` — входной файл;
- `--bot @my_reverse_bot` — username Telegram-бота;
- `--output-dir results` — каталог для результатов;
- `--delay 1` — пауза в секундах между сообщениями.

## Изменение задержки

Пауза 2 секунды:

```bash
python telegram_test.py messages.txt \
    --bot @my_reverse_bot \
    --output-dir results \
    --delay 2
```

Пауза 0.5 секунды:

```bash
python telegram_test.py messages.txt \
    --bot @my_reverse_bot \
    --output-dir results \
    --delay 0.5
```

Не рекомендуется отправлять сообщения слишком быстро, особенно если входной файл большой. Telegram имеет ограничения на частоту запросов и может временно ограничить аккаунт при слишком интенсивной отправке.

## Timeout ответа

По умолчанию скрипт ждёт ответ бота до 60 секунд.

Можно изменить это значение:

```bash
python telegram_test.py messages.txt \
    --bot @my_reverse_bot \
    --output-dir results \
    --delay 1 \
    --timeout 120
```

Если бот не ответил вовремя, в `output_XXXXX.txt` будет записано:

```text
<TIMEOUT>
```

## Пример структуры проекта

```text
telegram-test/
├── telegram_test.py
├── README.md
├── messages.txt
├── .venv/
├── telegram_session.session
└── results/
    ├── input_00001.txt
    ├── output_00001.txt
    ├── input_00002.txt
    ├── output_00002.txt
    └── ...
```

## Безопасность

Не публикуйте:

```text
TELEGRAM_API_HASH
telegram_session.session
```

Файл `.session` содержит авторизованную Telegram-сессию. Человек, получивший доступ к нему, потенциально может использовать эту сессию для доступа к Telegram.

Также не рекомендуется хранить `api_hash` непосредственно в исходном коде.

Использование переменных окружения:

```python
api_id = os.environ.get("TELEGRAM_API_ID")
api_hash = os.environ.get("TELEGRAM_API_HASH")
```

предпочтительнее, чем хранение секретов непосредственно в файле программы.

## Краткая установка на Ubuntu

Если Python уже установлен, полный набор команд выглядит примерно так:

```bash
mkdir telegram-test
cd telegram-test

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install telethon

export TELEGRAM_API_ID="12345678"
export TELEGRAM_API_HASH="0123456789abcdef0123456789abcdef"

python telegram_test.py messages.txt \
    --bot @my_reverse_bot \
    --output-dir results \
    --delay 1
```

При первом запуске нужно пройти Telegram-аутентификацию. После этого Telethon сохранит сессию в `.session` файле.
