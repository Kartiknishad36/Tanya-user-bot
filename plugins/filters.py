"""
Filters Plugin
"""
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import group_only, errors_handler

def register(client):
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_group and e.text))
    async def filter_handler(event):
        if event.sender and event.sender.bot: return
        text = event.text.lower()
        filters = db.get_filters(event.chat_id)
        for keyword, response in filters.items():
            if keyword in text:
                try: await event.reply(response)
                except: pass
                break

    @client.on(command_pattern("filter(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def add_filter(event):
        args = event.pattern_match.group(1).strip()
        if "|" not in args:
            return await edit_or_reply(event, "❌ Usage: `.filter <keyword> | <response>`")
        keyword, response = args.split("|", 1)
        db.add_filter(event.chat_id, keyword.strip().lower(), response.strip())
        await edit_or_reply(event, f"**✅ Filter saved** `{keyword.strip()}`")

    @client.on(command_pattern("stop(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def stop_filter(event):
        keyword = event.pattern_match.group(1).strip().lower()
        if db.delete_filter(event.chat_id, keyword):
            await edit_or_reply(event, f"**✅ Filter removed:** `{keyword}`")
        else:
            await edit_or_reply(event, f"❌ No filter for `{keyword}`")

    @client.on(command_pattern("filters$"))
    @group_only
    @errors_handler
    async def list_filters(event):
        filters = db.get_filters(event.chat_id)
        if not filters: return await edit_or_reply(event, "📭 No filters.")
        text = f"**📋 Filters ({len(filters)})**\n\n"
        for i, (k, v) in enumerate(filters.items(), 1):
            text += f"**{i}.** `{k}` → {v[:40]}\n"
        await edit_or_reply(event, text)
