import discord
from discord import app_commands
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def botinvite(self, ctx):
        client_id = self.bot.user.id
        permissions = 8
        bot_invite_url = (
            f"https://discord.com/oauth2/authorize"
            f"?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
        )
        group_invite_url = "https://discord.gg/your-server-code"  # 替换为你的服务器链接

        embed = discord.Embed(
            title="💌 邀请 Bot 酱 & 加入官方群组！",
            description="✨ 快来邀请我和加入我们的社区吧！⬇️",
            color=discord.Color.pink()
        )
        embed.add_field(
            name="🤖 邀请 Bot 酱",
            value=f"[点击邀请我到你的服务器]({bot_invite_url})",
            inline=False
        )
        embed.add_field(
            name="🌐 加入官方群组",
            value=f"[点击加入我们！]({group_invite_url})",
            inline=False
        )
        embed.set_footer(text="Bot 酱已经迫不及待要见你啦~ 🐰🎀")

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        await ctx.send(embed=embed)

    @app_commands.command(name="invite", description="获取 Bot 的邀请链接和官方群链接")
    async def invite(self, interaction: discord.Interaction):
        client_id = self.bot.user.id
        permissions = 8
        bot_invite_url = (
            f"https://discord.com/oauth2/authorize"
            f"?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
        )
        group_invite_url = "https://discord.gg/your-server-code"  # 替换为你的服务器链接

        embed = discord.Embed(
            title="💌 邀请 Bot 酱 & 加入官方群组！",
            description="✨ 快来邀请我和加入我们的社区吧！⬇️",
            color=discord.Color.pink()
        )
        embed.add_field(
            name="🤖 邀请 Bot 酱",
            value=f"[点击邀请我到你的服务器]({bot_invite_url})",
            inline=False
        )
        embed.add_field(
            name="🌐 加入官方群组",
            value=f"[点击加入我们！]({group_invite_url})",
            inline=False
        )
        embed.set_footer(text="神殿已经迫不及待要见你啦~ 🐰🎀 | © 2025 神殿")

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Invite(bot))
