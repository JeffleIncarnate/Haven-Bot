import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot(debug_guilds=[1021736744451838004])


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.load_extension("cogs.greetings")
bot.load_extension("cogs.roast")

bot.run(os.environ["TOKEN"])
