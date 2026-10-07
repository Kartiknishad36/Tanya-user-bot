"""Locks Plugin"""
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import group_only, errors_handler

LOCK_TYPES = {"msg": "send_messages", "media": "send_media", "sticker": "send_stickers", "gif": "send_gifs", "game": "send_games", "inline": "send_inline", "poll": "send_polls", "invite": "invite_users", "pin": "pin_messages", "info": "change_info"}

def register(client):
    @client.on(command_pattern("lock(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def lock_handler(event):
        lock_type = event.pattern_match.group(1).strip().lower()
        if not lock_type or lock_type not in LOCK_TYPES:
            return await edit_or_reply(event, f"❌ Usage: `.lock <type>`\nTypes: {', '.join(LOCK_TYPES.keys())}")
        rights = ChatBannedRights(until_date=None, **{LOCK_TYPES[lock_type]: True})
        try:
            await client(EditChatDefaultBannedRightsRequest(event.chat_id, rights))
            await edit_or_reply(event, f"**🔒 Locked:** `{lock_type}`")
        except Exception as e:
            await edit_or_reply(event, f"❌ Failed: `{e}`")

    @client.on(command_pattern("unlock(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def unlock_handler(event):
        lock_type = event.pattern_match.group(1).strip().lower()
        if not lock_type or lock_type not in LOCK_TYPES:
            return await edit_or_reply(event, f"❌ Usage: `.unlock <type>`\nTypes: {', '.join(LOCK_TYPES.keys())}")
        rights = ChatBannedRights(until_date=None, **{LOCK_TYPES[lock_type]: False})
        try:
            await client(EditChatDefaultBannedRightsRequest(event.chat_id, rights))
            await edit_or_reply(event, f"**🔓 Unlocked:** `{lock_type}`")
        except Exception as e:
            await edit_or_reply(event, f"❌ Failed: `{e}`")

    @client.on(command_pattern("locks$"))
    @group_only
    @errors_handler
    async def list_locks(event):
        await edit_or_reply(event, "**🔐 Lock Types:**\n" + "\n".join(f"• `{t}`" for t in LOCK_TYPES))
