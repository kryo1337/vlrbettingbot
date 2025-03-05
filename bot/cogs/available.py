import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_EVENT = os.getenv("API_EVENTS", "http://scraper:8000/events")
API_CREATED = os.getenv("API_CREATED_EVENTS", "http://scraper:8000/created_events")


class Available(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="available", description="Display upcoming events")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def events(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with httpx.AsyncClient() as client:
            event_response = await client.get(API_EVENT)
            if event_response.status_code != 200:
                await interaction.followup.send("Failed to fetch events.")
                return
            events_data = event_response.json()

            created_response = await client.get(API_CREATED)
            if created_response.status_code != 200:
                created_events = []
            else:
                created_data = created_response.json()
                created_events = created_data.get("data", [])

        if "data" in events_data and events_data["data"]:
            message = "**Upcoming Events:**\n"
            for event in events_data["data"]:
                event_name = event["event"]
                if event_name in created_events:
                    event_name_display = f"{event_name} (created)"
                else:
                    event_name_display = event_name
                message += f"\n**Event:** {event_name_display}\n"
                for match in event["matches"]:
                    team1 = match.get("team1", "Unknown")
                    team2 = match.get("team2", "Unknown")
                    time_until = match.get("time_until_match", "Unknown")
                    message += f"- {team1} vs {team2} at {time_until}\n"
        else:
            message = "No events found."

        await interaction.followup.send(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Available(bot))
