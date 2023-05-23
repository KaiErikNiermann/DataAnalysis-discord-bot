import os
import discord
import time
from discord.ext import commands 
from discord import option
from utils import img_scraper
from chromedriver_py import binary_path

class image_scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="search_image")
    @option(
        name="number",
        description="number of images",
        option_type=3,
        required=True
    )
    @option(
        name="search",
        description="search term",
        option_type=3,
        required=False
    )
    async def scrape(self, ctx, search: str, number: str = 1):
        if not os.path.exists(os.path.join(os.getcwd(), f"data/tmp")):
            os.mkdir(os.path.join(os.getcwd(), f"data/tmp"))
        print(binary_path)
        await ctx.respond("scraping images")
        img_scraper.search_and_download(search, 'data/tmp/', number)
        time.sleep(2)
        await ctx.send(file=discord.File(f"data/tmp/{search}.jpg"))
        await ctx.respond("done")

def setup(bot):
    bot.add_cog(image_scraper(bot))