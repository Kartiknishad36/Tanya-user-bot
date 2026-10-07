"""
Art & Text Style Plugin
"""
import random
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.constants import FONTS
from core.decorators import errors_handler

ASCII_ARTS = [r"(\(\n ( •_•)\n / >❤️", r"  /\_/\  \n ( o.o ) \n  > ^ <"]

def register(client):
    @client.on(command_pattern("font(?: |$)(.*)"))
    @errors_handler
    async def font_style(event):
        args = event.pattern_match.group(1).strip().split(maxsplit=1)
        if len(args) < 2:
            return await edit_or_reply(event, f"❌ Usage: `.font <style> <text>`\nStyles: {', '.join(FONTS.keys())}")
        style, text = args[0].lower(), args[1]
        if style not in FONTS:
            return await edit_or_reply(event, "❌ Unknown style")
        await edit_or_reply(event, text.translate(FONTS[style]))

    @client.on(command_pattern("ascii$"))
    @errors_handler
    async def ascii_art(event):
        await edit_or_reply(event, f"```{random.choice(ASCII_ARTS)}```")

    @client.on(command_pattern("flip(?: |$)(.*)"))
    @errors_handler
    async def flip_text(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply:
            text = (await event.get_reply_message()).text or ""
        if not text: return await edit_or_reply(event, "❌ Provide text")
        flip_map = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ɐqɔpǝɟƃɥᴉɾʞklɯuodbɹsʇnʋʍxʎz")
        await edit_or_reply(event, text.translate(flip_map)[::-1])

    @client.on(command_pattern("vapor(?: |$)(.*)"))
    @errors_handler
    async def vapor_text(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply: text = (await event.get_reply_message()).text or ""
        if not text: return await edit_or_reply(event, "❌ Provide text")
        await edit_or_reply(event, " ".join(list(text.upper())))

    @client.on(command_pattern("carbon(?: |$)(.*)"))
    @errors_handler
    async def carbon_cmd(event):
        code = event.pattern_match.group(1).strip()
        if not code and event.is_reply: code = (await event.get_reply_message()).text or ""
        if not code: return await edit_or_reply(event, "❌ Provide code")
        lines = code.split("\n")
        result = "```\n" + "\n".join(f"{i:2} │ {l}" for i, l in enumerate(lines[:30], 1)) + "\n```"
        await edit_or_reply(event, f"**♥️ Carbon**\n{result}")
