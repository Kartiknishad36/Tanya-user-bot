"""
Notes Plugin
"""
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("save(?: |$)(.*)"))
    @errors_handler
    async def save_note(event):
        args = event.pattern_match.group(1).strip()
        if "|" not in args:
            if event.is_reply and args:
                reply = await event.get_reply_message()
                content = reply.text or ""
                db.add_note(event.chat_id, args, content)
                return await edit_or_reply(event, f"**✅ Note saved:** `{args}`")
            return await edit_or_reply(event, "❌ Usage: `.save <name> | <content>`")
        name, content = args.split("|", 1)
        db.add_note(event.chat_id, name.strip(), content.strip())
        await edit_or_reply(event, f"**✅ Note saved:** `{name.strip()}`")

    @client.on(command_pattern("get(?: |$)(.*)"))
    @errors_handler
    async def get_note(event):
        name = event.pattern_match.group(1).strip()
        content = db.get_note(event.chat_id, name)
        if content:
            await edit_or_reply(event, f"**📝 Note: `{name}`**\n\n{content}")
        else:
            await edit_or_reply(event, f"❌ Note `{name}` not found")

    @client.on(command_pattern("clear(?: |$)(.*)"))
    @errors_handler
    async def clear_note(event):
        name = event.pattern_match.group(1).strip()
        if db.delete_note(event.chat_id, name):
            await edit_or_reply(event, f"**✅ Note deleted:** `{name}`")
        else:
            await edit_or_reply(event, f"❌ Note not found")

    @client.on(command_pattern("notes$"))
    @errors_handler
    async def list_notes(event):
        notes = db.get_all_notes(event.chat_id)
        if not notes: return await edit_or_reply(event, "📭 No notes.")
        text = f"**📝 Notes ({len(notes)})**\n\n" + "\n".join(f"• `{n}`" for n in notes)
        await edit_or_reply(event, text)
