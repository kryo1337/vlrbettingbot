import os
import httpx
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

API_EVENT = os.getenv("API_EVENTS", "http://scraper:8000/events")
API_UPCOMING = os.getenv("API_UPCOMING", "http://scraper:8000/upcoming")


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="events")
    async def events(self, ctx):
        async with httpx.AsyncClient() as client:
            upcoming_response = await client.get(API_UPCOMING)
            if upcoming_response.status_code != 200:
                await ctx.send("Failed to update upcoming matches.")
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

        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Events(bot))
