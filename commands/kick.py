import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import config

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Wyrzuca użytkownika z serwera.")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Brak podanego powodu"):
        await interaction.response.defer()

        if not interaction.guild.me.guild_permissions.kick_members:
            return await interaction.followup.send("❌ Nie mam uprawnień do wyrzucania użytkowników!", ephemeral=True)

        kick_time = datetime.utcnow()
        timestamp = int(kick_time.timestamp())

        image_url = "https://media.discordapp.net/attachments/1345303025564254208/1345707676121825361/Photoroom-20250302_114044108.png?ex=67c58770&is=67c435f0&hm=adcdbdc9ca9fc26be9f08fec28dabf23b741195938af5a1c802e2ac067706c71&=&format=webp&quality=lossless&width=663&height=663"

        embed_dm = discord.Embed(
            title="⚠ Zostałeś wyrzucony z serwera!",
            description=f"Powód: **{reason}**",
            color=discord.Color.orange(),
            timestamp=kick_time
        )
        embed_dm.add_field(name="📅 Data i godzina", value=f"<t:{timestamp}:F>", inline=False)
        embed_dm.add_field(name="👮‍♂️ Administrator", value=f"{interaction.user.mention}", inline=False)
        embed_dm.add_field(name="📩 Masz wątpliwości?",
                           value="Uważasz, że wyrzucenie jest niesłuszne? Skontaktuj się z administratorem lub napisz na: **kontakt@mealife.net**",
                           inline=False)
        embed_dm.set_image(url=image_url)
        embed_dm.set_footer(text=f"Serwer: {interaction.guild.name}", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        try:
            await user.send(embed=embed_dm)
        except discord.Forbidden:
            print(f"⚠️ Nie udało się wysłać wiadomości prywatnej do {user}.")

        await interaction.guild.kick(user, reason=reason)

        embed_command = discord.Embed(
            title="🚪 Użytkownik został wyrzucony!",
            color=discord.Color.orange(),
            timestamp=kick_time
        )
        embed_command.add_field(name="👤 Użytkownik", value=f"{user.mention} ({user.id})", inline=False)
        embed_command.add_field(name="✏️ Powód", value=reason, inline=False)
        embed_command.add_field(name="👮‍♂️ Administrator", value=f"{interaction.user.mention}", inline=False)
        embed_command.add_field(name="📅 Data i godzina", value=f"<t:{timestamp}:F>", inline=False)
        embed_command.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed_command.set_image(url=image_url)

        await interaction.followup.send(embed=embed_command)

        embed_log = embed_command.copy()
        embed_log.title = "📜 Log: Wyrzucono użytkownika"

        log_channel = interaction.guild.get_channel(config.LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed_log)
        else:
            print("⚠️ Kanał logów nie został znaleziony. Sprawdź LOG_CHANNEL_ID w config.py!")

async def setup(bot):
    await bot.add_cog(Kick(bot))
