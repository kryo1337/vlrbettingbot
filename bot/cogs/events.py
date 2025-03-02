import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_CREATED_EVENTS = os.getenv(
    "API_CREATED_EVENTS", "http://scraper:8000/created_events"
)


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="events",
        description="Display events available to bet",
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def created_events(self, interaction: discord.Interaction):
        async with httpx.AsyncClient() as client:
            response = await client.get(API_CREATED_EVENTS)
            if response.status_code != 200:
                await interaction.response.send_message(
                    "Failed to fetch created events."
                )
                return

            data = response.json()

        if "data" in data and data["data"]:
            message = "**Created Events:**\n"
            for event in data["data"]:
                message += f"- {event}\n"
        else:
            message = "No created events found."

        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
