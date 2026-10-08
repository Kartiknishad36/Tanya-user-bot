"""
Tanya UserBot v2.0 - All commands built into main.py
Works even if plugins fail to load
"""

import asyncio
import logging
import os
import sys
import random
import time
import threading
from datetime import datetime
from flask import Flask

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import AuthKeyError

from config import (
    API_ID, API_HASH, STRING_SESSION, PORT,
    BOT_NAME, BOT_VERSION, OWNER_ID, CMD_PREFIX,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("Tanya")

app = Flask(__name__)
START_TIME = datetime.now()
P = CMD_PREFIX


@app.route("/")
def home():
    return {"status": "online", "bot": BOT_NAME, "version": BOT_VERSION}, 200


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


def run_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


def uptime_str():
    secs = int((datetime.now() - START_TIME).total_seconds())
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


client = None


def register_all_commands(tg):
    """Register every command directly - no plugin import needed"""

    @tg.on(events.NewMessage(pattern=rf"^{P}ping$", outgoing=True))
    async def cmd_ping(e):
        t = time.time()
        await e.edit("**Pinging...**")
        ms = round((time.time() - t) * 1000, 2)
        await e.edit(f"**Pong!** `{ms} ms`\n**Uptime:** `{uptime_str()}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}alive$", outgoing=True))
    async def cmd_alive(e):
        me = await tg.get_me()
        await e.edit(
            f"**{BOT_NAME}**\n\n"
            f"**Status** » `ONLINE`\n"
            f"**User** » `{me.first_name}`\n"
            f"**Version** » `{BOT_VERSION}`\n"
            f"**Uptime** » `{uptime_str()}`\n"
            f"**Prefix** » `{P}`"
        )

    @tg.on(events.NewMessage(pattern=rf"^{P}help(?: |$)(.*)", outgoing=True))
    async def cmd_help(e):
        arg = (e.pattern_match.group(1) or "").strip().lower()
        menus = {
            "admin": f"`{P}ban` `{P}kick` `{P}mute` `{P}unmute` `{P}promote` `{P}demote` `{P}del` `{P}purge` `{P}pin` `{P}unpin`",
            "info": f"`{P}id` `{P}info` `{P}whois`",
            "fun": f"`{P}joke` `{P}quote` `{P}decide` `{P}choose`",
            "tools": f"`{P}calc` `{P}reverse` `{P}tagall`",
        }
        if arg in menus:
            await e.edit(f"**{arg.upper()}**\n\n{menus[arg]}")
            return
        await e.edit(
            f"**{BOT_NAME} Help** v`{BOT_VERSION}`\n\n"
            f"`{P}ping` `{P}alive` `{P}help`\n"
            f"`{P}id` `{P}info`\n"
            f"`{P}ban` `{P}kick` `{P}mute` `{P}promote`\n"
            f"`{P}del` `{P}purge` `{P}pin`\n"
            f"`{P}tagall` `{P}joke` `{P}calc`\n\n"
            f"**More:** `{P}help admin` / `info` / `fun` / `tools`"
        )

    @tg.on(events.NewMessage(pattern=rf"^{P}id$", outgoing=True))
    async def cmd_id(e):
        if e.is_reply:
            r = await e.get_reply_message()
            await e.edit(f"**User ID:** `{r.sender_id}`\n**Chat ID:** `{e.chat_id}`")
        else:
            await e.edit(f"**Chat ID:** `{e.chat_id}`\n**Your ID:** `{e.sender_id}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}info(?: |$)(.*)", outgoing=True))
    async def cmd_info(e):
        arg = (e.pattern_match.group(1) or "").strip()
        try:
            if e.is_reply:
                r = await e.get_reply_message()
                user = await tg.get_entity(r.sender_id)
            elif arg:
                user = await tg.get_entity(arg)
            else:
                user = await tg.get_me()
        except Exception:
            return await e.edit("User not found")
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        await e.edit(
            f"**User Info**\n\n"
            f"**Name:** [{name}](tg://user?id={user.id})\n"
            f"**Username:** @{user.username or 'None'}\n"
            f"**ID:** `{user.id}`\n"
            f"**Bot:** `{user.bot}`\n"
            f"**Premium:** `{getattr(user, 'premium', False)}`\n"
            f"**Verified:** `{user.verified}`"
        )

    @tg.on(events.NewMessage(pattern=rf"^{P}whois(?: |$)(.*)", outgoing=True))
    async def cmd_whois(e):
        await cmd_info(e)

    @tg.on(events.NewMessage(pattern=rf"^{P}ban$", outgoing=True))
    async def cmd_ban(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.edit_permissions(e.chat_id, r.sender_id, view_messages=False)
            await e.edit(f"Banned `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}unban$", outgoing=True))
    async def cmd_unban(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.edit_permissions(e.chat_id, r.sender_id, view_messages=True)
            await e.edit(f"Unbanned `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}kick$", outgoing=True))
    async def cmd_kick(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.kick_participant(e.chat_id, r.sender_id)
            await e.edit(f"Kicked `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}mute$", outgoing=True))
    async def cmd_mute(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.edit_permissions(e.chat_id, r.sender_id, send_messages=False)
            await e.edit(f"Muted `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}unmute$", outgoing=True))
    async def cmd_unmute(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.edit_permissions(e.chat_id, r.sender_id, send_messages=True)
            await e.edit(f"Unmuted `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}promote$", outgoing=True))
    async def cmd_promote(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.edit_admin(
                e.chat_id, r.sender_id,
                change_info=True, delete_messages=True, ban_users=True,
                invite_users=True, pin_messages=True,
            )
            await e.edit(f"Promoted `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}demote$", outgoing=True))
    async def cmd_demote(e):
        if not e.is_reply:
            return await e.edit("Reply to user")
        r = await e.get_reply_message()
        try:
            await tg.edit_admin(e.chat_id, r.sender_id, is_admin=False)
            await e.edit(f"Demoted `{r.sender_id}`")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}del$", outgoing=True))
    async def cmd_del(e):
        if e.is_reply:
            r = await e.get_reply_message()
            await r.delete()
        await e.delete()

    @tg.on(events.NewMessage(pattern=rf"^{P}purge$", outgoing=True))
    async def cmd_purge(e):
        if not e.is_reply:
            return await e.edit("Reply to message")
        r = await e.get_reply_message()
        ids = []
        async for m in tg.iter_messages(e.chat_id, min_id=r.id - 1, max_id=e.id):
            ids.append(m.id)
            if len(ids) >= 100:
                await tg.delete_messages(e.chat_id, ids)
                ids = []
        if ids:
            await tg.delete_messages(e.chat_id, ids)

    @tg.on(events.NewMessage(pattern=rf"^{P}pin$", outgoing=True))
    async def cmd_pin(e):
        if not e.is_reply:
            return await e.edit("Reply to message")
        r = await e.get_reply_message()
        await tg.pin_message(e.chat_id, r.id)
        await e.edit("Pinned")

    @tg.on(events.NewMessage(pattern=rf"^{P}unpin$", outgoing=True))
    async def cmd_unpin(e):
        await tg.pin_message(e.chat_id, None)
        await e.edit("Unpinned")

    @tg.on(events.NewMessage(pattern=rf"^{P}tagall(?: |$)(.*)", outgoing=True))
    async def cmd_tagall(e):
        text = (e.pattern_match.group(1) or "").strip() or "Hello!"
        mentions, n = [], 0
        async for u in tg.iter_participants(e.chat_id):
            if u.bot:
                continue
            mentions.append(f"[{u.first_name}](tg://user?id={u.id})")
            n += 1
            if n % 15 == 0:
                await e.respond(text + "\n\n" + " ".join(mentions))
                mentions = []
                await asyncio.sleep(0.8)
        if mentions:
            await e.respond(text + "\n\n" + " ".join(mentions))
        await e.delete()

    @tg.on(events.NewMessage(pattern=rf"^{P}joke$", outgoing=True))
    async def cmd_joke(e):
        jokes = [
            "Why do programmers prefer dark mode? Light attracts bugs!",
            "There are 10 types of people: those who know binary and those who don't.",
            "A SQL query walks into a bar and asks: Can I JOIN you?",
        ]
        await e.edit(f"**{random.choice(jokes)}**")

    @tg.on(events.NewMessage(pattern=rf"^{P}quote$", outgoing=True))
    async def cmd_quote(e):
        qs = [
            "The only way to do great work is to love what you do.",
            "First solve the problem, then write the code.",
            "Code is like humor. When you have to explain it, it's bad.",
        ]
        await e.edit(f"**{random.choice(qs)}**")

    @tg.on(events.NewMessage(pattern=rf"^{P}decide$", outgoing=True))
    async def cmd_decide(e):
        await e.edit(f"**{random.choice(['Yes', 'No', 'Maybe', 'Definitely'])}**")

    @tg.on(events.NewMessage(pattern=rf"^{P}choose(?: |$)(.*)", outgoing=True))
    async def cmd_choose(e):
        opts = (e.pattern_match.group(1) or "").split()
        if len(opts) < 2:
            return await e.edit(f"Usage: `{P}choose a b c`")
        await e.edit(f"**I choose:** `{random.choice(opts)}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}calc(?: |$)(.*)", outgoing=True))
    async def cmd_calc(e):
        expr = (e.pattern_match.group(1) or "").strip()
        if not expr:
            return await e.edit(f"Usage: `{P}calc 2+2`")
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expr):
            return await e.edit("Invalid")
        try:
            await e.edit(f"**{expr} = `{eval(expr)}`**")
        except Exception as ex:
            await e.edit(f"`{ex}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}reverse(?: |$)(.*)", outgoing=True))
    async def cmd_reverse(e):
        t = (e.pattern_match.group(1) or "").strip()
        if not t and e.is_reply:
            r = await e.get_reply_message()
            t = r.text or ""
        if not t:
            return await e.edit("Provide text")
        await e.edit(f"`{t[::-1]}`")

    @tg.on(events.NewMessage(pattern=rf"^{P}spam(?: |$)(.*)", outgoing=True))
    async def cmd_spam(e):
        if OWNER_ID and e.sender_id != OWNER_ID:
            return
        parts = (e.pattern_match.group(1) or "").strip().split(maxsplit=1)
        if len(parts) < 2:
            return await e.edit(f"Usage: `{P}spam 5 hello`")
        try:
            n = min(int(parts[0]), 20)
        except ValueError:
            return await e.edit("Need number")
        await e.delete()
        for _ in range(n):
            await e.respond(parts[1])
            await asyncio.sleep(0.3)

    @tg.on(events.NewMessage(outgoing=True))
    async def debug_cmd(e):
        t = e.raw_text or ""
        if t.startswith(P):
            logger.info(f"CMD: {t[:60]!r}")

    logger.info("All built-in commands registered")


