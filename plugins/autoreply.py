"""
Auto Reply Plugin
Commands: .autoreply <trigger> | <reply> , .delreply , .listreply
"""

from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import owner_only, errors_handler


def register(client):
    @client.on(events.NewMessage(incoming=True))
    async def auto_reply_handler(event):
        if event.is_private and event.sender and event.sender.bot:
            return
        text = (event.text or "").lower().strip()
        if not text:
            return

        replies = db.get_auto_replies()
        for trigger, response in replies.items():
            if trigger in text:
                try:
                    await event.reply(response)
                except Exception:
                    pass
                break

    @client.on(command_pattern("autoreply(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def add_auto_reply(event):
        args = event.pattern_match.group(1).strip()
        if "|" not in args:
            return await edit_or_reply(
                event,
                "❌ Usage: `.autoreply <trigger> | <reply message>`\n"
                "Example: `.autoreply hello | Hi there! How are you?`"
            )

        trigger, reply = args.split("|", 1)
        trigger = trigger.strip()
        reply = reply.strip()

        if not trigger or not reply:
            return await edit_or_reply(event, "❌ Both trigger and reply are required")

        db.add_auto_reply(trigger, reply)
        await edit_or_reply(
            event,
            f"**✅ Auto Reply Added**\n\n"
            f"**Trigger:** `{trigger}`\n"
            f"**Reply:** `{reply}`"
        )

    @client.on(command_pattern("delreply(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def delete_auto_reply(event):
        trigger = event.pattern_match.group(1).strip()
        if not trigger:
            return await edit_or_reply(event, "❌ Usage: `.delreply <trigger>`")

        if db.delete_auto_reply(trigger):
            await edit_or_reply(event, f"**✅ Deleted auto reply for:** `{trigger}`")
        else:
            await edit_or_reply(event, f"❌ No auto reply found for `{trigger}`")

    @client.on(command_pattern("listreply$"))
    @owner_only
    @errors_handler
    async def list_auto_replies(event):
        replies = db.get_auto_replies()
        if not replies:
            return await edit_or_reply(event, "📭 No auto replies set.")

        text = "**📋 Auto Replies List**\n\n"
        for i, (trigger, reply) in enumerate(replies.items(), 1):
            text += f"**{i}.** `{trigger}` → `{reply[:50]}{'...' if len(reply) > 50 else ''}`\n"

        await edit_or_reply(event, text)
