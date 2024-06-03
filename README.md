# TelegramBot
Original Author: Arion_Miles

# Introduction
I use this bot in conjunction with qBittorrent to automatically send reports via push notifications when a download has completed.

# Installation
We're using a Telegram bot for sending messages. 

[Start here](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to learn how to create a bot token. 

You can message [@get_id](https://telegram.me/get_id_bot) with `/my_id` and it'll give you a 9-digit Chat ID. 

Copy the Bot Token & Chat ID you received to `creds.ini` (remove [SAMPLE] from the name) file under `API_TOKEN` & `CHAT_ID` respectively. 

You're all set!


# Usage

## telegram.py
#### Syntax:
`python telegram.py -t "TITLE" [-m "MESSAGE"]`

#### Example:
`python telegram.py -t "%N" -m "%N has finished downloading."`

----

# Compiling using Nuitka for Windows

Install Python 3.12

`python -m pip install --upgrade pip`

`python -m pip install -U nuitka`

`python -m pip install -r requirements.txt`

Download [UPX](https://github.com/upx/upx/releases/latest) and unzip

`python -m nuitka --no-deployment-flag=self-execution --onefile --plugin-enable=upx --upx-binary="UPXLOCATION" --windows-icon-from-ico=telegram.ico telegram.py`

Finally add  `FULLPATH\telegram.exe -t "%N" -m "%N has finished downloading."`  to your favourite torrent software



# Compiling using Nuitka for MacOS (Not Yet Working!)

Install Python 3.12

`python3 -m pip install --upgrade pip`

`python3 -m pip install -U nuitka`

`python3 -m pip install -r requirements.txt`

`python3 -m pip install imageio` # MacOS only

`brew install upx`

`python3 -m nuitka --no-deployment-flag=self-execution --onefile --plugin-enable=upx --upx-binary="UPXLOCATION" --windows-icon-from-ico=telegram.ico telegram.py`

Finally add  `FULLPATH\telegram.bin -t "%N" -m "%N has finished downloading."`  to your favourite torrent software