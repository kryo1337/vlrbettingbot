import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_EVENT_MATCHES = os.getenv("API_EVENT_MATCHES", "http://scraper:8000/event")
API_CREATED = os.getenv("API_CREATED_EVENTS", "http://scraper:8000/created_events")


class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="event", description="Display upcoming matches for a given event"
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def event(self, interaction: discord.Interaction, event_name: str):
        await interaction.response.defer()

        encoded_event = quote(event_name.strip())
        url = f"{API_EVENT_MATCHES}/{encoded_event}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code != 200:
                    await interaction.followup.send(
                        f"Failed to fetch upcoming matches for event '{event_name}'."
                    )
                    return
                data = response.json()
        except Exception as e:
            print(f"[ERROR] Fetching matches: {e}")
            await interaction.followup.send("An error occurred while fetching matches.")
            return

        matches = data.get("data", [])
        event_matches = [
            match
            for match in matches
            if event_name.strip().lower()
            in match.get("match_event", "").strip().lower()
        ]

        if not event_matches:
            await interaction.followup.send(
                f"No upcoming matches found for event '{event_name}'."
            )
            return

        message = f"**Upcoming matches for event '{event_name}':**\n"
        for match in event_matches:
            team1 = match.get("team1", "Unknown")
            team2 = match.get("team2", "Unknown")
            time_until = match.get("time_until_match", "Unknown")
            message += f"- {team1} vs {team2} at {time_until}\n"

        await interaction.followup.send(message)

    @event.autocomplete("event_name")
    async def event_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_CREATED, timeout=10.0)
                if response.status_code != 200:
                    return []
                data = response.json()
        except Exception as e:
            print(f"[ERROR] Autocomplete fetch failed: {e}")
            return []
        created_events = data.get("data", [])
        choices = [
            app_commands.Choice(name=event, value=event)
            for event in created_events
            if current.lower() in event.lower()
        ]
        return choices[:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
