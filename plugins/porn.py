"""
Dark Video / NSFW Media Plugin
Commands: .porn .darkdl .nsfwdl .vdark .darkvid
Download videos & media (including dark/NSFW content)
"""

import os
import time
import aiohttp
from telethon import events
from utils.helpers import edit_or_reply, command_pattern, humanbytes
from core.decorators import errors_handler, owner_only
from core.theme import FOOTER, LINE

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_file(url: str, path: str, progress_callback=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"HTTP {resp.status}")
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0
            with open(path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        await progress_callback(downloaded, total)
    return path


async def porn_dl_core(client, event, args: str):
    msg = await edit_or_reply(
        event,
        "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "\u2551  \U0001f311 DARK VIDEO DOWNLOAD   \u2551\n"
        "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n"
        "**\u23f3 Processing...**",
    )

    if event.is_reply and not args:
        reply = await event.get_reply_message()
        if not reply.media:
            return await msg.edit("\u274c **Reply to a video / media**")

        start = time.time()
        await msg.edit(
            "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
            "\u2551  \U0001f311 DARK VIDEO DOWNLOAD   \u2551\n"
            "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n"
            "**\U0001f4e5 Downloading...**"
        )
        path = None
        try:
            path = await reply.download_media(file=DOWNLOAD_DIR + "/")
            if not path:
                return await msg.edit("\u274c **Download failed**")
            size = os.path.getsize(path)
            elapsed = round(time.time() - start, 2)
            await event.client.send_file(
                event.chat_id,
                path,
                caption=(
                    "\U0001f311 **Dark Video**\n"
                    f"**Size:** `{humanbytes(size)}`\n"
                    f"**Time:** `{elapsed}s`\n"
                    f"{FOOTER}"
                ),
                supports_streaming=True,
            )
            await msg.delete()
        except Exception as e:
            await msg.edit(f"\u274c **Error:** `{e}`")
        finally:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        return

    if args and (args.startswith("http://") or args.startswith("https://")):
        url = args.split()[0]
        start = time.time()
        filename = url.split("/")[-1].split("?")[0] or f"dark_{int(time.time())}.mp4"
        if not any(filename.lower().endswith(ext) for ext in [".mp4", ".mkv", ".webm", ".mov", ".avi", ".gif"]):
            filename += ".mp4"
        path = os.path.join(DOWNLOAD_DIR, filename)

        await msg.edit(
            "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
            "\u2551  \U0001f311 DARK VIDEO DOWNLOAD   \u2551\n"
            "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n"
            "**\U0001f4e5 Downloading from URL...**"
        )
        try:
            last_edit = [0]

            async def progress(current, total):
                now = time.time()
                if now - last_edit[0] < 2:
                    return
                last_edit[0] = now
                pct = (current / total) * 100 if total else 0
                bar_len = 12
                filled = int(bar_len * current / total) if total else 0
                bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
                try:
                    await msg.edit(
                        "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
                        "\u2551  \U0001f311 DARK VIDEO DOWNLOAD   \u2551\n"
                        "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n"
                        f"**\U0001f4e5 Downloading**\n"
                        f"`[{bar}] {pct:.1f}%`\n"
                        f"**{humanbytes(current)} / {humanbytes(total)}**"
                    )
                except Exception:
                    pass

            await download_file(url, path, progress)
            size = os.path.getsize(path)
            elapsed = round(time.time() - start, 2)
            await event.client.send_file(
                event.chat_id,
                path,
                caption=(
                    "\U0001f311 **Dark Video Downloaded**\n"
                    f"**Source:** [Link]({url})\n"
                    f"**Size:** `{humanbytes(size)}`\n"
                    f"**Time:** `{elapsed}s`\n"
                    f"{FOOTER}"
                ),
                supports_streaming=True,
            )
            await msg.delete()
        except Exception as e:
            await msg.edit(f"\u274c **Failed:** `{e}`")
        finally:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        return

    await msg.edit(
        "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "\u2551  \U0001f311 DARK VIDEO DOWNLOAD   \u2551\n"
        "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n"
        "**Usage:**\n"
        "\u2022 Reply to video \u2192 `.porn` / `.darkdl`\n"
        "\u2022 From URL \u2192 `.porn <url>`\n\n"
        "**Aliases:** `.nsfwdl` `.vdark` `.darkvid`\n"
        f"{FOOTER}"
    )


def register(client):
    @client.on(command_pattern("porn(?: |$)(.*)"))
    @errors_handler
    @owner_only
    async def porn_handler(event):
        args = event.pattern_match.group(1).strip()
        await porn_dl_core(client, event, args)

    @client.on(command_pattern("darkdl(?: |$)(.*)"))
    @errors_handler
    @owner_only
    async def darkdl_handler(event):
        args = event.pattern_match.group(1).strip()
        await porn_dl_core(client, event, args)

    @client.on(command_pattern("nsfwdl(?: |$)(.*)"))
    @errors_handler
    @owner_only
    async def nsfwdl_handler(event):
        args = event.pattern_match.group(1).strip()
        await porn_dl_core(client, event, args)

    @client.on(command_pattern("vdark(?: |$)(.*)"))
    @errors_handler
    @owner_only
    async def vdark_handler(event):
        args = event.pattern_match.group(1).strip()
        await porn_dl_core(client, event, args)

    @client.on(command_pattern("darkvid(?: |$)(.*)"))
    @errors_handler
    @owner_only
    async def darkvid_handler(event):
        args = event.pattern_match.group(1).strip()
        await porn_dl_core(client, event, args)
