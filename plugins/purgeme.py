"""Purge Me"""
import asyncio
from utils.helpers import command_pattern
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("purgeme(?: |$)(.*)"))
    @errors_handler
    async def purge_me(event):
        try: count = min(int(event.pattern_match.group(1).strip() or 10), 100)
        except: count = 10
        await event.delete()
        deleted = 0
        async for msg in client.iter_messages(event.chat_id, from_user="me", limit=count):
            try:
                await msg.delete()
                deleted += 1
            except: pass
        try:
            status = await event.respond(f"**🧹 Deleted `{deleted}` messages**")
            await asyncio.sleep(3)
            await status.delete()
        except: pass
