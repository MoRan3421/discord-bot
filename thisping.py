import discord
from discord import app_commands
from discord.ext import commands
import psutil
import asyncio
from collections import deque

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recent_latencies = deque(maxlen=10)  # 使用 deque 实现更高效的队列

    def smooth_fps(self, latency):
        self.recent_latencies.append(latency)
        if not self.recent_latencies:
            return "N/A"
        
        avg_latency = sum(self.recent_latencies) / len(self.recent_latencies)
        return round(1000 / avg_latency) if avg_latency > 0 else "N/A"

    @app_commands.command(name="ping", description="查看机器人的延迟和CPU使用率")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        fps = self.smooth_fps(latency)

        try:
            cpu_usage = psutil.cpu_percent(interval=1)
        except Exception as e:
            cpu_usage = "N/A"
            print(f"[ERROR] 获取 CPU 使用率失败: {e}")

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"📡 **延迟:** {latency}ms\n⚙️ **CPU 使用率:** {cpu_usage}%\n🎮 **近似 FPS:** {fps}",
            color=discord.Color.green()
        )
        embed.set_footer(
            text=f"请求者: {interaction.user}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
