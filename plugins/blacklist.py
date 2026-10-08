"""
Blacklist Plugin - Block certain words
Commands: .addblacklist <word> , .rmblacklist <word> , .blacklist
"""

from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import group_only, errors_handler


def _get_bl_data():
    """Always return a dict: {chat_id: [words]}"""
    data = db.get("blacklist", {})
    if isinstance(data, list):
        data = {}
        db.set("blacklist", data)
    if not isinstance(data, dict):
        data = {}
        db.set("blacklist", data)
    return data


def register(client):
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_group and e.text))
    async def blacklist_watcher(event):
        try:
            if event.sender and (getattr(event.sender, "bot", False) or getattr(event.sender, "is_self", False)):
                return
            text = (event.text or "").lower()
            if not text:
                return
            data = _get_bl_data()
            bl = data.get(str(event.chat_id), [])
            if not isinstance(bl, list):
                return
            for word in bl:
                if word and word in text:
                    try:
                        await event.delete()
                    except Exception:
                        pass
                    break
        except Exception:
            pass

    @client.on(command_pattern("addblacklist"))
    @group_only
    @errors_handler
    async def add_bl(event):
        word = ""
        try:
            word = (event.pattern_match.group(1) or "").strip().lower()
        except Exception:
            pass
        if not word:
            return await edit_or_reply(event, "Usage: `.addblacklist <word>`")
        data = _get_bl_data()
        chat_bl = data.setdefault(str(event.chat_id), [])
        if not isinstance(chat_bl, list):
            chat_bl = []
            data[str(event.chat_id)] = chat_bl
        if word not in chat_bl:
            chat_bl.append(word)
            db.set("blacklist", data)
        await edit_or_reply(event, f"**Added to blacklist:** `{word}`")

    @client.on(command_pattern("rmblacklist"))
    @group_only
    @errors_handler
    async def rm_bl(event):
        word = ""
        try:
            word = (event.pattern_match.group(1) or "").strip().lower()
        except Exception:
            pass
        if not word:
            return await edit_or_reply(event, "Usage: `.rmblacklist <word>`")
        data = _get_bl_data()
        chat_bl = data.get(str(event.chat_id), [])
        if isinstance(chat_bl, list) and word in chat_bl:
            chat_bl.remove(word)
            db.set("blacklist", data)
            await edit_or_reply(event, f"**Removed from blacklist:** `{word}`")
        else:
            await edit_or_reply(event, "Word not in blacklist")

    @client.on(command_pattern("blacklist"))
    @group_only
    @errors_handler
    async def list_bl(event):
        data = _get_bl_data()
        chat_bl = data.get(str(event.chat_id), [])
        if not chat_bl or not isinstance(chat_bl, list):
            return await edit_or_reply(event, "Blacklist is empty")
        text = "**Blacklisted words:**\n\n" + "\n".join(f"• `{w}`" for w in chat_bl)
        await edit_or_reply(event, text)
