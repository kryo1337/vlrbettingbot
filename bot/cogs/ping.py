import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check bot responsiveness")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
