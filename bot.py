import os
import sys

# 把当前文件目录加入模块搜索路径，避免找不到cogs
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ 已登录为 {bot.user}")
    print("📦 已加载命令:", [cmd.name for cmd in bot.commands])

# 这里用 setup_hook 异步加载扩展
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.ping")

# 读取 TOKEN.env 文件
with open("TOKEN.env", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)
