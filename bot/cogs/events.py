import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_EVENT = os.getenv("API_EVENTS", "http://scraper:8000/events")
API_UPCOMING = os.getenv("API_UPCOMING", "http://scraper:8000/upcoming")


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="events", description="Display upcoming events")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def events(self, interaction: discord.Interaction):
        async with httpx.AsyncClient() as client:
            upcoming_response = await client.get(API_UPCOMING)
            if upcoming_response.status_code != 200:
                await interaction.response.send_message(
                    "Failed to update upcoming matches."
                )
                return

            event_response = await client.get(API_EVENT)
            data = event_response.json()

        if "data" in data and data["data"]:
            message = "**Upcoming Events:**\n"
            for event in data["data"]:
                message += f"\n**Event:** {event['event']}\n"
                for match in event["matches"]:
                    team1 = match.get("team1", "Unknown")
                    team2 = match.get("team2", "Unknown")
                    time_until = match.get("time_until_match", "Unknown")
                    message += f"- {team1} vs {team2} at {time_until}\n"
        else:
            message = "No events found."

        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
