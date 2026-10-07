"""
Tag All Plugin - Mention all members in a group
Commands: .tagall , .all , .mentionall
"""

import asyncio
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.constants import MAX_TAGALL
from core.decorators import group_only, errors_handler


def register(client):
    @client.on(command_pattern("tagall(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def tag_all(event):
        text = event.pattern_match.group(1).strip() or "Hello everyone!"
        chat = await event.get_input_chat()
        await edit_or_reply(event, "🔄 Tagging members...")

        mentions = []
        count = 0
        async for user in client.iter_participants(chat):
            if user.bot or user.deleted:
                continue
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")
            count += 1
            if count >= MAX_TAGALL:
                break

        if not mentions:
            return await edit_or_reply(event, "❌ No members found to tag.")

        chunk_size = 5
        for i in range(0, len(mentions), chunk_size):
            chunk = mentions[i:i + chunk_size]
            msg = f"**📢 {text}**\n\n" + " ".join(chunk)
            await event.respond(msg)
            await asyncio.sleep(1.5)

        await event.delete()

    @client.on(command_pattern("all(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def all_alias(event):
        text = event.pattern_match.group(1).strip() or "Attention!"
        event.pattern_match = type("obj", (object,), {"group": lambda self, n: text})()
        await tag_all(event)

    @client.on(command_pattern("admin(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def tag_admins(event):
        text = event.pattern_match.group(1).strip() or "Admins needed!"
        chat = await event.get_input_chat()
        mentions = []
        async for user in client.iter_participants(chat, filter="admins"):
            if user.bot:
                continue
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

        if not mentions:
            return await edit_or_reply(event, "❌ No admins found.")

        msg = f"**🛡️ {text}**\n\n" + " ".join(mentions)
        await edit_or_reply(event, msg)
