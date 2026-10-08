"""
Alive / Ping / Stats plugin
"""

from datetime import datetime
from utils.helpers import get_system_stats, get_readable_time, edit_or_reply, command_pattern

START_TIME = datetime.now()


def register(client):
    @client.on(command_pattern("stats"))
    async def stats_handler(event):
        stats = get_system_stats()
        uptime = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        text = (
            f"**System Stats**\n\n"
            f"**Uptime** \u00bb `{uptime}`\n"
            f"**CPU** \u00bb `{stats['cpu']}`\n"
            f"**RAM** \u00bb `{stats['ram']}`\n"
            f"**DISK** \u00bb `{stats['disk']}`\n"
        )
        await edit_or_reply(event, text)
