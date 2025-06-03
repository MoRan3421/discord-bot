import discord
from discord.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_serverinfo_embed(self, guild: discord.Guild, requester: discord.abc.User) -> discord.Embed:
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        emoji_count = len(guild.emojis)

        embed = discord.Embed(
            title=f"🌸 {guild.name} 的服务器信息",
            description="这里是我们温馨的小窝 ✨",
            color=0xFF69B4
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="🆔 服务器 ID", value=guild.id, inline=True)
        embed.add_field(name="👑 服务器拥有者", value=guild.owner.mention, inline=True)
        embed.add_field(name="📅 创建时间", value=guild.created_at.strftime("%Y-%m-%d %H:%M"), inline=True)

        embed.add_field(name="👥 成员数", value=f"总数：{guild.member_count}\n👤 人类：{humans}\n🤖 机器人：{bots}", inline=True)
        embed.add_field(name="📚 频道数量", value=f"文字：{text_channels}\n语音：{voice_channels}", inline=True)
        embed.add_field(name="🚀 Boost", value=f"等级：{guild.premium_tier}\n次数：{guild.premium_subscription_count}", inline=True)

        embed.add_field(name="🎭 身份组数量", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="🎨 Emoji 数量", value=str(emoji_count), inline=True)
        embed.set_footer(text=f"由 {requester.display_name} 请求 💖 | © 2025 神殿")

        return embed

    @commands.command(name="serverinfo")
    async def serverinfo_prefix(self, ctx):
        embed = self.create_serverinfo_embed(ctx.guild, ctx.author)
        await ctx.send(embed=embed)

    @discord.app_commands.command(name="serverinfo", description="查看当前服务器的信息")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        embed = self.create_serverinfo_embed(interaction.guild, interaction.user)
        await interaction.response.send_message(embed=embed)

    #async def cog_load(self):
        #self.bot.tree.add_command(self.serverinfo_slash)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
