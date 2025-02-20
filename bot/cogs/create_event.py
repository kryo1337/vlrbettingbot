import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_CREATE = os.getenv("API_CREATE", "http://scraper:8000/event")
API_AVAILABLE = os.getenv("API_AVAILABLE", "http://scraper:8000/available_events")


class CreateEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="create", description="Create a leaderboard for an event."
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def create(self, interaction: discord.Interaction, event_name: str):
        async with httpx.AsyncClient() as client:
            available_resp = await client.get(API_AVAILABLE)
            if available_resp.status_code != 200:
                await interaction.response.send_message(
                    "Failed to fetch available events."
                )
                return
            available_data = available_resp.json()

        available_events = available_data.get("data", [])
        if event_name not in available_events:
            await interaction.response.send_message(
                f"Event '{event_name}' is not available for leaderboard creation. Please check the available events."
            )
            return

        async with httpx.AsyncClient() as client:
            create_resp = await client.post(f"{API_CREATE}/{event_name}")
            if create_resp.status_code != 200:
                await interaction.response.send_message(
                    "Failed to create leaderboard for the event."
                )
                return
            result = create_resp.json()

        await interaction.response.send_message(
            result.get(
                "message", f"Leaderboard for event '{event_name}' created successfully."
            )
        )

    @create.autocomplete("event_name")
    async def event_name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        async with httpx.AsyncClient() as client:
            available_resp = await client.get(API_AVAILABLE)
            if available_resp.status_code != 200:
                return []
            available_data = available_resp.json()
        available_events = available_data.get("data", [])
        choices = [
            app_commands.Choice(name=event, value=event)
            for event in available_events
            if current.lower() in event.lower()
        ]
        return choices[:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(CreateEvent(bot))
