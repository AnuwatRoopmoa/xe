import config
from nextcord.ext import commands
from nextcord import Embed, __version__
from datetime import datetime, timezone
from humanize import intcomma
import asyncio

# ใช้ datetime.now(timezone.utc) แทน datetime.utcnow()
start_time = datetime.now(timezone.utc)

class Botinfo(commands.Cog):
    def __init__(self, React: commands.Bot):
        self.React = React

    @commands.command()
    async def botinfo(self, ctx: commands.Context):
        # สร้าง Embed พร้อมสีหลักและไอคอน
        embed = Embed(
            colour=0x9b59b6,  # เปลี่ยนเป็นสีม่วงที่เข้ากัน
            title="✨ ข้อมูลของบอท ✨",
            description="ข้อมูลเกี่ยวกับบอทและการทำงานในขณะนี้"
        )
        
        # เพิ่มไอคอนและแบนเนอร์ให้กับบอท
        embed.set_author(name=f"{self.React.user}", icon_url=self.React.user.avatar.url if self.React.user.avatar else self.React.user.default_avatar.url)
        
        # ตั้งเวลาประทับเพื่อให้ตรงตามเวลาปัจจุบัน
        embed.timestamp = datetime.now(timezone.utc)

        # ข้อมูลบอทในรูปแบบช่องต่างๆ พร้อมอิโมจิ
        embed.add_field(
            name="🤖 ชื่อของบอท", value=f"`{self.React.user}`", inline=False
        )
        embed.add_field(
            name="🖥️ จํานวนเซิฟเวอร์",
            value=f"🟢 `{intcomma(len(self.React.guilds))}` เซิฟเวอร์",
            inline=True
        )
        embed.add_field(
            name="👥 สมาชิกทั้งหมด",
            value=f"👤 `{intcomma(len(self.React.users))}` คน",
            inline=True
        )
        embed.add_field(
            name="⏳ เวลาทำงาน", 
            value=f"⏲️ `{str(datetime.now(timezone.utc) - start_time).split('.')[0]}`",
            inline=True
        )
        embed.add_field(
            name="📡 Ping ของบอท",
            value=f"📶 `{round(self.React.latency * 1000)}ms`",
            inline=True
        )
        embed.add_field(
            name="🔧 Nextcord.py เวอร์ชัน",
            value=f"🔷 `Nextcord.py {__version__}`",
            inline=True
        )

        # ตั้ง footer พร้อมข้อมูลผู้เรียกใช้คำสั่ง
        embed.set_footer(text=f"👤 Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        # ตั้งรูปภาพ Thumbnail (รูปโปรไฟล์ของบอท)
        avatar_url = self.React.user.avatar.url if self.React.user.avatar else self.React.user.default_avatar.url
        embed.set_thumbnail(url=avatar_url)

        # ส่ง Embed พร้อมลบข้อความหลังจาก 15 วินาที
        message = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await message.delete()

def setup(React: commands.Bot):
    React.add_cog(Botinfo(React))
