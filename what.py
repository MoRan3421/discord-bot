import discord
import os
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

# 完善 .env 文件加载
def load_env_file(path=".env"):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" not in line:
                            print(f"[WARN] .env 文件格式错误：缺少 '=' - {line}")
                            continue
                        key, value = line.split("=", 1)
                        os.environ[key] = value
        except FileNotFoundError:
            print(f"[WARN] 找不到 .env 文件：{path}")
        except Exception as e:
            print(f"[ERROR] 读取 .env 文件出错：{e}")
    else:
        print(f"[WARN] 找不到 .env 文件：{path}")

load_env_file()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("[ERROR] TOKEN 未在 .env 文件中设置")
    exit()  # 终止程序

print("[DEBUG] TOKEN from env:", TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!", "/"), intents=intents) # 可根据需要调整前缀

@bot.event
async def on_ready():
    print(f"✅ Bot 已登录为 {bot.user}（ID: {bot.user.id}）")
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ 同步了 {len(synced)} 个 Slash Commands")
    except Exception as e:
        print(f"❌ 同步 Slash Commands 失败: {e}")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello! I am your friendly bot!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == "hello":
        await message.channel.send("Hello! I am your friendly bot!")

    await bot.process_commands(message)

async def main():
    async with bot:
        try:
            await bot.load_extension("ping")
            await bot.start(TOKEN)
        except discord.LoginFailure:
            print("[ERROR] 无效的 TOKEN，请检查 .env 文件")
        except discord.ExtensionNotFound:
            print("[ERROR] 找不到 'ping' 扩展，请确保文件存在")
        except Exception as e:
            print(f"[ERROR] 启动 Bot 失败：{e}")

if __name__ == "__main__":
    asyncio.run(main())
