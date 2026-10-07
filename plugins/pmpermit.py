"""
PM Permit Plugin - Protect your inbox
"""

import json
import os
from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from config import PM_PERMIT, MAX_PM_FLOOD, DATA_DIR, CMD_PREFIX, OWNER_ID
from utils.helpers import edit_or_reply, command_pattern, is_owner

APPROVED_FILE = os.path.join(DATA_DIR, "approved_users.json")
WARN_COUNT = {}


def load_approved():
    if os.path.exists(APPROVED_FILE):
        with open(APPROVED_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_approved(approved):
    with open(APPROVED_FILE, "w") as f:
        json.dump(list(approved), f)


APPROVED = load_approved()


def register(client):
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def pm_handler(event):
        if not PM_PERMIT:
            return
        sender = await event.get_sender()
        if sender.bot or sender.is_self:
            return
        if sender.id in APPROVED or (OWNER_ID and sender.id == OWNER_ID):
            return

        uid = sender.id
        WARN_COUNT[uid] = WARN_COUNT.get(uid, 0) + 1

        if WARN_COUNT[uid] == 1:
            await event.reply(
                f"**👋 Hello!**\n\n"
                f"This is an automated message from **Tanya UserBot**.\n"
                f"Please wait for the user to approve you.\n\n"
                f"Do not spam, or you will be blocked.\n"
                f"**Warnings:** 1/{MAX_PM_FLOOD}"
            )
        elif WARN_COUNT[uid] >= MAX_PM_FLOOD:
            await event.reply("**🚫 You have been blocked for spamming.**")
            await client(BlockRequest(uid))
            WARN_COUNT.pop(uid, None)

    @client.on(command_pattern("approve(?: |$)(.*)"))
    async def approve(event):
        if event.is_private:
            user_id = event.chat_id
        elif event.is_reply:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        else:
            args = event.pattern_match.group(1).strip()
            if not args:
                return await edit_or_reply(event, "❌ Reply or provide user ID")
            try:
                user = await event.client.get_entity(args)
                user_id = user.id
            except Exception:
                return await edit_or_reply(event, "❌ User not found")

        APPROVED.add(user_id)
        save_approved(APPROVED)
        WARN_COUNT.pop(user_id, None)
        await edit_or_reply(event, f"**✅ Approved** user `{user_id}`")

    @client.on(command_pattern("disapprove(?: |$)(.*)"))
    async def disapprove(event):
        if event.is_private:
            user_id = event.chat_id
        elif event.is_reply:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        else:
            return await edit_or_reply(event, "❌ Reply to user")

        APPROVED.discard(user_id)
        save_approved(APPROVED)
        await edit_or_reply(event, f"**❌ Disapproved** user `{user_id}`")

    @client.on(command_pattern("block(?: |$)(.*)"))
    async def block_user(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        elif event.is_private:
            user_id = event.chat_id
        else:
            return await edit_or_reply(event, "❌ Reply or use in PM")
        await client(BlockRequest(user_id))
        APPROVED.discard(user_id)
        save_approved(APPROVED)
        await edit_or_reply(event, f"**🚫 Blocked** `{user_id}`")

    @client.on(command_pattern("unblock(?: |$)(.*)"))
    async def unblock_user(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        else:
            args = event.pattern_match.group(1).strip()
            if not args:
                return await edit_or_reply(event, "❌ Provide user")
            try:
                user = await event.client.get_entity(args)
                user_id = user.id
            except Exception:
                return await edit_or_reply(event, "❌ User not found")
        await client(UnblockRequest(user_id))
        await edit_or_reply(event, f"**✅ Unblocked** `{user_id}`")
