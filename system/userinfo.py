import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_userinfo_embed(self, target: discord.Member, requester: discord.abc.User) -> discord.Embed:
        embed = discord.Embed(
            title=f"🌸 {target.display_name} 的信息卡",
            description="来看一下这位可爱的成员吧 ✨",
            color=0xFFB6C1
        )

        embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
        embed.add_field(name="🆔 用户 ID", value=target.id, inline=True)
        embed.add_field(name="🤖 是机器人吗", value=str(target.bot), inline=True)
        embed.add_field(name="🎀 显示昵称", value=target.display_name, inline=True)

        if target.joined_at:
            embed.add_field(name="📅 加入服务器时间", value=target.joined_at.strftime("%Y-%m-%d %H:%M"), inline=True)
        else:
            embed.add_field(name="📅 加入服务器时间", value="未知", inline=True)

        embed.add_field(name="📆 加入 Discord 时间", value=target.created_at.strftime("%Y-%m-%d %H:%M"), inline=True)

        roles = [role.mention for role in target.roles if role.name != "@everyone"]
        embed.add_field(name="💞 拥有的身份组", value=", ".join(roles) if roles else "无", inline=False)

        footer_text = f"请求者：{requester.display_name} | © 2025 神殿 ✨"
        if requester.avatar:
            embed.set_footer(text=footer_text, icon_url=requester.avatar.url)
        else:
            embed.set_footer(text=footer_text)

        return embed

    # Prefix 命令
    @commands.command(name="userinfo")
    async def userinfo_prefix(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = self.create_userinfo_embed(member, ctx.author)
        await ctx.send(embed=embed)

    # Slash 命令
    @discord.app_commands.command(name="userinfo", description="获取成员的信息 ✨")
    @discord.app_commands.describe(member="你想查看的成员")
    async def userinfo_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = self.create_userinfo_embed(member, interaction.user)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
