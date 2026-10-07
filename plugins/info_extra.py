"""Extra Info"""
from telethon.tl.functions.channels import GetFullChannelRequest
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import group_only, errors_handler

def register(client):
    @client.on(command_pattern("chatinfo$"))
    @group_only
    @errors_handler
    async def chat_info(event):
        chat = await event.get_chat()
        text = f"**📊 Chat Info**\n\n**Title:** `{chat.title}`\n**ID:** `{event.chat_id}`\n**Username:** @{getattr(chat, 'username', None) or 'None'}\n"
        try:
            full = await client(GetFullChannelRequest(chat))
            text += f"**Members:** `{full.full_chat.participants_count}`\n**Admins:** `{full.full_chat.admins_count or 'N/A'}`\n**About:** `{full.full_chat.about or 'None'}`\n"
        except: pass
        await edit_or_reply(event, text)

    @client.on(command_pattern("members$"))
    @group_only
    @errors_handler
    async def members_count(event):
        count = bots = deleted = 0
        async for user in client.iter_participants(event.chat_id):
            count += 1
            if user.bot: bots += 1
            if user.deleted: deleted += 1
        await edit_or_reply(event, f"**👥 Members**\nTotal: `{count}` | Bots: `{bots}` | Deleted: `{deleted}` | Humans: `{count-bots-deleted}`")

    @client.on(command_pattern("admins$"))
    @group_only
    @errors_handler
    async def list_admins(event):
        text = "**🛡️ Admins**\n\n"
        i = 1
        async for user in client.iter_participants(event.chat_id, filter="admins"):
            text += f"**{i}.** [{user.first_name}](tg://user?id={user.id})\n"
            i += 1
            if i > 30: break
        await edit_or_reply(event, text)
