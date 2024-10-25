import config
import os
import asyncio
from logging import getLogger, DEBUG, FileHandler, Formatter
from nextcord import Intents, Status, Streaming
from nextcord.ext import commands
from asyncio import run
from os import listdir

from myserver import server_on


# ตั้งค่าการบันทึก log
logger = getLogger("nextcord")
logger.setLevel(DEBUG)
handler = FileHandler(filename="log/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# ตั้งค่า intents สำหรับบอท
intents = Intents.default()
intents.message_content = True

React = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    help_command=None,
    intents=intents,
    strip_after_prefix=True,
)

os.system('clear')

# ฟังก์ชันโหลด cogs
async def loadcogs():
    for file in listdir("cogs"):
        if file.endswith(".py") and not file.startswith("__COMING__SOON"):
            try:
                React.load_extension(f"cogs.{file[:-3]}")
                print(f"Successfully load {file[:-3]}")
            except Exception as e:
                print(f"Unable to load {file[:-3]} {e}")

# ฟังก์ชันแสดงสถานะบอทออนไลน์
@React.event
async def on_ready():
    print(f"{React.user} is online")
    await React.change_presence(
        status=Status.idle,
        activity=Streaming(
            name="Check FiveM By ....",
            url="https://youtu.be/jxsb69XtGFs?list=RDjxsb69XtGFs",
        ),
    )

@React.event
async def on_message(message):
    if message.author == React.user:
        return

    await React.process_commands(message)
server_on()
if __name__ == "__main__":
    async def start_bot():
        await loadcogs()
        await React.start("TOKEN", reconnect=True)
    run(start_bot())
