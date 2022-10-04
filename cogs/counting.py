import discord
from discord.ext import commands


class Counting(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        if message.channel.id != 1026989117935980665:
            return

        if not message.content.isnumeric():
            return


def setup(bot):
    bot.add_cog(Counting(bot))
