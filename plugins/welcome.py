"""
Welcome & Goodbye Plugin
"""
from telethon import events
from utils.helpers import edit_or_reply, command_pattern
from core.database import db
from core.decorators import group_only, errors_handler

def register(client):
    @client.on(events.ChatAction)
    async def welcome_goodbye(event):
        if event.user_joined or event.user_added:
            welcome = db.get("welcome", {}).get(str(event.chat_id))
            if welcome:
                try:
                    user = await event.get_user()
                    text = welcome.format(mention=f"[{user.first_name}](tg://user?id={user.id})", chat=(await event.get_chat()).title, name=user.first_name, id=user.id)
                    await event.reply(text)
                except: pass
        if event.user_left or event.user_kicked:
            goodbye = db.get("goodbye", {}).get(str(event.chat_id))
            if goodbye:
                try:
                    user = await event.get_user()
                    text = goodbye.format(mention=f"[{user.first_name}](tg://user?id={user.id})", chat=(await event.get_chat()).title, name=user.first_name)
                    await event.reply(text)
                except: pass

    @client.on(command_pattern("setwelcome(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def set_welcome(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply: text = (await event.get_reply_message()).text or ""
        if not text: return await edit_or_reply(event, "❌ Provide welcome message. Vars: {mention} {chat} {name} {id}")
        welcomes = db.get("welcome", {})
        welcomes[str(event.chat_id)] = text
        db.set("welcome", welcomes)
        await edit_or_reply(event, f"**✅ Welcome set**\n\n{text}")

    @client.on(command_pattern("setgoodbye(?: |$)(.*)"))
    @group_only
    @errors_handler
    async def set_goodbye(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply: text = (await event.get_reply_message()).text or ""
        if not text: return await edit_or_reply(event, "❌ Provide goodbye message")
        goodbyes = db.get("goodbye", {})
        goodbyes[str(event.chat_id)] = text
        db.set("goodbye", goodbyes)
        await edit_or_reply(event, f"**✅ Goodbye set**\n\n{text}")

    @client.on(command_pattern("clearwelcome$"))
    @group_only
    @errors_handler
    async def clear_welcome(event):
        welcomes = db.get("welcome", {})
        if str(event.chat_id) in welcomes:
            del welcomes[str(event.chat_id)]
            db.set("welcome", welcomes)
            await edit_or_reply(event, "**✅ Welcome cleared**")
        else:
            await edit_or_reply(event, "❌ No welcome set")
