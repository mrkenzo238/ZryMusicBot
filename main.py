from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream.input_audio_stream import InputAudioStream
from config import *
import yt_dlp
import os

BOT_NAME = "Zry Music Bot"

app = Client(
    BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)


async def download_audio(query):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.mp3",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
    return "song.mp3"


@app.on_message(filters.command("start") & filters.private)
async def start(_, m: Message):
    await m.reply(f"🎧 **{BOT_NAME} is Alive!**\nUse /play <song>")


@app.on_message(filters.command("play") & filters.group)
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("Song name do!")

    query = m.text.split(None, 1)[1]
    msg = await m.reply("🎵 Downloading...")

    file = await download_audio(query)

    await call.join_group_call(
        m.chat.id,
        InputStream(
            InputAudioStream(
                file
            )
        )
    )

    await msg.edit(f"▶️ **{BOT_NAME}** is playing: {query}")


@app.on_message(filters.command("stop") & filters.group)
async def stop(_, m: Message):
    await call.leave_group_call(m.chat.id)
    await m.reply(f"⏹ **{BOT_NAME}** stopped playing!")


call.start()
app.run()
