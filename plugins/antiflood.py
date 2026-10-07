"""Anti Flood Plugin"""
from collections import defaultdict
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import group_only, errors_handler
from core.database import db

flood_count = defaultdict(lambda: defaultdict(int))

def register(client):
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_group))
    async def flood_watcher(event):
        settings = db.get("settings", {})
        limit = settings.get(f"flood_{event.chat_id}", 0)
        if limit <= 0: return
        flood_count[event.chat_id][event.sender_id] += 1
        if flood_count[event.chat_id][event.sender_id] >= limit:
            try:
                await client(EditBannedRequest(event.chat_id, event.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
                await event.reply(f"🔇 **Muted for flooding** (limit: {limit})")
                flood_count[event.chat_id][event.sender_id] = 0
            except: pass

    @client.on(command_pattern("setflood(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def set_flood(event):
        try: limit = int(event.pattern_match.group(1).strip())
        except: return await edit_or_reply(event, "❌ Usage: `.setflood <number>` (0=disable)")
        settings = db.get("settings", {})
        settings[f"flood_{event.chat_id}"] = limit
        db.set("settings", settings)
        await edit_or_reply(event, f"**✅ Flood limit:** `{limit}`" if limit else "**✅ Flood protection disabled**")

    @client.on(command_pattern("flood$"))
    @group_only
    @errors_handler
    async def show_flood(event):
        limit = db.get("settings", {}).get(f"flood_{event.chat_id}", 0)
        await edit_or_reply(event, f"**Current flood limit:** `{limit}` (0=off)")
