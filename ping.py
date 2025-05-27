import discord
import client
import psutil
import time
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # 启用 message_content
bot = commands.Bot(command_prefix="/", intents=intents)
bot = commands.Bot(command_prefix="*", intents=intents)  # 改回普通前缀


@bot.tree.command(name="ping", description="查看机器人的延迟和CPU使用率")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # 机器人延迟，毫秒计算
    cpu_usage = psutil.cpu_percent(interval=1)  # 计算CPU使用率
    fps = round(1000 / latency) if latency > 0 else "N/A"  # 以延迟近似FPS

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"📡 **延迟:** {latency}ms\n⚙️ **CPU 使用率:** {cpu_usage}%\n🎮 **近似 FPS:** {fps}",
        color=discord.Color.green()
    )
    embed.set_footer(
        text=f"请求者: {interaction.user}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty
    )

    await interaction.response.send_message(embed=embed)