async def try_load_plugins(tg):
    root = os.path.dirname(os.path.abspath(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)
    plugins_dir = os.path.join(root, "plugins")
    loaded = 0
    if not os.path.isdir(plugins_dir):
        return 0
    for f in sorted(os.listdir(plugins_dir)):
        if not f.endswith(".py") or f.startswith("_"):
            continue
        name = f[:-3]
        try:
            mod = __import__(f"plugins.{name}", fromlist=[name])
            if hasattr(mod, "register"):
                mod.register(tg)
                loaded += 1
                logger.info(f"Plugin OK: {name}")
        except Exception as ex:
            logger.warning(f"Plugin skip {name}: {ex}")
    return loaded


async def main():
    global client
    logger.info(f"Starting {BOT_NAME} v{BOT_VERSION}")

    if not STRING_SESSION or not API_ID or not API_HASH:
        logger.error("Missing API_ID / API_HASH / STRING_SESSION")
        sys.exit(1)

    threading.Thread(target=run_flask, daemon=True).start()
    logger.info(f"Keep-alive port {PORT}")

    client = TelegramClient(
        StringSession(STRING_SESSION),
        API_ID,
        API_HASH,
        device_model="TanyaUserBot",
        system_version="Render",
        app_version=BOT_VERSION,
    )

    try:
        await client.start()
        me = await client.get_me()
        logger.info(f"Logged in: {me.first_name} | {me.id}")

        register_all_commands(client)

        plug_count = await try_load_plugins(client)
        logger.info(f"Extra plugins: {plug_count}")

        try:
            await client.send_message(
                "me",
                f"**{BOT_NAME} STARTED**\n\n"
                f"**Status** » `ONLINE`\n"
                f"**User** » `{me.first_name}`\n"
                f"**Version** » `{BOT_VERSION}`\n"
                f"**Prefix** » `{P}`\n"
                f"**Commands** » `Built-in`\n\n"
                f"Try `{P}ping` `{P}help` `{P}alive`",
            )
        except Exception:
            pass

        logger.info("Fully operational!")
        await client.run_until_disconnected()

    except AuthKeyError:
        logger.error("Invalid STRING_SESSION")
        sys.exit(1)
    except Exception as ex:
        logger.error(f"Fatal: {ex}")
        raise
    finally:
        if client:
            try:
                await client.disconnect()
            except Exception:
                pass


if __name__ == "__main__":
    try:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bye")
    except Exception as ex:
        logger.error(f"Crash: {ex}")
        sys.exit(1)
