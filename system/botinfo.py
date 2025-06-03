import asyncio
import discord
from discord.ext import commands
import platform
import time
from datetime import timedelta

class BotInfo(commands.Cog):
    BOT_VERSION = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    def get_status_emoji(self, status: discord.Status) -> str:
        status_emojis = {
            discord.Status.online: "🟢 在线",
            discord.Status.idle: "🌙 闲置",
            discord.Status.dnd: "⛔ 勿扰",
            discord.Status.offline: "⚫ 离线",
            discord.Status.invisible: "⚫ 隐身"
        }
        return status_emojis.get(status, "❓ 未知")

    async def create_botinfo_embed(self) -> discord.Embed:
        uptime = str(timedelta(seconds=int(time.time() - self.start_time)))
        total_guilds = len(self.bot.guilds)
        total_users = sum(len(guild.members) for guild in self.bot.guilds)

        status_str = "❓ 未知"
        if self.bot.guilds:
            try:
                guild = self.bot.guilds[0]
                bot_member = guild.get_member(self.bot.user.id)
                if bot_member is None:
                    bot_member = await guild.fetch_member(self.bot.user.id)
                status_str = self.get_status_emoji(bot_member.status)
            except Exception as e:
                print(f"[状态获取失败] {e}")

        embed = discord.Embed(
            title="🤖 神殿 ✨",
            description="你的贴身小助手来报道啦~ 💌",
            color=0xFFB6C1
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.add_field(name="📛 名称", value=self.bot.user.name, inline=True)
        embed.add_field(name="🆔 Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="🧑‍💻 开发者", value="@godking512", inline=True)
        embed.add_field(name="🌐 服务器数", value=str(total_guilds), inline=True)
        embed.add_field(name="👥 服务用户数", value=str(total_users), inline=True)
        embed.add_field(name="🧾 机器人版本", value=self.BOT_VERSION, inline=True)
        embed.add_field(name="📡 当前状态", value=status_str, inline=True)
        embed.add_field(name="📦 使用库", value=f"`discord.py` {discord.__version__}", inline=True)
        embed.add_field(name="💻 运行环境", value=platform.python_version(), inline=True)
        embed.add_field(name="⏱️ 启动时长", value=uptime, inline=True)
        embed.set_footer(text="✨ 来自神殿  | © 2025 神殿 ✨")

        return embed

    @commands.command(name="botinfo")
    async def botinfo_prefix(self, ctx):
        embed = await self.create_botinfo_embed()
        await ctx.send(embed=embed)

    @discord.app_commands.command(name="botinfo", description="查看 Bot 的信息和状态")
    async def botinfo_slash(self, interaction: discord.Interaction):
        embed = await self.create_botinfo_embed()
        try:
            await interaction.response.send_message(embed=embed)
        except (discord.HTTPException, discord.ClientOSError, asyncio.TimeoutError) as e:
            print(f"发送 botinfo 消息失败: {e}")
            try:
                await interaction.followup.send("⚠️ 发送信息时出错，可能是网络问题，请稍后再试。", ephemeral=True)
            except Exception as err:
                print(f"无法发送错误提示消息: {err}")

async def setup(bot):
    await bot.add_cog(BotInfo(bot))




 

