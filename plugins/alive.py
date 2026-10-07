"""
Alive / Ping / Stats - Premium Dark Theme
"""

import time
from datetime import datetime
from telethon import events
from config import BOT_NAME, CMD_PREFIX
from core.version import __version__
from core.theme import ALIVE_BANNER, FOOTER, LINE
from utils.helpers import get_system_stats, get_readable_time, edit_or_reply, command_pattern

START_TIME = datetime.now()


def register(client):
    @client.on(command_pattern("alive"))
    async def alive_handler(event):
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        stats = get_system_stats()
        me = await event.client.get_me()
        name = me.first_name or "User"

        text = f"""
{ALIVE_BANNER}

**\u26a1 Status** \u00bb `ONLINE`
**\U0001f464 User** \u00bb [{name}](tg://user?id={me.id})
**\U0001f3f7\ufe0f Version** \u00bb `{__version__}`
**\u23f3 Uptime** \u00bb `{uptime}`
**\U0001f539 Prefix** \u00bb `{CMD_PREFIX}`

{LINE}

**\U0001f4ca System**
**CPU** \u00bb `{stats['cpu']}`
**RAM** \u00bb `{stats['ram']}`
**DISK** \u00bb `{stats['disk']}`
**SERVER** \u00bb `{stats['uptime']}`

{LINE}

**\U0001f311 Dark \u2022 Premium \u2022 Powerful**
{FOOTER}
"""
        await edit_or_reply(event, text)

    @client.on(command_pattern("ping"))
    async def ping_handler(event):
        start = time.time()
        msg = await edit_or_reply(event, "**\u23f3 Pinging...**")
        end = time.time()
        ms = round((end - start) * 1000, 2)
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))

        text = f"""
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551   \u26a1 PONG \u26a1          \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d

**Speed** \u00bb `{ms} ms`
**Uptime** \u00bb `{uptime}`

{FOOTER}
"""
        await msg.edit(text)

    @client.on(command_pattern("stats"))
    async def stats_handler(event):
        stats = get_system_stats()
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))

        text = f"""
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551   \U0001f4ca SYSTEM STATISTICS     \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d

**Bot Uptime** \u00bb `{uptime}`
**CPU Usage** \u00bb `{stats['cpu']}`
**RAM Usage** \u00bb `{stats['ram']}`
**Disk Usage** \u00bb `{stats['disk']}`
**Server Up** \u00bb `{stats['uptime']}`

{FOOTER}
"""
        await edit_or_reply(event, text)
