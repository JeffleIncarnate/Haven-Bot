import typing

import asyncpg.exceptions
import discord
from discord.ext import commands

from data import return_level


async def check_if_leveling_enabled(guild_id, bot) -> bool:
    res = await bot.conn.fetch(
        "SELECT enabled FROM leveling_core WHERE guild_id=$1",
        guild_id,
    )

    return res[0][0]


async def app_xp_command() -> None:
    ...


async def add_xp_on_message(xp: int, guild_id: int, user_id: int, bot) -> bool:
    if xp is None or guild_id is None or user_id is None:
        # moyai moment, how dare you give me bad input
        return False

    try:
        await bot.conn.execute(
            "UPDATE leveling_vals SET xp=xp+$1 WHERE guild_id=$2 and user_id=$3",
            xp,
            guild_id,
            user_id,
        )
        return True
    except asyncpg.exceptions.UndefinedColumnError:
        return False


async def level_up(guild_id: int, user_id: int, bot) -> bool:
    if guild_id is None or user_id is None or bot is None:
        # moyai moment, how dare you give me bad input
        return False

    try:
        await bot.conn.execute(
            "UPDATE leveling_vals SET level=level+$1 WHERE guild_id=$2 and user_id=$3",
            1,
            guild_id,
            user_id,
        )
        return True
    except asyncpg.exceptions.UndefinedColumnError:
        return False


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_cooldown = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.member)

    def is_member_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        bucket = self.member_cooldown.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        enabled = await check_if_leveling_enabled(message.guild.id, self.bot)

        if not enabled:
            return

        ratelimit = self.is_member_ratelimit(message)

        if ratelimit is not None:
            return

        update_success = await add_xp_on_message(15, message.guild.id, message.author.id, self.bot)

        if not update_success:
            return message.add_reaction("❌")

        xp_res = await self.bot.conn.fetch(
            "SELECT xp FROM leveling_vals WHERE guild_id=$1 and user_id=$2",
            message.guild.id,
            message.author.id,
        )
        total_xp = xp_res[0][0]

        level_calc = await return_level(total_xp)

        level_res = await self.bot.conn.fetch(
            "SELECT level FROM leveling_vals WHERE guild_id=$1 and user_id=$2",
            message.guild.id,
            message.author.id,
        )

        level = level_res[0][0]

        print(level, level_calc)

        if level_calc-1 == level:
            print("Level Up!")
            if await level_up(message.guild.id, message.author.id, self.bot):
                embed = discord.Embed(
                    title="Level Up!",
                    description=f"Good job {message.author.mention} you've leveled up to level {level_calc}"
                )
                channel_id = message.channel.id
                channel = await self.bot.fetch_channel(channel_id)
                await channel.send(embed=embed)

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def reset_xp(self, ctx: discord.Message, member: discord.Member):
        await self.bot.conn.execute(
            "UPDATE leveling_vals SET xp=$1 WHERE guild_id=$2 and user_id=$3",
            0,
            member.guild.id,
            member.id,
        )

        await ctx.respond("Update.")

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def reset_level(self, ctx: discord.Message, member: discord.Member):
        await self.bot.conn.execute(
            "UPDATE leveling_vals SET level=$1 WHERE guild_id=$2 and user_id=$3",
            0,
            member.guild.id,
            member.id,
        )

        await ctx.respond("Update.")


def setup(bot):
    bot.add_cog(Leveling(bot))
