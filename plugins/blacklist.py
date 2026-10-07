"""Blacklist Plugin"""
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import group_only, errors_handler

def register(client):
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_group and e.text))
    async def blacklist_watcher(event):
        if event.sender and (event.sender.bot or event.sender.is_self): return
        text = event.text.lower()
        bl = db.get("blacklist", {}).get(str(event.chat_id), [])
        for word in bl:
            if word in text:
                try: await event.delete()
                except: pass
                break

    @client.on(command_pattern("addblacklist(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def add_bl(event):
        word = event.pattern_match.group(1).strip().lower()
        if not word: return await edit_or_reply(event, "❌ Usage: `.addblacklist <word>`")
        data = db.get("blacklist", {})
        chat_bl = data.setdefault(str(event.chat_id), [])
        if word not in chat_bl:
            chat_bl.append(word)
            db.set("blacklist", data)
        await edit_or_reply(event, f"**✅ Blacklisted:** `{word}`")

    @client.on(command_pattern("rmblacklist(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def rm_bl(event):
        word = event.pattern_match.group(1).strip().lower()
        if not word: return await edit_or_reply(event, "❌ Usage: `.rmblacklist <word>`")
        data = db.get("blacklist", {})
        chat_bl = data.get(str(event.chat_id), [])
        if word in chat_bl:
            chat_bl.remove(word)
            db.set("blacklist", data)
            await edit_or_reply(event, f"**✅ Removed:** `{word}`")
        else:
            await edit_or_reply(event, "❌ Word not in blacklist")

    @client.on(command_pattern("blacklist$"))
    @group_only
    @errors_handler
    async def list_bl(event):
        chat_bl = db.get("blacklist", {}).get(str(event.chat_id), [])
        if not chat_bl: return await edit_or_reply(event, "📭 Blacklist empty")
        await edit_or_reply(event, "**🚫 Blacklisted:**\n" + "\n".join(f"• `{w}`" for w in chat_bl))
