import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_BETS = os.getenv("API_BETS", "http://scraper:8000/bets")
API_MATCH_TEAMS = os.getenv("API_MATCH_TEAMS", "http://scraper:8000/match/teams")


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
                async with httpx.AsyncClient() as client:
                    for bet in bets_list:
                        match_id = bet.get("match_id")
                        teams_response = await client.get(
                            f"{API_MATCH_TEAMS}/{match_id}", timeout=10.0
                        )
                        if teams_response.status_code == 200:
                            teams_data = teams_response.json().get("data", {})
                            team1 = teams_data.get("team1", "Unknown")
                            team2 = teams_data.get("team2", "Unknown")
                            teams_str = f"{team1} vs {team2}"
                        else:
                            teams_str = f"Match ID: {match_id}"

                        message += (
                            f"Bet {bet.get('bet_id')}: "
                            f"Event: {bet.get('event')}, "
                            f"Teams: {teams_str}, "
                            f"Predicted Winner: {bet.get('predicted_winner')}, "
                            f"Score: {bet.get('predicted_result')}, "
                            f", Top Frag: {bet.get('predicted_top_frag')}\n"
                        )
            await interaction.response.send_message(message)
        except Exception as e:
            print(f"[ERROR] /bets command error: {e}")
            await interaction.response.send_message(
                "An error occurred while fetching your bets."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Bets(bot))
