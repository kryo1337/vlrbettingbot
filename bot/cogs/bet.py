import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
API_BET = os.getenv("API_BET", "http://scraper:8000/bet")
API_EVENT_MATCHES = os.getenv("API_EVENT_MATCHES", "http://scraper:8000/event")
API_CREATED = os.getenv("API_CREATED_EVENTS", "http://scraper:8000/created_events")
API_AVAILABLE_MATCHES = os.getenv(
    "API_AVAILABLE_MATCHES", "http://scraper:8000/available_matches"
)
API_MATCH_TEAMS = os.getenv("API_MATCH_TEAMS", "http://scraper:8000/match/teams")
API_MATCH_PLAYERS = os.getenv("API_MATCH_PLAYERS", "http://scraper:8000/match/players")


class Bet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bet", description="Place a bet on a match")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def bet(
        self,
        interaction: discord.Interaction,
        event: str,
        match_id: int,
        predicted_winner: str,
        predicted_result: str,
        predicted_top_frag: str = None,
    ):
        username = interaction.user.name
        await interaction.response.defer()

        payload = {
            "username": username,
            "match_id": match_id,
            "event": event,
            "predicted_winner": predicted_winner,
            "predicted_result": predicted_result,
            "predicted_top_frag": predicted_top_frag,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(API_BET, json=payload, timeout=10.0)
                if response.status_code != 200:
                    await interaction.followup.send("Failed to place bet.")
                    return
                data = response.json()
            await interaction.followup.send(
                data.get("message", "Bet placed successfully.")
            )
        except Exception as e:
            print(f"[ERROR] /bet command error: {e}")
            await interaction.followup.send("An error occurred while placing your bet.")

    @bet.autocomplete("event")
    async def bet_event_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_CREATED, timeout=10.0)
                if response.status_code != 200:
                    return []
                data = response.json()
            created_events = data.get("data", [])
            choices = [
                app_commands.Choice(name=ev, value=ev)
                for ev in created_events
                if current.lower() in ev.lower()
            ]
            return choices[:25]
        except Exception as e:
            print(f"[ERROR] bet_event_autocomplete: {e}")
            return []

    @bet.autocomplete("match_id")
    async def bet_match_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        event = getattr(interaction.namespace, "event", None)
        if not event:
            return []
        username = interaction.user.name
        encoded_event = quote(event.strip())
        url = f"{API_AVAILABLE_MATCHES}/{username}/{encoded_event}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code != 200:
                    return []
                data = response.json()
            matches = data.get("data", [])
            choices = [
                app_commands.Choice(
                    name=f"ID {match.get('id')} - {match.get('team1')} vs {match.get('team2')} ({match.get('time_until_match')})",
                    value=str(match.get("id")),
                )
                for match in matches
                if current.lower() in str(match.get("id")).lower() or current == ""
            ]
            return choices[:25]
        except Exception as e:
            print(f"[ERROR] bet_match_autocomplete: {e}")
            return []

    @bet.autocomplete("predicted_winner")
    async def bet_winner_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        match_id_str = getattr(interaction.namespace, "match_id", None)
        if not match_id_str:
            return []
        try:
            match_id = int(match_id_str)
        except Exception:
            return []
        url = f"{API_MATCH_TEAMS}/{match_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code != 200:
                    return []
                data = response.json()
            teams_data = data.get("data", {})
            team1 = teams_data.get("team1", "")
            team2 = teams_data.get("team2", "")
            choices = []
            if current.lower() in team1.lower():
                choices.append(app_commands.Choice(name=team1, value=team1))
            if current.lower() in team2.lower():
                choices.append(app_commands.Choice(name=team2, value=team2))
            if not choices:
                choices = [
                    app_commands.Choice(name=team1, value=team1),
                    app_commands.Choice(name=team2, value=team2),
                ]
            return choices[:25]
        except Exception as e:
            print(f"[ERROR] bet_winner_autocomplete: {e}")
            return []

    @bet.autocomplete("predicted_top_frag")
    async def bet_top_frag_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        match_id_str = getattr(interaction.namespace, "match_id", None)
        if not match_id_str:
            return []
        try:
            match_id = int(match_id_str)
        except Exception:
            return []
        url = f"{API_MATCH_PLAYERS}/{match_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code != 200:
                    return []
                data = response.json()
            players = data.get("data", [])
            choices = [
                app_commands.Choice(name=player, value=player)
                for player in players
                if current.lower() in player.lower() or current == ""
            ]
            return choices[:25]
        except Exception as e:
            print(f"[ERROR] bet_top_frag_autocomplete: {e}")
            return []


async def setup(bot: commands.Bot):
    await bot.add_cog(Bet(bot))
