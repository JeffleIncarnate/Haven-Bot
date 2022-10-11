import discord
from discord.ext import commands


class SetupServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.guild):
        """
        Args:
            guild: discord.Guild (Type)

        Returns:
            None, but does setup tables, so we can just UPDATE them when need be
        """
        await self.bot.change_presence(
            activity=discord.Game(f"On {len(self.bot.guilds)} servers! | /help")
        )

        # For the welcome table
        welcome_vals = {
            "guild_id": guild.id,
            "channel": None,
            "message": None,
            "enabled": False,
        }

        # For the logging table
        logging_vals = {"guild_id": guild.id, "channel": None, "enabled": False}

        # For counting vals
        counting_vals = {
            "guild_id": guild.id,
            "channel": None,
            "enabled": False,
            "num_right_now": 0,
            "author_id": 0,
            "next_num": 1,
            "highest_num": 0,
        }

        # Insert welcome_vals into the welcome table
        await self.bot.conn.execute(
            "INSERT INTO welcome (guild_id, channel, welcome_text, enabled) VALUES ($1, $2, $3, $4);",
            welcome_vals["guild_id"],
            welcome_vals["channel"],
            welcome_vals["message"],
            welcome_vals["enabled"],
        )

        # Insert logging_vals into the logging table
        await self.bot.conn.execute(
            "INSERT INTO logging (guild_id, channel, enabled) VALUES ($1, $2, $3);",
            logging_vals["guild_id"],
            logging_vals["channel"],
            logging_vals["enabled"],
        )

        # Insert counting_vals the counting table
        await self.bot.conn.execute(
            "INSERT INTO counting (guild_id, channel, enabled, num_right_now, author_id, next_num, highest_num) VALUES ($1, $2, $3, $4, $5, $6, $7);",
            counting_vals["guild_id"],
            counting_vals["channel"],
            counting_vals["enabled"],
            counting_vals["num_right_now"],
            counting_vals["author_id"],
            counting_vals["next_num"],
            counting_vals["highest_num"],
        )

    @discord.slash_command(
        description="Run this command to setup welcoming to the server"
    )
    @commands.has_permissions(administrator=True)
    async def setup_welcome(
        self,
        ctx,
        welcome_channel: discord.TextChannel,
        enabled: bool,
        welcome_message: str,
    ):
        vals = {
            "guild_id": ctx.guild.id,
            "channel_id": welcome_channel.id,
            "message": welcome_message,
            "enabled": enabled,
        }

        if vals["guild_id"] is None or vals["channel_id"] is None:
            return ctx.respond("You need to provide a guild id, and channel id.")

        if len(vals["message"]) > 255:
            return ctx.respond(
                f"Message can not be longer than 255 characters, your total characters are {len(vals['message'])}"
            )

        await self.bot.conn.execute(
            "UPDATE welcome SET channel=$1, welcome_text=$2, enabled=$3 WHERE guild_id=$4",
            vals["channel_id"],
            vals["message"],
            vals["enabled"],
            vals["guild_id"],
        )

        if enabled is True:
            embed = discord.Embed(
                title="Setup!",
                description="This message was to confirm that the welcome channel has been setup successfully! Please delete this message.",
            )
            await welcome_channel.send(embed=embed)

        await ctx.respond("Executed successfully!")

    @discord.slash_command(
        description="Run this command to setup logging on the server"
    )
    @commands.has_permissions(administrator=True)
    async def setup_logging(self, ctx, channel: discord.TextChannel, enabled: bool):
        logging_vals = {
            "guild_id": ctx.guild.id,
            "channel": channel.id,
            "enabled": enabled,
        }

        if logging_vals["channel"] is None or logging_vals["enabled"] is None:
            return await ctx.respond(
                "Please provide a channel, and whether the feature is enabled"
            )

        await self.bot.conn.execute(
            "UPDATE logging SET channel=$1, enabled=$2 WHERE guild_id=$3",
            logging_vals["channel"],
            logging_vals["enabled"],
            logging_vals["guild_id"],
        )

        if enabled is True:
            embed = discord.Embed(
                title="Setup!",
                description="This message was to confirm that the logging channel has been setup successfully! Please delete this message.",
            )
            await channel.send(embed=embed)

        await ctx.respond("Executed successfully!")

    @discord.slash_command(
        description="Run this command to setup counting on the server"
    )
    @commands.has_permissions(administrator=True)
    async def setup_counting(self, ctx, channel: discord.TextChannel, enabled: bool):
        counting_vals = {
            "guild_id": ctx.guild.id,
            "channel": channel.id,
            "enabled": enabled,
        }

        if counting_vals["channel"] is None or counting_vals["enabled"] is None:
            return await ctx.respond(
                "Please provide a channel, and whether the feature is enabled"
            )

        await self.bot.conn.execute(
            "UPDATE counting SET channel=$1, enabled=$2 WHERE guild_id=$3",
            counting_vals["channel"],
            counting_vals["enabled"],
            counting_vals["guild_id"],
        )

        if enabled is True:
            embed = discord.Embed(
                title="Setup!",
                description="This message was to confirm that the counting channel has been setup successfully! Please delete this message.",
            )
            await channel.send(embed=embed)

        await ctx.respond("Executed successfully!")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.bot.conn.execute("DELETE FROM welcome WHERE guild_id=$1", guild.id)
        await self.bot.conn.execute("DELETE FROM logging WHERE guild_id=$1", guild.id)
        await self.bot.conn.execute("DELETE FROM counting WHERE guild_id=$1", guild.id)
        await self.bot.change_presence(
            activity=discord.Game(f"On {len(self.bot.guilds)} servers! | /help")
        )

    @discord.slash_command()
    async def welcome_all(self, ctx):
        if ctx.author.id != 624029883626029066:
            return await ctx.respond("You do not have permissions.")

        res = await self.bot.conn.fetch("SELECT * FROM welcome")
        print(res)
        await ctx.respond(res)

    @discord.slash_command()
    async def delete_row(self, ctx, guild_id: str):
        if ctx.author.id != 624029883626029066:
            return await ctx.respond("You do not have permissions.")

        await self.bot.conn.execute(
            "DELETE FROM welcome WHERE guild_id=$1", int(guild_id)
        )
        await ctx.respond("Nice")


def setup(bot):
    bot.add_cog(SetupServer(bot))
