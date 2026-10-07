"""
Utility Commands Plugin
"""

import io
import qrcode
from telethon import events
from utils.helpers import edit_or_reply, command_pattern, humanbytes


def register(client):
    @client.on(command_pattern("id(?: |$)(.*)"))
    async def get_id(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            user = await event.client.get_entity(reply.sender_id)
            text = f"**User ID:** `{user.id}`\n**Chat ID:** `{event.chat_id}`"
        else:
            text = f"**Chat ID:** `{event.chat_id}`\n**Your ID:** `{event.sender_id}`"
        await edit_or_reply(event, text)

    @client.on(command_pattern("info(?: |$)(.*)"))
    async def user_info(event):
        user = None
        if event.is_reply:
            reply = await event.get_reply_message()
            user = await event.client.get_entity(reply.sender_id)
        else:
            args = event.pattern_match.group(1).strip()
            if args:
                try:
                    user = await event.client.get_entity(args)
                except Exception:
                    return await edit_or_reply(event, "❌ User not found")
            else:
                user = await event.client.get_me()

        full = await event.client.get_entity(user.id)
        text = f"""
**👤 User Info**

**Name:** [{full.first_name or ''} {full.last_name or ''}](tg://user?id={full.id})
**Username:** @{full.username or 'None'}
**User ID:** `{full.id}`
**Bot:** `{full.bot}`
**Verified:** `{full.verified}`
**Restricted:** `{full.restricted}`
**Premium:** `{getattr(full, 'premium', False)}`
"""
        await edit_or_reply(event, text)

    @client.on(command_pattern("whois(?: |$)(.*)"))
    async def whois(event):
        await user_info(event)

    @client.on(command_pattern("qr(?: |$)(.*)"))
    async def make_qr(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply:
            reply = await event.get_reply_message()
            text = reply.text or reply.raw_text
        if not text:
            return await edit_or_reply(event, "❌ Provide text or reply to a message")

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        bio = io.BytesIO()
        img.save(bio, "PNG")
        bio.seek(0)
        bio.name = "qrcode.png"
        await event.client.send_file(event.chat_id, bio, caption=f"**QR Code for:**\n`{text[:100]}`")
        await event.delete()

    @client.on(command_pattern("tts(?: |$)(.*)"))
    async def text_to_speech(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply:
            reply = await event.get_reply_message()
            text = reply.text or reply.raw_text
        if not text:
            return await edit_or_reply(event, "❌ Provide text or reply")

        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="en")
            bio = io.BytesIO()
            tts.write_to_fp(bio)
            bio.seek(0)
            bio.name = "tts.mp3"
            await event.client.send_file(event.chat_id, bio, voice_note=True)
            await event.delete()
        except Exception as e:
            await edit_or_reply(event, f"❌ TTS failed: `{e}`")
