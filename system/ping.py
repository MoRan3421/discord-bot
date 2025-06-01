import discord
import psutil
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_ping_embed(self, user: discord.abc.User, latency: int) -> discord.Embed:
        # 近似 FPS 计算
        fps = round(1000 / latency) if latency > 0 else "N/A"

        # 根据延迟设置颜色
        if latency < 100:
            color = discord.Color.green()
        elif latency < 200:
            color = discord.Color.gold()
        else:
            color = discord.Color.red()

        embed = discord.Embed(
            title="🏓 Ping 状态",
            description=(
                f"📶 **延迟:** `{latency}ms`\n"
                f"🎮 **近似 FPS:** `{fps}`"
            ),
            color=color
        )

        # Footer: 请求者 + 版权
        footer_text = f"请求者: {user} | © 2025 神殿"
        if user.avatar:
            embed.set_footer(text=footer_text, icon_url=user.avatar.url)
        else:
            embed.set_footer(text=footer_text)

        return embed

    @commands.command(name="ping")
    async def ping_prefix(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = self.create_ping_embed(ctx.author, latency)
        await ctx.send(embed=embed)

    @discord.app_commands.command(name="ping", description="查看延迟和近似 FPS")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = self.create_ping_embed(interaction.user, latency)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
