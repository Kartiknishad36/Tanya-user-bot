"""
Global Ban Plugin
"""
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import owner_only, errors_handler

async def get_target(event):
    if event.is_reply:
        return await event.client.get_entity((await event.get_reply_message()).sender_id)
    args = event.pattern_match.group(1).strip().split(maxsplit=1)
    if args:
        try: return await event.client.get_entity(args[0])
        except: return None
    return None

def register(client):
    @client.on(command_pattern("gban(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def gban_user(event):
        user = await get_target(event)
        if not user: return await edit_or_reply(event, "❌ Reply or provide user")
        reason = event.pattern_match.group(1).strip()
        db.add_gban(user.id, reason)
        await edit_or_reply(event, f"**🔨 Globally Banned** [{user.first_name}](tg://user?id={user.id})\n**Reason:** {reason or 'No reason'}")
        if event.is_group:
            try:
                await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
            except: pass

    @client.on(command_pattern("ungban(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def ungban_user(event):
        user = await get_target(event)
        if not user: return await edit_or_reply(event, "❌ Reply or provide user")
        if db.remove_gban(user.id):
            await edit_or_reply(event, f"**✅ Removed gban** for [{user.first_name}](tg://user?id={user.id})")
        else:
            await edit_or_reply(event, "❌ User was not gbanned")

    @client.on(command_pattern("gbanlist$"))
    @owner_only
    @errors_handler
    async def gban_list(event):
        gbans = db.get("gbans", [])
        if not gbans: return await edit_or_reply(event, "📭 No global bans.")
        text = f"**🔨 Global Bans ({len(gbans)})**\n\n"
        for i, g in enumerate(gbans[:30], 1):
            text += f"**{i}.** `{g['id']}` - {g.get('reason') or 'No reason'}\n"
        await edit_or_reply(event, text)
