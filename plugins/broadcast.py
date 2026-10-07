"""
Broadcast Plugin
"""
import asyncio
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import owner_only, errors_handler

def register(client):
    @client.on(command_pattern("broadcast(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def broadcast(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply: text = (await event.get_reply_message()).text or ""
        if not text: return await edit_or_reply(event, "❌ Provide message")
        msg = await edit_or_reply(event, "📡 Broadcasting...")
        success = failed = 0
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                try:
                    await client.send_message(dialog.id, text)
                    success += 1
                    await asyncio.sleep(0.5)
                except: failed += 1
        await msg.edit(f"**📡 Broadcast Complete**\nSuccess: `{success}` | Failed: `{failed}`")

    @client.on(command_pattern("gcast(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def gcast(event):
        await broadcast(event)
