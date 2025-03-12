import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_UPCOMING_EVENTS = os.getenv(
    "API_UPCOMING_EVENTS", "http://scraper:8000/upcoming_events"
)
API_LIVE_EVENTS = os.getenv("API_LIVE_EVENTS", "http://scraper:8000/live_events")
API_CREATED = os.getenv("API_CREATED_EVENTS", "http://scraper:8000/created_events")


class AvailableEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="available", description="Display upcoming and live events"
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def available(self, interaction: discord.Interaction):
        await interaction.response.defer()

        async with httpx.AsyncClient() as client:
            upcoming_resp = await client.get(API_UPCOMING_EVENTS, timeout=10.0)
            if upcoming_resp.status_code != 200:
                await interaction.followup.send("Failed to fetch upcoming events.")
                return
            upcoming_data = upcoming_resp.json()

            live_resp = await client.get(API_LIVE_EVENTS, timeout=10.0)
            if live_resp.status_code != 200:
                live_data = {"data": []}
            else:
                live_data = live_resp.json()

            created_resp = await client.get(API_CREATED, timeout=10.0)
            if created_resp.status_code != 200:
                created_events = []
            else:
                created_data = created_resp.json()
                created_events = created_data.get("data", [])

        message = ""
        if "data" in upcoming_data and upcoming_data["data"]:
            message += "**Upcoming Events:**\n"
            for event in upcoming_data["data"]:
                event_name = event.get("event", "Unknown")
                if event_name in created_events:
                    event_name_display = f"{event_name} (created)"
                else:
                    event_name_display = event_name
                message += f"\n**Event:** {event_name_display}\n"
                for match in event.get("matches", []):
                    team1 = match.get("team1", "Unknown")
                    team2 = match.get("team2", "Unknown")
                    time_until = match.get("time_until_match", "Unknown")
                    message += f"- {team1} vs {team2} at {time_until}\n"
        else:
            message += "No upcoming events found.\n"

        if "data" in live_data and live_data["data"]:
            message += "\n**Live Events:**\n"
            for event in live_data["data"]:
                event_name = event.get("event", "Unknown")
                if event_name in created_events:
                    event_name_display = f"{event_name} (created)"
                else:
                    event_name_display = event_name
                event_name_display += " (LIVE 🔴)"
                message += f"\n**Event:** {event_name_display}\n"
                for match in event.get("matches", []):
                    team1 = match.get("team1", "Unknown")
                    team2 = match.get("team2", "Unknown")
                    time_until = match.get("time_until_match", "Unknown")
                    message += f"- {team1} vs {team2} at {time_until}\n"
        else:
            message += "\nNo live events found."

        if len(message) > 2000:
            chunks = [message[i : i + 2000] for i in range(0, len(message), 2000)]
            for chunk in chunks:
                await interaction.followup.send(chunk)
        else:
            await interaction.followup.send(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(AvailableEvents(bot))
