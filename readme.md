# EzBot
[![Python version](https://img.shields.io/badge/python-3.9-blue.svg)](https://python.org)
[![GitHub stars](https://img.shields.io/github/stars/Enzo2991/EzBot.svg)](https://github.com/Enzo2991/EzBot/stargazers)

EzBot is a bot made in [Python](https://www.python.org "Python") in order to have a form directly on discord, it allows to have a system of log, of second chance, of addition of automatic role, it uses the [interactions.py](https://github.com/interactions-py) library in order to have a form directly on discord, it allows to have a system of log, of second chance, of addition of automatic role.

[Video](https://streamable.com/ebmi9z)

## Install

* [Python 3.9+](https://www.python.org/downloads/)

* Install requirements or manual install package
```
pip install -r requirements.txt
```
```
# manual install package
pip install discord-py-interactions
pip install requests
```

* edit config.json
```
"token": "",
"clientId": "",
"guildId": "",
"StaffChannel": "",
"secondchannel": "",
"LogChannel": "",
"roleUnWhitelist": "",
"roleSemiWhitelist": "",
"roleWhitelist": "",
"secondechance": true,
"SlashCommand": true,
"ChannelLog": true
```

* in your [developer discord portal](https://discord.com/developers/applications/), go to O2Auth, then in general, activate the scope applications.commands and give it the necessary rights
![Developers portals discord](https://i.imgur.com/bDdNzoE.png)

* Run the bot
```
python main.py
```

## Usage

| Command                       | Action                                                                                                     |
| :---------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `/form`  | allows you to display the embed in the room in question |

## Libs
[interactions.py](https://github.com/interactions-py)
