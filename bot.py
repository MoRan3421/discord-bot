import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True       # 👈 必须
intents.presences = True     # 👈 必须
intents.guilds = True        # 👈 必须
intents.messages = True      # 👈 必须
intents.emojis = True        # 👈 可选，但推荐
intents.reactions = True     # 👈 可选，但推荐
intents.voice_states = True  # 👈 可选，但推荐

bot = commands.Bot(command_prefix="*", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ 已登录为 {bot.user}")
    print(f"📦 已加载命令: {[cmd.name for cmd in bot.commands]}")

@bot.event
async def setup_hook():
    await bot.load_extension("system.ping")
    await bot.load_extension("system.userinfo")
    await bot.load_extension("system.botinfo")
    await bot.load_extension("system.serverinfo")
    await bot.load_extension("system.invite")  # 根据你的实际路径
    await bot.load_extension("daily.daily")

with open("TOKEN.env", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)
