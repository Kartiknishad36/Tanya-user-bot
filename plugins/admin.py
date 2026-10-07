"""
Admin Tools Plugin - Ban, Kick, Mute, Purge etc.
"""

from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest
from telethon.tl.types import ChatBannedRights, ChatAdminRights
from utils.helpers import edit_or_reply, command_pattern, is_owner


async def get_user(event):
    """Get target user from reply or argument"""
    if event.is_reply:
        reply = await event.get_reply_message()
        return await event.client.get_entity(reply.sender_id)
    args = event.pattern_match.group(1).strip()
    if args:
        try:
            return await event.client.get_entity(args)
        except Exception:
            return None
    return None


def register(client):
    @client.on(command_pattern("ban(?: |$)(.*)"))
    async def ban_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ This command works only in groups!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply to a user or provide username/ID")
        try:
            await event.client(EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=None, view_messages=True)
            ))
            await edit_or_reply(event, f"**Banned** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ Failed: `{e}`")

    @client.on(command_pattern("unban(?: |$)(.*)"))
    async def unban_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ Groups only!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply or provide user")
        try:
            await event.client(EditBannedRequest(
                event.chat_id, user.id,
                ChatBannedRights(until_date=None)
            ))
            await edit_or_reply(event, f"**Unbanned** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("kick(?: |$)(.*)"))
    async def kick_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ Groups only!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply or provide user")
        try:
            await event.client.kick_participant(event.chat_id, user.id)
            await edit_or_reply(event, f"**Kicked** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("mute(?: |$)(.*)"))
    async def mute_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ Groups only!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply or provide user")
        try:
            await event.client(EditBannedRequest(
                event.chat_id, user.id,
                ChatBannedRights(until_date=None, send_messages=True)
            ))
            await edit_or_reply(event, f"**Muted** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("unmute(?: |$)(.*)"))
    async def unmute_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ Groups only!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply or provide user")
        try:
            await event.client(EditBannedRequest(
                event.chat_id, user.id,
                ChatBannedRights(until_date=None)
            ))
            await edit_or_reply(event, f"**Unmuted** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("promote(?: |$)(.*)"))
    async def promote_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ Groups only!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply or provide user")
        try:
            rights = ChatAdminRights(
                add_admins=False,
                invite_users=True,
                change_info=False,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
            )
            await event.client(EditAdminRequest(event.chat_id, user.id, rights, "Admin"))
            await edit_or_reply(event, f"**Promoted** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("demote(?: |$)(.*)"))
    async def demote_user(event):
        if not event.is_group:
            return await edit_or_reply(event, "❌ Groups only!")
        user = await get_user(event)
        if not user:
            return await edit_or_reply(event, "❌ Reply or provide user")
        try:
            rights = ChatAdminRights(add_admins=False)
            await event.client(EditAdminRequest(event.chat_id, user.id, rights, ""))
            await edit_or_reply(event, f"**Demoted** [{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            await edit_or_reply(event, f"❌ `{e}`")

    @client.on(command_pattern("purge(?: |$)(.*)"))
    async def purge_messages(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to a message to start purging from there")
        try:
            reply = await event.get_reply_message()
            messages = []
            async for msg in event.client.iter_messages(
                event.chat_id, min_id=reply.id - 1, reverse=True
            ):
                messages.append(msg.id)
                if len(messages) >= 100:
                    await event.client.delete_messages(event.chat_id, messages)
                    messages = []
            if messages:
                await event.client.delete_messages(event.chat_id, messages)
            await event.delete()
        except Exception as e:
            await edit_or_reply(event, f"❌ Purge failed: `{e}`")

    @client.on(command_pattern("del$"))
    async def delete_msg(event):
        if not event.is_reply:
            return await event.delete()
        reply = await event.get_reply_message()
        await reply.delete()
        await event.delete()

    @client.on(command_pattern("pin$"))
    async def pin_msg(event):
        if not event.is_reply:
            return await edit_or_reply(event, "❌ Reply to a message to pin")
        reply = await event.get_reply_message()
        await reply.pin(notify=True)
        await edit_or_reply(event, "✅ Message pinned!")

    @client.on(command_pattern("unpin$"))
    async def unpin_msg(event):
        await event.client.pin_message(event.chat_id, None)
        await edit_or_reply(event, "✅ All messages unpinned!")
