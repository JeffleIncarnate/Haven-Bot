import discord
from discord.ext import commands


class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def reload_cog(self, ctx, cog: str):
        if f"cogs.{cog}" not in self.bot.cog:
            return await ctx.respond("You idiot, it's not a cog")
        self.bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"reloaded {cog}")


def setup(bot):
    bot.add_cog(ReloadCog(bot))
