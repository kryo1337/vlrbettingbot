import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_BETS = os.getenv("API_BETS", "http://scraper:8000/bets")


class Bets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bets", description="Check your active bets")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def bets(self, interaction: discord.Interaction):
        username = interaction.user.name
        try:
            async with httpx.AsyncClient() as client:
                url = f"{API_BETS}/{username}"
                response = await client.get(url, timeout=10.0)
                if response.status_code != 200:
                    await interaction.response.send_message(
                        "Failed to fetch your bets."
                    )
                    return
                data = response.json()

            bets_list = data.get("data", [])
            if not bets_list:
                message = f"{username} has no active bets."
            else:
                message = f"**Active Bets for {username}:**\n"
                for bet in bets_list:
                    message += (
                        f"Bet ID {bet.get('bet_id')}: "
                        f"Event: {bet.get('event')}, "
                        f"Match ID: {bet.get('match_id')}, "
                        f"Predicted Winner: {bet.get('predicted_winner')}, "
                        f"Score: {bet.get('predicted_result')}\n"
                    )
            await interaction.response.send_message(message)
        except Exception as e:
            print(f"[ERROR] /bets command error: {e}")
            await interaction.response.send_message(
                "An error occurred while fetching your bets."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Bets(bot))
