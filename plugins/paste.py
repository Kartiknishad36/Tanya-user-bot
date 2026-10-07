"""Paste Plugin"""
import httpx
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("paste(?: |$)(.*)"))
    @errors_handler
    async def paste_cmd(event):
        text = event.pattern_match.group(1).strip()
        if not text and event.is_reply: text = (await event.get_reply_message()).text or ""
        if not text: return await edit_or_reply(event, "❌ Provide text or reply")
        msg = await edit_or_reply(event, "📋 Creating paste...")
        try:
            async with httpx.AsyncClient(timeout=15) as http:
                r = await http.post("https://dpaste.com/api/v2/", data={"content": text, "syntax": "text", "expiry_days": 7})
                if r.status_code in (200, 201):
                    await msg.edit(f"**📋 Paste:** {r.text.strip()}")
                else: await msg.edit("❌ Failed")
        except Exception as e: await msg.edit(f"❌ `{e}`")
