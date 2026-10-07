"""
AFK Plugin - Away From Keyboard
Commands: .afk <reason> , .unafk
"""

import time
from telethon import events
from utils.helpers import edit_or_reply, command_pattern, get_readable_time
from core.database import db
from core.constants import AFK_DEFAULT
from core.decorators import errors_handler


def register(client):
    @client.on(command_pattern("afk(?: |$)(.*)"))
    @errors_handler
    async def set_afk(event):
        reason = event.pattern_match.group(1).strip() or AFK_DEFAULT
        db.set_afk(event.sender_id, reason)
        await edit_or_reply(
            event,
            f"**💤 AFK Mode Enabled**\n\n**Reason:** {reason}"
        )

    @client.on(command_pattern("unafk$"))
    @errors_handler
    async def remove_afk(event):
        afk_data = db.get_afk(event.sender_id)
        if not afk_data:
            return await edit_or_reply(event, "❌ You are not AFK.")
        duration = get_readable_time(int(time.time() - afk_data.get("time", time.time())))
        db.remove_afk(event.sender_id)
        await edit_or_reply(
            event,
            f"**✅ Welcome back!**\nYou were AFK for `{duration}`"
        )

    @client.on(events.NewMessage(incoming=True))
    async def afk_responder(event):
        if not event.is_private and not event.mentioned:
            if not event.is_reply:
                return
            reply = await event.get_reply_message()
            if not reply or reply.sender_id != (await client.get_me()).id:
                return

        me = await client.get_me()
        afk_data = db.get_afk(me.id)
        if not afk_data:
            return

        if event.sender_id == me.id:
            return

        duration = get_readable_time(int(time.time() - afk_data.get("time", time.time())))
        reason = afk_data.get("reason", AFK_DEFAULT)

        try:
            await event.reply(
                f"**💤 I'm currently AFK**\n\n"
                f"**Reason:** {reason}\n"
                f"**Since:** `{duration}`"
            )
        except Exception:
            pass

    @client.on(events.NewMessage(outgoing=True))
    async def auto_unafk(event):
        me = await client.get_me()
        if db.get_afk(me.id):
            if event.text and event.text.startswith((".", "!", "/", "?")):
                return
            duration = get_readable_time(int(time.time() - db.get_afk(me.id).get("time", time.time())))
            db.remove_afk(me.id)
            try:
                await event.respond(f"**✅ AFK removed** (was away for `{duration}`)")
            except Exception:
                pass
