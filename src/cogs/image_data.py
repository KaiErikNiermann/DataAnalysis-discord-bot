import os
import discord
import time
from discord.ext import commands 
from discord import option
from utils import img_scraper
from chromedriver_py import binary_path
from utils import util

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
        util.setup_dir(server_id)
        await ctx.respond("searching")

        img_scraper.search_and_download(search, f"data/{server_id}/", number)

        await ctx.send(file=discord.File(f"data/{server_id}/{search}.jpg"))
        
        os.remove(f"data/{server_id}/{search}.jpg")
        util.destroy_dir(server_id)

def setup(bot):
    bot.add_cog(image_scraper(bot))