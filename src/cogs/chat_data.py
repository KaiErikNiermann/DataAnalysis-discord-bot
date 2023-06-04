import collections
import datetime
import os
import string
import discord
import csv
import shutil
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands
from discord import option

class chat_data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exactDate = datetime.datetime.now()
        self.todaydate = self.exactDate - datetime.timedelta(
            hours=self.exactDate.hour,
            minutes=self.exactDate.minute,
            seconds=self.exactDate.second,
            microseconds=self.exactDate.microsecond,
        )
        self.server_id = str

    def cache_message_data(self, messages, dates):
        log_file = os.path.join(os.getcwd(), "data", "message_data_cache.csv")
        with open(log_file, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(map(lambda date: date.date(), dates))
            writer.writerow(messages)

    def check_cached(self, limit, todaydate):
        log_file = os.path.join(os.getcwd(), "data", "message_data_cache.csv")
        with open(log_file, "r", encoding="UTF8", newline="") as f:
            reader = csv.reader(f)
            dates = next(reader)
            messages = next(reader)
            if limit and todaydate in dates:
                return messages[dates.index(limit) : dates.index(todaydate)]
            else:
                return None

    async def graph_handler(self, counts, file_path, days, date_strs, ctx):
        coef = np.polyfit(np.arange(len(counts)), counts, 1)
        poly1d_fn = np.poly1d(coef)

        plt.xticks(np.arange(len(date_strs)), date_strs, rotation=45)
        plt.plot(
            np.arange(len(counts)),
            counts,
            "-o",                               
            poly1d_fn(np.arange(len(counts))),   
            "--k",                        
        )

        #TODO - improve the look of the formatting
        plt.gca().margins(x=0)
        plt.gcf().canvas.draw()
        tl = plt.gca().get_xticklabels()
        maxsize = max([t.get_window_extent().width for t in tl])
        m = 0.5  # inch margin
        s = maxsize / plt.gcf().dpi * int(days) + 2 * m
        margin = m / plt.gcf().get_size_inches()[0]

        plt.gcf().subplots_adjust(left=margin, right=1.0 - margin)
        plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

        plt.savefig(file_path)

        await ctx.send(file=discord.File(file_path))

        shutil.rmtree(os.path.join(os.getcwd(), f"data/{self.server_id}"))
        plt.close()

    @commands.slash_command()
    @option(
        name="days",
        description="number of days to look back",
        option_type=3,
        required=False,
    )
    @option(
        name="start_date",
        description="start date",
        option_type=3,
        required=False,
    )
    @option(
        name="end_date",
        description="end date",
        option_type=3,
        required=False,
    )
    async def chatdata(self, ctx, days: str = 5, start_date: str = None, end_date: str = None):
        """
        command allows you to count messages over a specified number of days
        """
        server_id = str(ctx.guild.id)
        imfp = f"chatdata{days}.png"
        file_path = os.path.join(os.getcwd(), f"data/{server_id}", imfp)
        if not os.path.exists(os.path.join(os.getcwd(), f"data/{server_id}")):
            os.mkdir(os.path.join(os.getcwd(), f"data/{server_id}"))

        start_date = start_date if start_date else self.todaydate - datetime.timedelta(days=int(days))
        end_date =  end_date if end_date else self.todaydate

        counts = self.check_cached(start_date.date(), end_date.date())
        dates = [start_date + datetime.timedelta(days=i) for i in range(int(days) + 1)]
        date_strs = [
            (
                (end_date.strftime("%m/%d/%Y")).translate(
                    str.maketrans("", "", string.punctuation)
                )
            ).replace("20", "")
            for end_date in dates
        ]

        await ctx.respond(
            f"gathering daily chat data from {start_date.date()} to {end_date.date()}",
            ephemeral=True,
        )

        if counts == None:
            counter = collections.Counter()
            allchannels = ctx.guild.text_channels

            for channel in allchannels:
                messages = await channel.history(start_date=None, after=start_date).flatten()
                for message in messages:
                    counter[message.created_at.date()] += 1

            counts = [counter[date.date()] for date in dates]
            self.cache_message_data(counts, dates)

        self.graph_handler(counts, file_path, days, date_strs, ctx)



def setup(bot):
    bot.add_cog(chat_data(bot))
