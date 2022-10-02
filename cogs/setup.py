import discord
from discord.ext import commands


class SetupServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Run this command to setup the server")
    async def setup_server(self, guild_id: int, welcome_channel: int):
        pass


def setup(bot):
    bot.add_cog(SetupServer(bot))
