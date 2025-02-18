import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import cast

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("DISCORD_TOKEN not set in environment.")
TOKEN: str = cast(str, token)

BOT_PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    if bot.user is None:
        raise ValueError("bot.user is None after ready")
    print(f"Logged in as {bot.user.name}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
