"""Sudo Plugin"""
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import owner_only, errors_handler
from config import OWNER_ID

def register(client):
    @client.on(command_pattern("addsudo(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def add_sudo(event):
        if event.is_reply:
            user_id = (await event.get_reply_message()).sender_id
        else:
            args = event.pattern_match.group(1).strip()
            if not args: return await edit_or_reply(event, "❌ Reply or provide user ID")
            try: user_id = (await event.client.get_entity(args)).id
            except: return await edit_or_reply(event, "❌ User not found")
        if user_id == OWNER_ID: return await edit_or_reply(event, "❌ Owner already superuser")
        db.add_sudo(user_id)
        await edit_or_reply(event, f"**✅ Added Sudo:** `{user_id}`")

    @client.on(command_pattern("rmsudo(?: |$)(.*)"))
    @owner_only
    @errors_handler
    async def remove_sudo(event):
        if event.is_reply: user_id = (await event.get_reply_message()).sender_id
        else:
            args = event.pattern_match.group(1).strip()
            if not args: return await edit_or_reply(event, "❌ Reply or provide ID")
            try: user_id = int(args)
            except: return await edit_or_reply(event, "❌ Invalid ID")
        db.remove_sudo(user_id)
        await edit_or_reply(event, f"**✅ Removed Sudo:** `{user_id}`")

    @client.on(command_pattern("sudolist$"))
    @owner_only
    @errors_handler
    async def sudo_list(event):
        sudos = db.get("sudo", [])
        if not sudos: return await edit_or_reply(event, "📭 No sudo users.")
        text = f"**👑 Sudo Users ({len(sudos)})**\n\n" + "\n".join(f"**{i}.** `{uid}`" for i, uid in enumerate(sudos, 1))
        await edit_or_reply(event, text)
