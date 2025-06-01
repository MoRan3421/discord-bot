import discord
import psutil
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        latency = round(self.bot.latency * 1000)
        cpu = psutil.cpu_percent(interval=1)
        await ctx.send(f"🏓 延迟: {latency}ms | CPU 使用率: {cpu}%")

    @discord.app_commands.command(name="ping", description="获取延迟和CPU使用率")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        cpu = psutil.cpu_percent(interval=1)
        await interaction.response.send_message(f"🏓 Pong! 延迟: {latency}ms | CPU 使用率: {cpu}%")

    async def cog_load(self):
        self.bot.tree.add_command(self.ping_slash)

async def setup(bot):
    await bot.add_cog(Ping(bot))
