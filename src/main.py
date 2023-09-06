import os
import yaml

import discord
from discord.ext import commands

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

TOKEN = config["bot"]["token"]
PREFIX = config["bot"]["prefix"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# registering the cogs
cogs = [
    cogFiles[0:-3]
    for cogFiles in os.listdir("src/cogs")
        if cogFiles.endswith(".py") and cogFiles != "__init__.py"
]

for cog in cogs:
    print(f"Loading cogs.{cog}")
    bot.load_extension(f"cogs.{cog}")

@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))

bot.run(TOKEN)
