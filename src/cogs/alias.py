import discord
import json
from discord import option
from discord.ext import commands

class link_alias(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.link_map = json.loads(open("src/cogs/links.json").read())['links'];
        self.add_alias_whitelist = [
            332935845004705793, 
            655144378062471173, 
            845784118536175676, 
            464247726381727744, 
            192732093019717632  
        ]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        alias = message.content.split(" ")[0]
        if f"{alias}" in self.link_map.keys():
            await message.channel.send(self.link_map[alias])

    @commands.slash_command()
    async def showaliases(self, ctx):
        alias_list = ""
        for alias in self.link_map.keys():
            alias_list += f"{alias[1:]} -> <{self.link_map[alias]}>\n"
        await ctx.respond(alias_list)

    @commands.slash_command()
    @option(
        name="alias",
        description="alias to add",
        option_type=3,
        required=True,
    )
    @option(
        name="link",
        description="link to add",
        option_type=3,
        required=True,
    )
    async def addalias(self, ctx, alias: str, link: str):
        if ctx.author.id not in self.add_alias_whitelist:
            await ctx.respond("you are not allowed to add aliases", ephemeral=True)
            return

        self.link_map[f"-{alias}"] = link
        with open("src/cogs/links.json", "w") as f:
            json.dump({"links": self.link_map}, f)

        await ctx.respond(f"added alias {alias} for link {link}", ephemeral=True)


def setup(bot):
    bot.add_cog(link_alias(bot))
