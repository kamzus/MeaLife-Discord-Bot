import discord
from discord import app_commands
from discord.ext import commands
import config
from datetime import datetime


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Banuje użytkownika na serwerze.")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Brak podanego powodu"):
        await interaction.response.defer()

        if not interaction.guild.me.guild_permissions.ban_members:
            return await interaction.followup.send("❌ Nie mam uprawnień do banowania!", ephemeral=True)

        ban_time = datetime.utcnow()
        timestamp = int(ban_time.timestamp())

        image_url = "https://media.discordapp.net/attachments/1345303025564254208/1345743110227099739/Photoroom-20250302_140209029.png?ex=67c5a870&is=67c456f0&hm=f663633575da9d3c789c9c77e68891136b3563e26085e7af3285004e2076659a&=&format=webp&quality=lossless&width=663&height=663"

        embed_dm = discord.Embed(
            title="⛔ Zostałeś zbanowany!",
            description=f"Powód: **{reason}**",
            color=discord.Color.red(),
            timestamp=ban_time
        )
        embed_dm.add_field(name="📅 Data i godzina", value=f"<t:{timestamp}:F>", inline=False)
        embed_dm.add_field(name="👮‍♂️ Administrator", value=f"{interaction.user.mention}", inline=False)
        embed_dm.add_field(name="📩 Masz wątpliwości?",
                           value="Uważasz, że ban jest niesłuszny? Skontaktuj się z administratorem lub napisz na: **kontakt@mealife.net**",
                           inline=False)
        embed_dm.set_image(url=image_url)
        embed_dm.set_footer(text=f"Serwer: {interaction.guild.name}", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        try:
            await user.send(embed=embed_dm)
        except discord.Forbidden:
            print(f"⚠️ Nie udało się wysłać wiadomości prywatnej do {user}.")

        await interaction.guild.ban(user, reason=reason)

        embed_command = discord.Embed(
            title="🚫 Użytkownik został zbanowany!",
            color=discord.Color.red(),
            timestamp=ban_time
        )
        embed_command.add_field(name="👤 Użytkownik", value=f"{user.mention} ({user.id})", inline=False)
        embed_command.add_field(name="✏️ Powód", value=reason, inline=False)
        embed_command.add_field(name="👮‍♂️ Administrator", value=f"{interaction.user.mention}", inline=False)
        embed_command.add_field(name="📅 Data i godzina", value=f"<t:{timestamp}:F>", inline=False)
        embed_command.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed_command.set_image(url=image_url)

        await interaction.followup.send(embed=embed_command)

        embed_log = embed_command.copy()
        embed_log.title = "📜 Log: Zbanowano użytkownika"

        log_channel = interaction.guild.get_channel(config.LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed_log)
        else:
            print("⚠️ Kanał logów nie został znaleziony. Sprawdź LOG_CHANNEL_ID w config.py!")


async def setup(bot):
    await bot.add_cog(Ban(bot))
