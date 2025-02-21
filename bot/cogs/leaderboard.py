import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_LEADERBOARD = os.getenv("API_LEADERBOARD", "http://scraper:8000/leaderboard")
API_CREATED_EVENTS = os.getenv(
    "API_CREATED_EVENTS", "http://scraper:8000/created_events"
)


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="leaderboard",
        description="Display top 10 users with most points for a given event.",
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def leaderboard(self, interaction: discord.Interaction, event_name: str):
        url = f"{API_LEADERBOARD}/{event_name}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                await interaction.response.send_message(
                    "Failed to fetch leaderboard data."
                )
                return
            data = response.json()

        if "data" in data and data["data"]:
            message = f"**Leaderboard for event '{event_name}':**\n"
            for user in data["data"]:
                username = user.get("username", "Unknown")
                points = user.get("points", 0)
                message += f"- **{username}**: {points} points\n"
        else:
            message = f"No leaderboard data found for event '{event_name}'."

        await interaction.response.send_message(message)

    @leaderboard.autocomplete("event_name")
    async def leaderboard_event_name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        async with httpx.AsyncClient() as client:
            response = await client.get(API_CREATED_EVENTS)
            if response.status_code != 200:
                return []
            data = response.json()
        created_events = data.get("data", [])
        choices = [
            app_commands.Choice(name=event, value=event)
            for event in created_events
            if current.lower() in event.lower()
        ]
        return choices[:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
