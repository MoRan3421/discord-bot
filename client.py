import discord
import ping
import os


# 创建一个客户端实例
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'已登录为 {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # 防止机器人回复自己

    if message.content.lower() == 'hello':
        await message.channel.send('Hello! I am your friendly bot!')
# 导入所需的库



# 从 TOKEN.txt 文件读取 token
with open("TOKEN.env", "r") as file:
    TOKEN = file.read().strip()

# 运行机器人
client.run(TOKEN)  # 使用实际令牌运行机器人
