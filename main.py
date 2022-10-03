import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
from rich.progress import Progress
from db import create_pool

load_dotenv()
bot = discord.Bot(debug_guilds=[1026324003444502590], intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(
        activity=discord.Game(f"On {len(bot.guilds)} servers! | /help")
    )
    bot.conn = await create_pool()


def start_bot(client: discord.Bot):
    cogs = []

    all_cogs = list(os.listdir("cogs"))
    for cog in all_cogs:
        if cog.endswith(".py"):
            cogs.append(f"cogs.{cog[:-3]}")

    bot.cog = cogs
    print("\n")

    with Progress() as progress:
        loading_cogs = progress.add_task("[bold green]Loading Cogs", total=len(cogs))
        while not progress.finished:
            for cog in cogs:
                client.load_extension(cog)
                time.sleep(0.1)
                progress.update(
                    loading_cogs,
                    advance=1,
                    description=f"[bold green]Loaded[/] [blue]{cog}[/]",
                )
        progress.update(loading_cogs, description="[bold green]Loaded all cogs")

    time.sleep(0.5)

    client.run(os.environ["TOKEN"])


if __name__ == "__main__":
    start_bot(bot)
