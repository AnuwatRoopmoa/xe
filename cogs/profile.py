from nextcord.ext import commands
from nextcord import Embed

class Profile(commands.Cog):
    def __init__(self, React: commands.Bot):
        self.React = React

    @commands.command()
    async def profile(self, ctx: commands.Context, id: str):
        embed = Embed(
            color=0xFFD06B,
            description="``🕐`` ``|`` กําลังโหลดกรุณารอสักครู่..."
        )
        message = await ctx.reply(embed=embed)
        
        try:
            user = await self.React.fetch_user(int(id))
            
            # ข้อความโปรไฟล์ของผู้ใช้
            embed = Embed(
                color=0x9b59b6,
                description=f"""
> ``✨ Discord``: {str(user)}     
> ``🔥 Discord Tag``: {user.mention}
"""
            )
            embed.set_author(name="DISCORD LOOKUP", icon_url="https://th.bing.com/th/id/R.392ece4a4d04d32c15d030143e762939?rik=ifRK4XdOBR6ZnA&pid=ImgRaw&r=0")
            
            # ตรวจสอบ avatar ของผู้ใช้
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            else:
                embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.sfSekXlCEGWtRXswI6ibjQAAAA?rs=1&pid=ImgDetMain")  # รูปภาพแทนถ้าไม่มี avatar

            # ตรวจสอบ banner ของผู้ใช้
            if user.banner:
                embed.set_image(url=user.banner.url)

            await message.edit(embed=embed)

        except Exception as e:
            # ข้อความกรณีไม่พบไอดีหรือเกิดข้อผิดพลาด
            embed = Embed(
                color=0xFF9193,
                description=f"``❌`` ``|`` ไม่พบดิสคอร์ดไอดี {id} หรือเกิดข้อผิดพลาด: {e}"
            )
            await message.edit(embed=embed)

def setup(React: commands.Bot):
    React.add_cog(Profile(React))
