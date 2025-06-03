import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import sqlite3
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import calendar
import random

def generate_cute_background(width=500, height=220):
    base = Image.new('RGBA', (width, height), (255, 182, 193, 255))  # 粉色底
    draw = ImageDraw.Draw(base)

    # 纵向渐变
    for y in range(height):
        r = 255
        g = int(182 + (255 - 182) * (y / height))
        b = int(193 + (255 - 193) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # 叠加气泡（半透明圆）
    for _ in range(60):
        radius = random.randint(10, 30)
        x = random.randint(0, width)
        y = random.randint(0, height)
        alpha = random.randint(20, 60)
        circle = Image.new('RGBA', (radius*2, radius*2), (255, 255, 255, 0))
        circle_draw = ImageDraw.Draw(circle)
        circle_draw.ellipse((0, 0, radius*2, radius*2), fill=(255, 192, 203, alpha))
        base.paste(circle, (x - radius, y - radius), circle)

    # 爱心点缀函数
    def draw_heart(draw_obj, x, y, size, fill):
        r = size // 3
        draw_obj.ellipse((x, y, x + 2*r, y + 2*r), fill=fill)
        draw_obj.ellipse((x + r, y, x + 3*r, y + 2*r), fill=fill)
        draw_obj.polygon([(x, y + r), (x + 3*r, y + r), (x + 1.5*r, y + size)], fill=fill)

    # 画几个爱心点缀
    for _ in range(10):
        x = random.randint(0, width - 40)
        y = random.randint(0, height - 40)
        size = random.randint(20, 40)
        draw_heart(draw, x, y, size, (255, 105, 180, 100))

    # 模糊背景让画面柔和
    base = base.filter(ImageFilter.GaussianBlur(radius=1))

    return base

class DailyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("sign_in.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS sign_in (
            user_id INTEGER PRIMARY KEY,
            last_sign DATE,
            total_days INTEGER,
            streak INTEGER,
            points INTEGER DEFAULT 0
        )''')
        self.conn.commit()

    def draw_calendar(self, draw, year, month, signed_days, start_x, start_y):
        cal = calendar.monthcalendar(year, month)
        font = ImageFont.truetype("arial.ttf", 14)
        day_w, day_h = 30, 20
        days_of_week = "一二三四五六日"
        for i, d in enumerate(days_of_week):
            draw.text((start_x + i * day_w + 8, start_y), d, fill=(150, 0, 100), font=font)
        for row_i, week in enumerate(cal):
            for col_i, day in enumerate(week):
                if day == 0:
                    continue
                x = start_x + col_i * day_w
                y = start_y + 20 + row_i * day_h
                if day in signed_days:
                    draw.ellipse((x + 5, y + 3, x + 25, y + 23), fill=(255, 105, 180))
                    draw.text((x + 10, y + 5), str(day), fill="white", font=font)
                else:
                    draw.text((x + 10, y + 5), str(day), fill=(80, 80, 80), font=font)

    async def generate_signin_card(self, user, total_days, streak, points, signed_dates):
        width, height = 500, 220
        card = generate_cute_background(width, height).convert("RGBA")
        draw = ImageDraw.Draw(card)
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_text = ImageFont.truetype("arial.ttf", 20)

        bot_avatar_url = str(self.bot.user.display_avatar.url)
        async with aiohttp.ClientSession() as session:
            async with session.get(bot_avatar_url) as resp:
                avatar_bytes = await resp.read()
        avatar = Image.open(io.BytesIO(avatar_bytes)).resize((100, 100)).convert("RGBA")
        card.paste(avatar, (20, 60), avatar)

        draw.text((140, 30), f"{user.name} 的签到卡", font=font_title, fill=(255, 105, 180))
        draw.text((140, 80), f"🎉 总签到：{total_days} 天", font=font_text, fill=(80, 80, 80))
        draw.text((140, 110), f"🔥 连续签到：{streak} 天", font=font_text, fill=(80, 80, 80))
        draw.text((140, 140), f"⭐ 当前积分：{points} 分", font=font_text, fill=(80, 80, 80))

        now = datetime.utcnow()
        year = now.year
        month = now.month
        self.draw_calendar(draw, year, month, signed_dates, 140, 170)

        buffer = io.BytesIO()
        card.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def get_user_signed_dates(self, user_id, year, month):
        self.c.execute("SELECT last_sign FROM sign_in WHERE user_id = ?", (user_id,))
        row = self.c.fetchone()
        if not row:
            return []
        last_sign_date = row[0]
        if not last_sign_date:
            return []

        today = datetime.utcnow().date()
        if year == today.year and month == today.month:
            self.c.execute("SELECT streak FROM sign_in WHERE user_id = ?", (user_id,))
            streak = self.c.fetchone()
            if streak:
                streak_days = streak[0]
                start_day = max(1, today.day - streak_days + 1)
                return list(range(start_day, today.day + 1))
        return []

    async def handle_sign_in(self, user):
        user_id = user.id
        today = datetime.utcnow().date()

        self.c.execute("SELECT last_sign, total_days, streak, points FROM sign_in WHERE user_id = ?", (user_id,))
        result = self.c.fetchone()

        if result:
            last_sign, total_days, streak, points = result
            last_sign_date = datetime.strptime(last_sign, "%Y-%m-%d").date()
            if last_sign_date == today:
                return False, "你今天已经签到过啦，明天再来哦~", None

            if last_sign_date == today - timedelta(days=1):
                streak += 1
            else:
                streak = 1

            total_days += 1
            reward = 10 + (streak // 5) * 5
            points += reward

            self.c.execute("UPDATE sign_in SET last_sign = ?, total_days = ?, streak = ?, points = ? WHERE user_id = ?",
                          (today, total_days, streak, points, user_id))
        else:
            total_days = 1
            streak = 1
            points = 10
            reward = 10
            self.c.execute("INSERT INTO sign_in (user_id, last_sign, total_days, streak, points) VALUES (?, ?, ?, ?, ?)",
                          (user_id, today, total_days, streak, points))

        self.conn.commit()

        signed_dates = self.get_user_signed_dates(user_id, today.year, today.month)
        card_image = await self.generate_signin_card(user, total_days, streak, points, signed_dates)
        return True, f"签到成功！你获得了 {reward} 积分！🎉", card_image

    @commands.command(name="签到")
    async def sign_in_command(self, ctx):
        success, msg, card_image = await self.handle_sign_in(ctx.author)
        if not success:
            await ctx.send(msg)
            return
        file = discord.File(fp=card_image, filename="signin_card.png")
        await ctx.send(content=msg, file=file)

    # 新增 slash command
    @discord.app_commands.command(name="签到", description="每日签到，获得积分和奖励卡片")
    async def sign_in_slash(self, interaction: discord.Interaction):
        success, msg, card_image = await self.handle_sign_in(interaction.user)
        if not success:
            await interaction.response.send_message(msg, ephemeral=True)
            return
        file = discord.File(fp=card_image, filename="signin_card.png")
        await interaction.response.send_message(content=msg, file=file)

    @commands.Cog.listener()
    async def on_ready(self):
        print("DailyCog 已加载")

async def setup(bot: commands.Bot):
    await bot.add_cog(DailyCog(bot))
