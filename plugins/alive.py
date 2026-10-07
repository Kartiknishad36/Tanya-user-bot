"""
Alive / Ping / Stats plugin
"""

import time
from datetime import datetime
from telethon import events
from config import BOT_NAME, BOT_VERSION, CMD_PREFIX
from utils.helpers import get_system_stats, get_readable_time, edit_or_reply, command_pattern

START_TIME = datetime.now()


def register(client):
    @client.on(command_pattern("alive"))
    async def alive_handler(event):
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        stats = get_system_stats()
        me = await event.client.get_me()

        text = f"""
**🤖 {BOT_NAME} is Alive!**

**Version:** `{BOT_VERSION}`
**User:** [{me.first_name}](tg://user?id={me.id})
**Uptime:** `{uptime}`
**Prefix:** `{CMD_PREFIX}`

**📊 System Stats**
**CPU:** `{stats['cpu']}`
**RAM:** `{stats['ram']}`
**Disk:** `{stats['disk']}`
**Server Uptime:** `{stats['uptime']}`

**Powered by Tanya UserBot ❤️**
"""
        await edit_or_reply(event, text)

    @client.on(command_pattern("ping"))
    async def ping_handler(event):
        start = time.time()
        msg = await edit_or_reply(event, "🏓 Pinging...")
        end = time.time()
        ms = round((end - start) * 1000, 2)
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        await msg.edit(f"**🏓 Pong!**\n\n**Speed:** `{ms} ms`\n**Uptime:** `{uptime}`")

    @client.on(command_pattern("stats"))
    async def stats_handler(event):
        stats = get_system_stats()
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        text = f"""
**📊 System Statistics**

**Bot Uptime:** `{uptime}`
**CPU Usage:** `{stats['cpu']}`
**RAM Usage:** `{stats['ram']}`
**Disk Usage:** `{stats['disk']}`
**Server Uptime:** `{stats['uptime']}`
"""
        await edit_or_reply(event, text)
