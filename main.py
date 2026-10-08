"""
Tanya UserBot - Advanced Telegram UserBot for Render
Dark Premium Edition
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
    API_ID,
    API_HASH,
    STRING_SESSION,
    PORT,
    BOT_NAME,
    BOT_VERSION,
    OWNER_ID,
    CMD_PREFIX,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("TanyaUserBot")

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "status": "alive",
        "bot": BOT_NAME,
        "version": BOT_VERSION,
        "message": "Tanya UserBot is running on Render",
    }, 200


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


def run_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


client = None


async def load_plugins(tg_client):
    root = os.path.dirname(os.path.abspath(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)

    plugins_dir = os.path.join(root, "plugins")
    loaded = 0
    failed = 0
    failed_list = []

    if not os.path.isdir(plugins_dir):
        logger.warning("plugins/ folder not found")
        return 0

    for filename in sorted(os.listdir(plugins_dir)):
        if filename.endswith(".py") and not filename.startswith("_"):
            plugin_name = filename[:-3]
            try:
                module = __import__(f"plugins.{plugin_name}", fromlist=[plugin_name])
                if hasattr(module, "register"):
                    module.register(tg_client)
                    loaded += 1
                    logger.info(f"Loaded plugin: {plugin_name}")
                else:
                    logger.warning(f"No register() in {plugin_name}")
            except Exception as e:
                failed += 1
                failed_list.append(plugin_name)
                logger.error(f"Failed to load {plugin_name}: {type(e).__name__}: {e}")

    logger.info(f"Plugins loaded: {loaded} | Failed: {failed}")
    if failed_list:
        logger.error(f"Failed plugins: {', '.join(failed_list)}")
    return loaded


def register_builtin_commands(tg_client):
    prefix = CMD_PREFIX

    @tg_client.on(events.NewMessage(pattern=rf"^{prefix}ping$", outgoing=True))
    async def builtin_ping(event):
        await event.edit(f"**Pong!** `{BOT_NAME}` is alive")

    @tg_client.on(events.NewMessage(pattern=rf"^{prefix}alive$", outgoing=True))
    async def builtin_alive(event):
        me = await tg_client.get_me()
        await event.edit(
            f"**{BOT_NAME}**\n"
            f"**Status** \u00bb `ONLINE`\n"
            f"**User** \u00bb `{me.first_name}`\n"
            f"**Version** \u00bb `{BOT_VERSION}`\n"
            f"**Prefix** \u00bb `{prefix}`"
        )

    @tg_client.on(events.NewMessage(pattern=rf"^{prefix}help(?: |$)", outgoing=True))
    async def builtin_help(event):
        text = (
            f"**{BOT_NAME} Help**\n\n"
            f"`{prefix}ping` \u2014 Check bot\n"
            f"`{prefix}alive` \u2014 Status\n"
            f"`{prefix}help` \u2014 This menu\n"
            f"`{prefix}info` \u2014 User info\n"
            f"`{prefix}id` \u2014 Get IDs\n\n"
            f"**Prefix:** `{prefix}` | **v{BOT_VERSION}**"
        )
        await event.edit(text)

    @tg_client.on(events.NewMessage(pattern=r"^/help(?: |$)", outgoing=True))
    async def builtin_slash_help(event):
        await builtin_help(event)

    @tg_client.on(events.NewMessage(outgoing=True))
    async def debug_outgoing(event):
        text = event.raw_text or ""
        if text.startswith(prefix) or text.startswith("/"):
            logger.info(f"CMD received: {text[:80]!r} chat={event.chat_id}")

    logger.info("Built-in commands registered: .ping .alive .help")


async def main():
    global client

    logger.info(f"Starting {BOT_NAME} v{BOT_VERSION}...")

    if not STRING_SESSION:
        logger.error("STRING_SESSION is missing!")
        sys.exit(1)
    if not API_ID or not API_HASH:
        logger.error("API_ID or API_HASH is missing!")
        sys.exit(1)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"Keep-alive server started on port {PORT}")

    client = TelegramClient(
        StringSession(STRING_SESSION),
        API_ID,
        API_HASH,
        device_model="Tanya UserBot",
        system_version="Render Cloud",
        app_version=BOT_VERSION,
    )

    try:
        await client.start()
        me = await client.get_me()
        logger.info(
            f"Logged in as: {me.first_name} (@{me.username or 'NoUsername'}) | ID: {me.id}"
        )

        if not OWNER_ID:
            logger.warning(f"OWNER_ID not set. Using {me.id} as owner.")

        register_builtin_commands(client)
        await load_plugins(client)

        try:
            if not getattr(client, "_tanya_started_msg", False):
                client._tanya_started_msg = True
                await client.send_message(
                    "me",
                    f"**{BOT_NAME} STARTED**\n\n"
                    f"**Status** \u00bb `ONLINE`\n"
                    f"**User** \u00bb `{me.first_name}`\n"
                    f"**Version** \u00bb `{BOT_VERSION}`\n"
                    f"**Prefix** \u00bb `{CMD_PREFIX}`\n"
                    f"**Port** \u00bb `{PORT}`\n\n"
                    f"Type `{CMD_PREFIX}ping` or `{CMD_PREFIX}help`",
                )
        except Exception as e:
            logger.warning(f"Start message failed: {e}")

        logger.info("Tanya UserBot is fully operational!")
        await client.run_until_disconnected()

    except AuthKeyError:
        logger.error("Invalid STRING_SESSION!")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
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
                raise RuntimeError("closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Crash: {e}")
        sys.exit(1)
