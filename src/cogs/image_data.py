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
        server_id = str(ctx.guild.id)
        if not os.path.exists(os.path.join(os.getcwd(), f"data/{server_id}")):
            os.mkdir(os.path.join(os.getcwd(), f"data/{server_id}"))
        print(binary_path)
        await ctx.respond("scraping images")
        img_scraper.search_and_download(search, 'data/{server_id}/', number)
        time.sleep(2)
        await ctx.send(file=discord.File(f"data/{server_id}/{search}.jpg"))
        await ctx.respond("done")

def setup(bot):
    bot.add_cog(image_scraper(bot))