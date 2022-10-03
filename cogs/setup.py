import discord
from discord.ext import commands


class SetupServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.guild):
        vals = {
            "guild_id": guild.id,
            "channel_id": None,
            "message": None,
            "enabled": False,
        }

        await self.bot.conn.execute(
            "INSERT INTO welcome (guild_id, channel, welcome_text, enabled) VALUES ($1, $2, $3, $4);",
            vals["guild_id"],
            vals["channel_id"],
            vals["message"],
            vals["enabled"],
        )

    @discord.slash_command(description="Run this command to setup the server")
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
                description="Delete this message, this was to confirm it worked.",
            )
            await welcome_channel.send(embed=embed)

        await ctx.respond("Executed successfully!")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.bot.conn.execute("DELETE FROM welcome WHERE guild_id=$1", guild.id)

    @discord.slash_command()
    async def welcome_all(self, ctx):
        if ctx.author.id is not 624029883626029066:
            return await ctx.respond("You do not have permissions.")

        res = await self.bot.conn.fetch("SELECT * FROM welcome")
        print(res)
        await ctx.respond(res)

    @discord.slash_command()
    async def delete_row(self, ctx, guild_id: str):
        if ctx.author.id is not 624029883626029066:
            return await ctx.respond("You do not have permissions.")

        await self.bot.conn.execute(
            "DELETE FROM welcome WHERE guild_id=$1", int(guild_id)
        )
        await ctx.respond("Nice")


def setup(bot):
    bot.add_cog(SetupServer(bot))
