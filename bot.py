import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ 已登录为 {bot.user}")
    print(f"📦 已加载命令: {[cmd.name for cmd in bot.commands]}")

@bot.event
async def setup_hook():
    await bot.load_extension("system.ping")


with open("TOKEN.env", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)
