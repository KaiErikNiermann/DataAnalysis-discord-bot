# Data analysis Bot

[![Python Version](https://img.shields.io/badge/python-3.8.10-blue)](https://www.python.org/downloads/release/python-392/)
[![Discord.py Version](https://img.shields.io/badge/discord.py-2.1.0-blue)](https://pypi.org/project/discord.py/2.1.0/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/username/repo/blob/main/LICENSE)

## Description

This is a Discord bot built using Python and Discord.py. The bot is designed to perform various forms of data analysis with a primary focus being on using the server ( and other ) data for entertaining purposes.

## Features

- Google Image search from discord

- Chat data analytics

- User emulation via Markovify based on chat logs

## Installation

1. Clone the repository

```bash
git clone https://github.com/KaiErikNiermann/DataAnalysis-discordBot.git
```

2. Install the required packages

For this project I used poetry, if you do not want to deal with poetry then you can use the Docker container to run the bot. Otherwise do

```bash
poetry install
```

3. Configure the bot

You have to configure the bot, to do this create an application on the discord developer portal and add in the token and prefix you want to use.

```yaml
bot: 
  token: 'TOKEN'
  prefix: 'PREFIX'
```

## Usage

- `/chatdata <date> <start_date> <end_date>`
- `/search_image <name> <number>`
- `/speak`
