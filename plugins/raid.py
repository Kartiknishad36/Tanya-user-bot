"""
Raid Plugin - Reply raid on a user
Commands: .raid <count> (reply) , .replyraid , .draid
"""

import asyncio
import random
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.constants import MAX_RAID_COUNT, RAID_ART
from core.decorators import owner_only, errors_handler

RAID_MESSAGES = [
    "Teri maa ki...",
    "Madarchod",
    "Behenchod",
    "Gandu",
    "Chutiya",
    "Bhosdike",
    "Lund",
    "Teri behen ki chut",
    "Raand",
    "Randwa",
    "Chudakkad",
    "Harami",
    "Kamina",
    "Saale",
    "Teri maa ka bhosda",
    "Bhen ke lode",
    "Teri gand mara",
    "Chodu",
    "Lund ke baal",
    "Maa chuda",
]


def register(client):
    @client.on(command_pattern("raid(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def raid_handler(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to the target user")

        args = event.pattern_match.group(1).strip()
        try:
            count = min(int(args) if args else 10, MAX_RAID_COUNT)
        except ValueError:
            count = 10

        reply = await event.get_reply_message()
        target = await event.client.get_entity(reply.sender_id)
        await event.delete()

        await event.respond(f"```{RAID_ART}```\n**Raid started on** [{target.first_name}](tg://user?id={target.id})")

        for i in range(count):
            msg = random.choice(RAID_MESSAGES)
            await reply.reply(f"{msg} [{target.first_name}](tg://user?id={target.id})")
            await asyncio.sleep(0.8)

        await event.respond(f"**Raid completed** ({count} messages)")

    @client.on(command_pattern("replyraid(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def reply_raid(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to target")

        args = event.pattern_match.group(1).strip()
        try:
            count = min(int(args) if args else 5, MAX_RAID_COUNT)
        except ValueError:
            count = 5

        reply = await event.get_reply_message()
        await event.delete()

        for _ in range(count):
            msg = random.choice(RAID_MESSAGES)
            await reply.reply(msg)
            await asyncio.sleep(0.6)

    @client.on(command_pattern("draid(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def delay_raid(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to target")

        args = event.pattern_match.group(1).strip().split()
        count = 10
        delay = 1.0
        if len(args) >= 1:
            try:
                count = min(int(args[0]), MAX_RAID_COUNT)
            except ValueError:
                pass
        if len(args) >= 2:
            try:
                delay = float(args[1])
            except ValueError:
                pass

        reply = await event.get_reply_message()
        await event.delete()

        for _ in range(count):
            await reply.reply(random.choice(RAID_MESSAGES))
            await asyncio.sleep(delay)
