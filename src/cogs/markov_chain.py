import os
import markovify
from discord.ext import commands 

class chat_emulator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generate_corpus(self, ctx, corpus_location):
        current_channel = ctx.channel
        messages = await current_channel.history(limit=100).flatten() 
        messages = list(filter(lambda m: m.content.strip() 
                               and m.content[0].isalnum() 
                               and m.content != "\n"
                               and m.author != self.bot.user
                               and m.content != " ", messages))
        if not os.path.exists(os.path.join(os.getcwd(), f"data/{ctx.guild.id}")):
            os.mkdir(os.path.join(os.getcwd(), f"data/{ctx.guild.id}"))

        with open(corpus_location, "w") as f:
            for message in messages:
                f.write(message.content.replace("\n", " ") + "\n")

        with open(corpus_location, "r") as f:
            corpus = f.read()

        return markovify.Text(corpus)
            

    @commands.slash_command(name="chat_emulator")
    async def chat_emulator(self, ctx):
        server_id = str(ctx.guild.id)
        corpus_location = f"data/{server_id}/corpus.txt"
        corpus = await self.generate_corpus(ctx, corpus_location)
        await ctx.respond(corpus.make_sentence())
        
        os.remove(corpus_location)
        os.rmdir(f"data/{server_id}")

def setup(bot):
    bot.add_cog(chat_emulator(bot))