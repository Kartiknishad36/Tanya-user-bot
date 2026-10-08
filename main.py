"""
Tanya UserBot v2.0 — Render Ready
Dark • Premium • Stylish
"""

import asyncio
import logging
import os
import sys
import threading
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


@app.route("/")
def home():
    return {"status": "online", "bot": BOT_NAME, "version": BOT_VERSION}, 200


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


def run_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


client = None

PLUGIN_MODULES = [
    "core_commands",
    "help",
    "userinfo",
    "admin",
    "tagall",
    "spam",
    "raid",
    "afk",
    "notes",
    "filters",
    "autoreply",
    "welcome",
    "gban",
    "art",
    "ai",
    "media",
    "fun",
    "broadcast",
    "system",
    "pmpermit",
    "porn",
    "alive",
    "utils",
    "weather",
    "remind",
    "clone",
    "paste",
    "antiflood",
    "blacklist",
    "locks",
    "sudo",
]


async def load_all_plugins(tg_client):
    root = os.path.dirname(os.path.abspath(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)

    plugins_dir = os.path.join(root, "plugins")
    loaded, failed = [], []

    for name in PLUGIN_MODULES:
        path = os.path.join(plugins_dir, f"{name}.py")
        if not os.path.isfile(path):
            continue
        try:
            mod = __import__(f"plugins.{name}", fromlist=[name])
            if hasattr(mod, "register"):
                mod.register(tg_client)
                loaded.append(name)
                logger.info(f"OK {name}")
        except Exception as e:
            failed.append(name)
            logger.error(f"FAIL {name}: {type(e).__name__}: {e}")

    if os.path.isdir(plugins_dir):
        for f in sorted(os.listdir(plugins_dir)):
            if f.endswith(".py") and not f.startswith("_"):
                name = f[:-3]
                if name in loaded or name in failed:
                    continue
                try:
                    mod = __import__(f"plugins.{name}", fromlist=[name])
                    if hasattr(mod, "register"):
                        mod.register(tg_client)
                        loaded.append(name)
                        logger.info(f"OK {name}")
                except Exception as e:
                    failed.append(name)
                    logger.error(f"FAIL {name}: {e}")

    logger.info(f"Loaded: {len(loaded)} | Failed: {len(failed)}")
    if failed:
        logger.warning(f"Failed: {', '.join(failed)}")
    return len(loaded)


def register_emergency_commands(tg_client):
    p = CMD_PREFIX

    @tg_client.on(events.NewMessage(pattern=rf"^{p}ping$", outgoing=True))
    async def _ping(e):
        await e.edit(f"**Pong!** `{BOT_NAME}` OK")

    @tg_client.on(events.NewMessage(pattern=rf"^{p}alive$", outgoing=True))
    async def _alive(e):
        me = await tg_client.get_me()
        await e.edit(
            f"**{BOT_NAME}**\n"
            f"Status » `ONLINE`\n"
            f"User » `{me.first_name}`\n"
            f"Version » `{BOT_VERSION}`\n"
            f"Prefix » `{p}`"
        )

    logger.info("Emergency: .ping .alive")


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

        register_emergency_commands(client)
        count = await load_all_plugins(client)

        try:
            await client.send_message(
                "me",
                f"**{BOT_NAME} STARTED**\n\n"
                f"**Status** » `ONLINE`\n"
                f"**User** » `{me.first_name}`\n"
                f"**Version** » `{BOT_VERSION}`\n"
                f"**Prefix** » `{CMD_PREFIX}`\n"
                f"**Plugins** » `{count}`\n\n"
                f"Try `{CMD_PREFIX}ping` or `{CMD_PREFIX}help`",
            )
        except Exception:
            pass

        logger.info("Fully operational!")
        await client.run_until_disconnected()

    except AuthKeyError:
        logger.error("Invalid STRING_SESSION")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal: {e}")
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
        logger.info("Bye!")
    except Exception as e:
        logger.error(f"Crash: {e}")
        sys.exit(1)
