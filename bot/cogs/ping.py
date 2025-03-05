import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_UPCOMING = os.getenv("API_UPCOMING", "http://scraper:8000/upcoming")
API_LIVE = os.getenv("API_LIVE", "http://scraper:8000/live")
API_RESULTS = os.getenv("API_RESULTS", "http://scraper:8000/results")


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def update_data(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(API_UPCOMING, timeout=10.0)
                if response.status_code == 200:
                    print("Successfully updated upcoming matches data")
                else:
                    print(f"Failed to update upcoming matches: {response.status_code}")
                # Uncomment these if you want to update these as well:
                # response = await client.get(API_LIVE, timeout=10.0)
                # if response.status_code == 200:
                #     print("Successfully updated live scores data")
                # else:
                #     print(f"Failed to update live scores: {response.status_code}")
                #
                # response = await client.get(API_RESULTS, timeout=10.0)
                # if response.status_code == 200:
                #     print("Successfully updated match results data")
                # else:
                #     print(f"Failed to update match results: {response.status_code}")
            except Exception as e:
                print(f"Error updating data on startup: {e}")

    @app_commands.command(
        name="ping", description="Check bot responsiveness and update data"
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.update_data()
        await interaction.response.send_message("Pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
