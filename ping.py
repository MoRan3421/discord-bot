import discord
import client
import psutil
import time
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # 启用 message_content
bot = commands.Bot(command_prefix="/", intents=intents)
bot = commands.Bot(command_prefix="*", intents=intents)  # 改回普通前缀


@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    cpu_usage = psutil.cpu_percent(interval=1)
async def ping(ctx):
    latency = round(bot.latency * 1000)  # 机器人延迟，毫秒计算
    cpu_usage = psutil.cpu_percent(interval=1)  # 计算CPU使用率
    fps = round(1000 / latency) if latency > 0 else "N/A"  # 以延迟近似FPS

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"📡 **延迟:** {latency}ms\n⚙️ **CPU 使用率:** {cpu_usage}%\n🎮 **近似 FPS:** {fps}",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"请求者: {ctx.author}", icon_url=ctx.author.avatar.url)
    
    await ctx.send(embed=embed)