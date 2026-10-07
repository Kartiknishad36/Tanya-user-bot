"""
Media Download / Upload / YouTube Plugin
"""

import os
import time
import asyncio
from telethon import events
from utils.helpers import edit_or_reply, command_pattern, humanbytes, progress


def register(client):
    @client.on(command_pattern("dl$"))
    async def download_media(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to a media message")
        reply = await event.get_reply_message()
        if not reply.media:
            return await edit_or_reply(event, "❌ No media found")

        msg = await edit_or_reply(event, "⬇️ Downloading...")
        start = time.time()
        try:
            path = await reply.download_media(file="data/")
            size = os.path.getsize(path)
            await msg.edit(
                f"**✅ Downloaded Successfully!**\n\n"
                f"**File:** `{os.path.basename(path)}`\n"
                f"**Size:** `{humanbytes(size)}`\n"
                f"**Path:** `{path}`"
            )
        except Exception as e:
            await msg.edit(f"❌ Download failed: `{e}`")

    @client.on(command_pattern("yt(?: |$)(.*)"))
    async def youtube_dl(event):
        url = event.pattern_match.group(1).strip()
        if not url and event.is_reply:
            reply = await event.get_reply_message()
            url = reply.text or reply.raw_text
        if not url or "youtu" not in url:
            return await edit_or_reply(event, "❌ Provide a valid YouTube URL")

        msg = await edit_or_reply(event, "🔍 Fetching YouTube info...")
        try:
            import yt_dlp
            ydl_opts = {
                "format": "best[height<=720]",
                "outtmpl": "data/%(title)s.%(ext)s",
                "quiet": True,
                "noplaylist": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "video")
                await msg.edit(f"⬇️ Downloading **{title}**...")
                ydl.download([url])
                filename = ydl.prepare_filename(info)
                if not os.path.exists(filename):
                    for f in os.listdir("data"):
                        if title[:30] in f:
                            filename = os.path.join("data", f)
                            break

                await event.client.send_file(
                    event.chat_id,
                    filename,
                    caption=f"**🎬 {title}**",
                    supports_streaming=True,
                )
                await msg.delete()
                try:
                    os.remove(filename)
                except Exception:
                    pass
        except Exception as e:
            await msg.edit(f"❌ YouTube download failed:\n`{e}`")

    @client.on(command_pattern("song(?: |$)(.*)"))
    async def download_song(event):
        query = event.pattern_match.group(1).strip()
        if not query:
            return await edit_or_reply(event, "❌ Provide song name")

        msg = await edit_or_reply(event, f"🎵 Searching for **{query}**...")
        try:
            import yt_dlp
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "data/%(title)s.%(ext)s",
                "quiet": True,
                "noplaylist": True,
                "default_search": "ytsearch1",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                if "entries" in info:
                    info = info["entries"][0]
                title = info.get("title", query)
                filename = ydl.prepare_filename(info)

                await event.client.send_file(
                    event.chat_id,
                    filename,
                    caption=f"**🎵 {title}**",
                    supports_streaming=True,
                )
                await msg.delete()
                try:
                    os.remove(filename)
                except Exception:
                    pass
        except Exception as e:
            await msg.edit(f"❌ Song download failed:\n`{e}`")
