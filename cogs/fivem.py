from httpx import get
from nextcord.ext import commands
from nextcord.ui import View,button,Button
from nextcord import Interaction, Embed,ButtonStyle,Member

class FivemButton(View):
    def __init__(self, React: commands.Bot,Member: Member, id:str,did : str,url : str):
        super().__init__(timeout=None)
        self.React = React
        self.Member = Member
        self.did = did
        self.id = id
        self.url = url

    @button(label='ตรวจสอบข้อมูลดิสคอร์ด', style=ButtonStyle.green,emoji="🔎")
    async def lookup(self, button: Button, interaction: Interaction):
        if interaction.user == self.Member:
            user = await self.React.fetch_user(int(self.did))
            embed = Embed(
                color=0x9b59b6,
                description=f"""
> ``✨ Discord``:{str(user)}     
> ``🔥 Discord Tag``:{user.mention}           
"""
            )

            embed.set_author(name="DISCORD LOOKUP",icon_url="https://th.bing.com/th/id/R.392ece4a4d04d32c15d030143e762939?rik=ifRK4XdOBR6ZnA&pid=ImgRaw&r=0")
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)

            if user.banner:
                embed.set_image(url=user.banner.url)
            
            await interaction.message.reply(embed=embed)

    @button(label="ตรวจสอบข้อมูลอีกครั้ง",style=ButtonStyle.blurple,emoji="👑")
    async def retry(self, button: Button, interaction: Interaction):
        if interaction.user == self.Member:
            try:
                users = get(self.url).json()
                if self.id in  [id["id"] for id in users]:
                    for user in users:
                        if user["id"] == id:
                            break
                            
                else:
                    embed = Embed(
                        color=0xFF9193,
                        description= f"``❌`` ``|`` ไม่พบผู้เล่นไอดี {self.id}"
                    )
                    return await interaction.message.reply(
                        embed=embed
                    )

                ping = user["ping"]
                identifiers = user["identifiers"]
                for identifier in identifiers:
                    if identifier.split(":")[0] == "discord":
                        identifier = identifier.split(":")[1]
                        break
            
                formatted_identifiers = "\n".join(identifiers)
                name = user["name"]
                embed = Embed(
                    color=0x9b59b6,
                    description=f"""
> ``⚡ ID`` : {self.id}
> ``🍀 Name`` : {name}
> ``🔧 Ping`` : {ping} ms
> ``🌗 Identifier``

```
{formatted_identifiers}
```
"""
        )       
                embed.set_image(url="")
                embed.set_author(name="FIVEM SERVER PLAYER CHECKER",icon_url="https://i.imgur.com/X7m8J8h.png")
                await interaction.message.reply(embed=embed)

            except:
                embed = Embed(
                    color=0xFF9193,
                    description= "``❌`` ``|`` กรุณาอยู่ในเกมส์ด้วยครับ"
                )
                await interaction.message.reply(
                    embed=embed
                )


class Fivem(commands.Cog):
    def __init__(self, React: commands.Bot):
        self.React = React

    @commands.command()
    async def check(self, ctx: commands.Context, ip : str , port : str, id : str):
        embed = Embed(
            color=0xFFD06B,
            description= "``🕐`` ``|``กําลังโหลดกรุณารอสักครู่..."
        )
        message = await ctx.reply(embed=embed)
        try:
            port = int(port)
            id = int(id)
            url = f'http://{ip}:{port}/players.json'
            users = get(url).json()
        
            all_id = [id["id"] for id in users]
            if id in all_id:
                for user in users:
                    if user["id"] == id:
                        break
            
            else:
                embed = Embed(
                    color=0xFF9193,
                    description= f"``❌`` ``|`` ไม่พบผู้เล่นไอดี {id}"
                )
                return await message.edit(
                    embed=embed
                )

            ping = user["ping"]
            identifiers = user["identifiers"]
            for identifier in identifiers:
                if identifier.split(":")[0] == "discord":
                    identifier = identifier.split(":")[1]
                    break
        
            formatted_identifiers = "\n".join(identifiers)
            name = user["name"]
            embed = Embed(
                color=0x9b59b6,
                description=f"""
> ``⚡ ID`` : {id}
> ``🍀 Name`` : {name}
> ``🔧 Ping`` : {ping} ms
> ``🌗 Identifier``

```
{formatted_identifiers}
```
"""
        )   
            embed.set_author(name="FIVEM SERVER PLAYER CHECKER",icon_url="https://i.imgur.com/X7m8J8h.png")
            embed.set_image(url="")
            await message.edit(embed=embed,view=FivemButton(self.React,ctx.author,id,identifier,url))

        except Exception as e:
            embed = Embed(
                color=0xFF9193,
                description= "``❌`` ``|`` กรุณาอยู่ในเกมส์ด้วยครับ"
            )
            await message.edit(
                embed=embed
            )
def setup(React: commands.Bot):
    React.add_cog(Fivem(React))