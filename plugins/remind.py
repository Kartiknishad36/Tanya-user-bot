"""Reminder"""
import asyncio
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("remind(?: |$)(.*)"))
    @errors_handler
    async def remind_me(event):
        args = event.pattern_match.group(1).strip().split(maxsplit=1)
        if len(args) < 2: return await edit_or_reply(event, "❌ Usage: `.remind <minutes> <message>`")
        try: minutes = float(args[0])
        except: return await edit_or_reply(event, "❌ Minutes must be number")
        if minutes <= 0 or minutes > 1440: return await edit_or_reply(event, "❌ 0.1 to 1440 minutes only")
        message = args[1]
        await edit_or_reply(event, f"**⏰ Reminder set for {minutes} min**\n`{message}`")
        await asyncio.sleep(minutes * 60)
        try: await event.respond(f"**⏰ Reminder!**\n\n{message}")
        except: pass
