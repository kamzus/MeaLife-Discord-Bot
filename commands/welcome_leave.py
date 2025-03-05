import discord
from discord.ext import commands
import config
from datetime import datetime

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(config.WELCOME_CHANNEL_ID)
        if not channel:
            print("⚠ Kanał powitalny nie został znaleziony. Sprawdź WELCOME_CHANNEL_ID w config.py!")
            return

        join_time = datetime.utcnow()

        embed = discord.Embed(
            title="🎉 Nowy użytkownik!",
            description=f"**{member.mention} dołączył do {member.guild.name}!**\nCieszymy się, że jesteś z nami! 🎊",
            color=discord.Color.green(),
            timestamp=join_time
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Data dołączenia: {join_time.strftime('%Y-%m-%d %H:%M:%S')}",
                         icon_url=member.guild.icon.url if member.guild.icon else None)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = member.guild.get_channel(config.LEAVE_CHANNEL_ID)
        if not channel:
            print("⚠ Kanał pożegnań nie został znaleziony. Sprawdź LEAVE_CHANNEL_ID w config.py!")
            return

        leave_time = datetime.utcnow()

        embed = discord.Embed(
            title="📤 Użytkownik opuścił serwer",
            description=f"**{member.mention} opuścił {member.guild.name}.**\nMamy nadzieję, że jeszcze wrócisz! 😢",
            color=discord.Color.red(),
            timestamp=leave_time
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url) 
        embed.set_footer(text=f"Data opuszczenia: {leave_time.strftime('%Y-%m-%d %H:%M:%S')}",
                         icon_url=member.guild.icon.url if member.guild.icon else None)

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(JoinLeave(bot))
