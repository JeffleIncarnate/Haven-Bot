import discord
from discord.ext import commands

import operator


class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        res = await self.bot.conn.fetch(
            "SELECT * FROM counting WHERE guild_id=$1", message.guild.id
        )

        channel_id = res[0][1]
        next_num = res[0][5]
        author_id = res[0][4]
        highest_num = res[0][6]

        if int(channel_id) != channel_id:
            return

        if not message.content.isnumeric():
            return

        num_rn = int(message.content)

        if num_rn is not next_num:
            channel = await self.bot.fetch_channel(channel_id)
            await message.add_reaction("❌")
            embed = discord.Embed(
                title=f"{message.author.name}, you've ruined it!",
                description=f"This is a #moyaimoment :moyai:, the next number was supposed to be: `{next_num}`\n "
                f"Counter has been reset to `0`",
                color=discord.Colour.from_rgb(66, 135, 245),
            )
            await self.bot.conn.execute(
                "UPDATE counting SET num_right_now=$1, author_id=$2, next_num=$3 WHERE guild_id=$4",
                0,
                0,
                1,
                message.guild.id,
            )

            if num_rn > highest_num:
                await self.bot.conn.execute(
                    "UPDATE counting SET highest_num=$1 WHERE guild_id=$2",
                    next_num - 1,
                    message.guild.id,
                )

            return await channel.send(embed=embed)

        if message.author.id == author_id:
            channel = await self.bot.fetch_channel(channel_id)
            await message.add_reaction("❌")
            embed = discord.Embed(
                title=f"{message.author.name}, you've ruined it!",
                description=f"This is a #moyaimoment :moyai:, You are not allowed to send a message twice\n"
                f"Counter has been reset to `0`",
                color=discord.Colour.from_rgb(66, 135, 245),
            )
            await self.bot.conn.execute(
                "UPDATE counting SET num_right_now=$1, author_id=$2, next_num=$3 WHERE guild_id=$4",
                0,
                0,
                1,
                message.guild.id,
            )

            if num_rn > highest_num:
                await self.bot.conn.execute(
                    "UPDATE counting SET highest_num=$1 WHERE guild_id=$2",
                    next_num - 1,
                    message.guild.id,
                )

            return await channel.send(embed=embed)

        await self.bot.conn.execute(
            "UPDATE counting SET num_right_now=$1, author_id=$2, next_num=$3 WHERE guild_id=$4",
            num_rn,
            message.author.id,
            num_rn + 1,
            message.guild.id,
        )

        if num_rn == 69:
            channel = await self.bot.fetch_channel(channel_id)
            channel.send("Nice")

        await message.add_reaction("✅")

    @commands.slash_command(description="Get the high score from your server!")
    async def high_score(self, ctx):
        """
        Args:
            ctx

        Returns:
            Embed of the highest counting number for this guild
        """
        res = await self.bot.conn.fetch(
            "SELECT highest_num FROM counting WHERE guild_id=$1", ctx.guild.id
        )

        num = res[0][0]

        embed = discord.Embed(
            title="High score!",
        )

        if num < 50:
            embed.description = f"`{num}`. Wow, you guys suck"
        elif 50 < num < 100:
            embed.description = f"`{num}`. Ok, this is ok"
        elif 100 < num < 200:
            embed.description = f"`{num}`. Alright, you guys are good"
        else:
            embed.description = f"`{num}`. HOLY COW, THIS IS much better than expected"

        await ctx.respond(embed=embed)

    @commands.slash_command(
        description="Gets the top 5 guilds for counting! Including your current place!"
    )
    async def leaderboard(self, ctx):
        """
        Args:
            ctx:

        Returns:
            Leaderboard embed of the highest guilds for counting
        """
        res = await self.bot.conn.fetch("SELECT guild_id, highest_num FROM counting")

        hashmap_of_each_guild = {}
        """
            example: 
            {
                highest_num: guild_id
            }
        """

        for item in res:
            hashmap_of_each_guild[item[1]] = item[0]

        hashmap_of_each_guild = dict(
            sorted(
                hashmap_of_each_guild.items(), key=operator.itemgetter(1), reverse=True
            )
        )
        embed = discord.Embed(
            title="Leaderboard",
            description="",
            color=discord.Colour.from_rgb(66, 135, 245),
        )

        count = 1
        for key, value in hashmap_of_each_guild.items():
            if count >= 5:
                return

            try:
                guild = await self.bot.fetch_guild(value)
                embed.description += (
                    f"**{count}**:   {guild.name} with `{key}` as the highest! \n\n"
                )
            except (
                discord.NotFound,
                discord.HTTPException,
                discord.ApplicationCommandInvokeError,
            ):
                continue

            count += 1

        i = 1
        for key, place in hashmap_of_each_guild.items():
            i += 1
            if ctx.guild.id == place:
                embed.add_field(name="You're place is:", value=f"{i - 1}")

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Counting(bot))
