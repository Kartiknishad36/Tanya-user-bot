"""
Useful decorators for plugins
"""

import functools
from telethon import events
from config import OWNER_ID, CMD_PREFIX
from core.database import db
from utils.helpers import edit_or_reply


def owner_only(func):
    @functools.wraps(func)
    async def wrapper(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            if not db.is_sudo(event.sender_id):
                return
        return await func(event)
    return wrapper


def sudo_or_owner(func):
    @functools.wraps(func)
    async def wrapper(event):
        if OWNER_ID and event.sender_id != OWNER_ID and not db.is_sudo(event.sender_id):
            return
        return await func(event)
    return wrapper


def group_only(func):
    @functools.wraps(func)
    async def wrapper(event):
        if not event.is_group:
            await edit_or_reply(event, "❌ This command only works in groups!")
            return
        return await func(event)
    return wrapper


def private_only(func):
    @functools.wraps(func)
    async def wrapper(event):
        if not event.is_private:
            await edit_or_reply(event, "❌ This command only works in PM!")
            return
        return await func(event)
    return wrapper


def errors_handler(func):
    @functools.wraps(func)
    async def wrapper(event):
        try:
            return await func(event)
        except Exception as e:
            await edit_or_reply(event, f"❌ **Error:** `{type(e).__name__}: {e}`")
    return wrapper
