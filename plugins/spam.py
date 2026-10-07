"""
Spam Plugin - Spam messages (use carefully)
Commands: .spam <count> <text> , .delayspam , .spamreply
"""

import asyncio
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.constants import MAX_SPAM_COUNT
from core.decorators import owner_only, errors_handler


def register(client):
    @client.on(command_pattern("spam(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def spam_handler(event):
        args = event.pattern_match.group(1).strip().split(maxsplit=1)
        if len(args) < 2:
            return await edit_or_reply(
                event,
                f"❌ Usage: `.spam <count> <text>`\nMax count: {MAX_SPAM_COUNT}"
            )

        try:
            count = int(args[0])
        except ValueError:
            return await edit_or_reply(event, "❌ Count must be a number")

        if count > MAX_SPAM_COUNT:
            count = MAX_SPAM_COUNT
        if count < 1:
            return await edit_or_reply(event, "❌ Count must be at least 1")

        text = args[1]
        await event.delete()

        for i in range(count):
            await event.respond(text)
            await asyncio.sleep(0.3)

    @client.on(command_pattern("delayspam(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def delay_spam(event):
        args = event.pattern_match.group(1).strip().split(maxsplit=2)
        if len(args) < 3:
            return await edit_or_reply(
                event,
                "❌ Usage: `.delayspam <count> <delay_seconds> <text>`"
            )
        try:
            count = min(int(args[0]), MAX_SPAM_COUNT)
            delay = float(args[1])
        except ValueError:
            return await edit_or_reply(event, "❌ Invalid numbers")

        text = args[2]
        await event.delete()

        for _ in range(count):
            await event.respond(text)
            await asyncio.sleep(delay)

    @client.on(command_pattern("spamreply(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def spam_reply(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to a message first")

        args = event.pattern_match.group(1).strip().split(maxsplit=1)
        if len(args) < 2:
            return await edit_or_reply(event, "❌ Usage: `.spamreply <count> <text>`")

        try:
            count = min(int(args[0]), MAX_SPAM_COUNT)
        except ValueError:
            return await edit_or_reply(event, "❌ Count must be number")

        text = args[1]
        reply = await event.get_reply_message()
        await event.delete()

        for _ in range(count):
            await reply.reply(text)
            await asyncio.sleep(0.4)

    @client.on(command_pattern("cspam(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def char_spam(event):
        text = event.pattern_match.group(1).strip()
        if not text:
            return await edit_or_reply(event, "❌ Provide text")
        await event.delete()
        for char in text:
            if char.strip():
                await event.respond(char)
                await asyncio.sleep(0.2)
