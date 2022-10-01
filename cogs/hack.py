import discord
from discord.ext import commands
import asyncio
import random


class Hack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="hack someone")
    async def hack(self, ctx, member: discord.Member):
        await ctx.respond(f"Hacking {member.name} now...")
        await asyncio.sleep(1)
        await ctx.edit(content="Getting all personal information...")
        await asyncio.sleep(1)
        await ctx.edit(content="IP address: 192.168.1.69")
        await asyncio.sleep(1)
        await ctx.edit(
            content=f"Injecting trojan virus into discriminator: {member.discriminator}"
        )
        await asyncio.sleep(1)
        await ctx.edit(content="Selling information to the government...")
        await asyncio.sleep(1)
        await ctx.edit(content="Hacking medical records...")
        await ctx.edit(content=f"Successfully hacked {member.mention}")
        await ctx.send(f"{ctx.author.mention} successfully hacked {member.mention}")


def setup(bot):
    bot.add_cog(Hack(bot))
