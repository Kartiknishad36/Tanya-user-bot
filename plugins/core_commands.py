"""
Tanya UserBot - ALL CORE COMMANDS (Single File)
Stylish - Dark - Working
"""

import time
import random
import asyncio
from datetime import datetime

from config import CMD_PREFIX, BOT_NAME, BOT_VERSION, OWNER_ID
from utils.helpers import edit_or_reply, command_pattern, get_system_stats, get_readable_time

START_TIME = datetime.now()
PREFIX = CMD_PREFIX
FOOTER = f"\n•═══════ {BOT_NAME} ═══════•"
LINE = "────────────────────────"


def box(title: str) -> str:
    return (
        f"╔══════════════════════════╗\n"
        f"║  {title.center(22)}  ║\n"
        f"╚══════════════════════════╝"
    )


def register(client):

    @client.on(command_pattern("ping"))
    async def ping_cmd(event):
        t1 = time.time()
        msg = await edit_or_reply(event, "**Pinging...**")
        ms = round((time.time() - t1) * 1000, 2)
        up = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        await msg.edit(
            f"{box('PONG')}\n\n"
            f"**Speed** » `{ms} ms`\n"
            f"**Uptime** » `{up}`\n"
            f"{FOOTER}"
        )

    @client.on(command_pattern("alive"))
    async def alive_cmd(event):
        me = await client.get_me()
        up = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        stats = get_system_stats()
        await edit_or_reply(
            event,
            f"{box('TANYA ALIVE')}\n\n"
            f"**Status** » `ONLINE`\n"
            f"**User** » `{me.first_name}`\n"
            f"**Version** » `{BOT_VERSION}`\n"
            f"**Uptime** » `{up}`\n"
            f"**Prefix** » `{PREFIX}`\n"
            f"{LINE}\n"
            f"**CPU** » `{stats['cpu']}`\n"
            f"**RAM** » `{stats['ram']}`\n"
            f"{FOOTER}"
        )

    @client.on(command_pattern("stats"))
    async def stats_cmd(event):
        stats = get_system_stats()
        up = get_readable_time(int((datetime.now() - START_TIME).total_seconds()))
        await edit_or_reply(
            event,
            f"{box('SYSTEM STATS')}\n\n"
            f"**Bot Up** » `{up}`\n"
            f"**CPU** » `{stats['cpu']}`\n"
            f"**RAM** » `{stats['ram']}`\n"
            f"**DISK** » `{stats['disk']}`\n"
            f"{FOOTER}"
        )

    @client.on(command_pattern("help"))
    async def help_cmd(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip().lower()
        except Exception:
            pass
        modules = {
            "alive": f"`{PREFIX}ping` `{PREFIX}alive` `{PREFIX}stats`",
            "admin": f"`{PREFIX}ban` `{PREFIX}kick` `{PREFIX}mute` `{PREFIX}promote` `{PREFIX}purge` `{PREFIX}del` `{PREFIX}pin`",
            "info": f"`{PREFIX}info` `{PREFIX}id` `{PREFIX}whois`",
            "tag": f"`{PREFIX}tagall` `{PREFIX}admins`",
            "fun": f"`{PREFIX}joke` `{PREFIX}quote` `{PREFIX}decide` `{PREFIX}choose`",
            "tools": f"`{PREFIX}calc` `{PREFIX}reverse`",
            "spam": f"`{PREFIX}spam` `{PREFIX}cspam`",
        }
        if args and args in modules:
            await edit_or_reply(event, f"{box(args.upper())}\n\n{modules[args]}\n{FOOTER}")
            return
        text = f"{box('TANYA HELP')}\n\n**Version** » `{BOT_VERSION}`\n**Prefix** » `{PREFIX}`\n\n{LINE}\n\n"
        for name in modules:
            text += f"**» `{PREFIX}help {name}`**\n"
        text += f"\n{LINE}\n**Example:** `{PREFIX}help admin`\n{FOOTER}"
        await edit_or_reply(event, text)

    @client.on(command_pattern("id"))
    async def id_cmd(event):
        if event.is_reply:
            r = await event.get_reply_message()
            user = await client.get_entity(r.sender_id)
            text = f"**User ID:** `{user.id}`\n**Chat ID:** `{event.chat_id}`\n**Name:** `{user.first_name}`"
        else:
            text = f"**Chat ID:** `{event.chat_id}`\n**Your ID:** `{event.sender_id}`"
        await edit_or_reply(event, text)

    @client.on(command_pattern("info"))
    async def info_cmd(event):
        user = None
        if event.is_reply:
            r = await event.get_reply_message()
            user = await client.get_entity(r.sender_id)
        else:
            args = ""
            try:
                args = (event.pattern_match.group(1) or "").strip()
            except Exception:
                pass
            if args:
                try:
                    user = await client.get_entity(args)
                except Exception:
                    return await edit_or_reply(event, "User not found")
            else:
                user = await client.get_me()
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        text = (
            f"{box('USER INFO')}\n\n"
            f"**Name** » [{name}](tg://user?id={user.id})\n"
            f"**Username** » @{user.username or 'None'}\n"
            f"**ID** » `{user.id}`\n"
            f"**Bot** » `{user.bot}`\n"
            f"**Verified** » `{user.verified}`\n"
            f"**Premium** » `{getattr(user, 'premium', False)}`\n"
            f"{FOOTER}"
        )
        await edit_or_reply(event, text)

    @client.on(command_pattern("whois"))
    async def whois_cmd(event):
        await info_cmd(event)

    @client.on(command_pattern("ban"))
    async def ban_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.edit_permissions(event.chat_id, r.sender_id, view_messages=False)
            await edit_or_reply(event, f"Banned `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("unban"))
    async def unban_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.edit_permissions(event.chat_id, r.sender_id, view_messages=True)
            await edit_or_reply(event, f"Unbanned `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("kick"))
    async def kick_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.kick_participant(event.chat_id, r.sender_id)
            await edit_or_reply(event, f"Kicked `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("mute"))
    async def mute_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.edit_permissions(event.chat_id, r.sender_id, send_messages=False)
            await edit_or_reply(event, f"Muted `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("unmute"))
    async def unmute_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.edit_permissions(event.chat_id, r.sender_id, send_messages=True)
            await edit_or_reply(event, f"Unmuted `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("promote"))
    async def promote_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.edit_admin(
                event.chat_id, r.sender_id,
                change_info=True, delete_messages=True, ban_users=True,
                invite_users=True, pin_messages=True, manage_call=True,
            )
            await edit_or_reply(event, f"Promoted `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("demote"))
    async def demote_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to user")
        r = await event.get_reply_message()
        try:
            await client.edit_admin(event.chat_id, r.sender_id, is_admin=False)
            await edit_or_reply(event, f"Demoted `{r.sender_id}`")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("del"))
    async def del_cmd(event):
        if event.is_reply:
            r = await event.get_reply_message()
            await r.delete()
        await event.delete()

    @client.on(command_pattern("purge"))
    async def purge_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to start message")
        r = await event.get_reply_message()
        msgs = []
        async for m in client.iter_messages(event.chat_id, min_id=r.id - 1, max_id=event.id):
            msgs.append(m.id)
            if len(msgs) >= 100:
                await client.delete_messages(event.chat_id, msgs)
                msgs = []
        if msgs:
            await client.delete_messages(event.chat_id, msgs)
        msg = await event.respond("Purged")
        await asyncio.sleep(2)
        await msg.delete()

    @client.on(command_pattern("pin"))
    async def pin_cmd(event):
        if not event.is_reply:
            return await edit_or_reply(event, "Reply to message")
        r = await event.get_reply_message()
        await client.pin_message(event.chat_id, r.id, notify=True)
        await edit_or_reply(event, "Pinned")

    @client.on(command_pattern("unpin"))
    async def unpin_cmd(event):
        await client.pin_message(event.chat_id, None)
        await edit_or_reply(event, "Unpinned all")

    @client.on(command_pattern("tagall"))
    async def tagall_cmd(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        text = args or "Hello!"
        mentions = []
        count = 0
        async for user in client.iter_participants(event.chat_id):
            if user.bot:
                continue
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")
            count += 1
            if count % 20 == 0:
                await event.respond(f"{text}\n\n" + " ".join(mentions))
                mentions = []
                await asyncio.sleep(1)
        if mentions:
            await event.respond(f"{text}\n\n" + " ".join(mentions))
        await event.delete()

    @client.on(command_pattern("admins"))
    async def admins_cmd(event):
        text = "**Admins**\n\n"
        async for user in client.iter_participants(event.chat_id, filter="admin"):
            text += f"• [{user.first_name}](tg://user?id={user.id})\n"
        await edit_or_reply(event, text)

    @client.on(command_pattern("spam"))
    async def spam_cmd(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return await edit_or_reply(event, f"Usage: `{PREFIX}spam 5 hello`")
        try:
            n = min(int(parts[0]), 30)
        except ValueError:
            return await edit_or_reply(event, "Count must be number")
        msg = parts[1]
        await event.delete()
        for _ in range(n):
            await event.respond(msg)
            await asyncio.sleep(0.3)

    @client.on(command_pattern("cspam"))
    async def cspam_cmd(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        if not args:
            return await edit_or_reply(event, f"Usage: `{PREFIX}cspam hello`")
        await event.delete()
        for ch in args[:50]:
            await event.respond(ch)
            await asyncio.sleep(0.2)

    @client.on(command_pattern("joke"))
    async def joke_cmd(event):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people: those who understand binary and those who don't.",
            "A SQL query walks into a bar, asks two tables: Can I JOIN you?",
            "Why did the developer go broke? Because he used up all his cache!",
        ]
        await edit_or_reply(event, f"**{random.choice(jokes)}**")

    @client.on(command_pattern("quote"))
    async def quote_cmd(event):
        quotes = [
            "The only way to do great work is to love what you do.",
            "Code is like humor. When you have to explain it, it is bad.",
            "First, solve the problem. Then, write the code.",
        ]
        await edit_or_reply(event, f"**{random.choice(quotes)}**")

    @client.on(command_pattern("decide"))
    async def decide_cmd(event):
        await edit_or_reply(event, f"**{random.choice(['Yes', 'No', 'Maybe', 'Definitely', 'Never'])}**")

    @client.on(command_pattern("choose"))
    async def choose_cmd(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        opts = args.split() if args else []
        if len(opts) < 2:
            return await edit_or_reply(event, f"Usage: `{PREFIX}choose a b c`")
        await edit_or_reply(event, f"**I choose:** `{random.choice(opts)}`")

    @client.on(command_pattern("calc"))
    async def calc_cmd(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        if not args:
            return await edit_or_reply(event, f"Usage: `{PREFIX}calc 2+2`")
        try:
            allowed = set("0123456789+-*/().% ")
            if not all(c in allowed for c in args):
                return await edit_or_reply(event, "Invalid characters")
            result = eval(args)
            await edit_or_reply(event, f"**{args} = `{result}`**")
        except Exception as e:
            await edit_or_reply(event, f"`{e}`")

    @client.on(command_pattern("reverse"))
    async def reverse_cmd(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        if not args and event.is_reply:
            r = await event.get_reply_message()
            args = r.text or ""
        if not args:
            return await edit_or_reply(event, "Provide text")
        await edit_or_reply(event, f"`{args[::-1]}`")

    @client.on(command_pattern("purgeme"))
    async def purgeme_cmd(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip()
        except Exception:
            pass
        try:
            n = min(int(args) if args else 10, 100)
        except ValueError:
            n = 10
        count = 0
        async for m in client.iter_messages(event.chat_id, from_user="me", limit=n + 1):
            await m.delete()
            count += 1
        msg = await event.respond(f"Deleted {count} messages")
        await asyncio.sleep(2)
        await msg.delete()
