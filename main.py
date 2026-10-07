"""
Tanya UserBot - Advanced Telegram UserBot for Render
Made with ❤️ for powerful automation
"""

import asyncio
import logging
import os
import sys
import threading
from flask import Flask

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, AuthKeyError

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

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("TanyaUserBot")

# ========== KEEP-ALIVE SERVER (Required for Render Web Service) ==========
app = Flask(__name__)


@app.route("/")
def home():
    return {
        "status": "alive",
        "bot": BOT_NAME,
        "version": BOT_VERSION,
        "message": "Tanya UserBot is running successfully on Render 🚀",
    }, 200


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


def run_flask():
    """Run Flask keep-alive server in a separate thread"""
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


# ========== TELEGRAM CLIENT ==========
if not STRING_SESSION:
    logger.error("❌ STRING_SESSION is missing! Generate one using string_session.py")
    sys.exit(1)

if not API_ID or not API_HASH:
    logger.error("❌ API_ID or API_HASH is missing!")
    sys.exit(1)

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH,
    device_model="Tanya UserBot",
    system_version="Render Cloud",
    app_version=BOT_VERSION,
)


async def load_plugins():
    """Load all plugins from plugins/ directory"""
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    loaded = 0
    failed = 0

    for filename in sorted(os.listdir(plugins_dir)):
        if filename.endswith(".py") and not filename.startswith("_"):
            plugin_name = filename[:-3]
            try:
                # Import the plugin module
                module = __import__(f"plugins.{plugin_name}", fromlist=[plugin_name])
                # If plugin has a register function, call it
                if hasattr(module, "register"):
                    module.register(client)
                loaded += 1
                logger.info(f"✅ Loaded plugin: {plugin_name}")
            except Exception as e:
                failed += 1
                logger.error(f"❌ Failed to load {plugin_name}: {e}")

    logger.info(f"📦 Plugins loaded: {loaded} | Failed: {failed}")
    return loaded


async def main():
    """Main entry point"""
    logger.info(f"🚀 Starting {BOT_NAME} v{BOT_VERSION}...")

    # Start Flask keep-alive in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"🌐 Keep-alive server started on port {PORT}")

    try:
        await client.start()
        me = await client.get_me()
        logger.info(f"✅ Logged in as: {me.first_name} (@{me.username or 'NoUsername'}) | ID: {me.id}")

        # Set owner if not set
        if not OWNER_ID:
            logger.warning(f"⚠️ OWNER_ID not set. Using logged-in user ({me.id}) as owner.")

        # Load all plugins
        await load_plugins()

        # Notify owner
        try:
            await client.send_message(
                "me",
                f"**🤖 {BOT_NAME} v{BOT_VERSION} Started Successfully!**\n\n"
                f"**User:** `{me.first_name}`\n"
                f"**Prefix:** `{CMD_PREFIX}`\n"
                f"**Port:** `{PORT}`\n"
                f"**Status:** Running on Render 🚀\n\n"
                f"Type `{CMD_PREFIX}help` to see all commands.",
            )
        except Exception:
            pass

        logger.info("🎉 Tanya UserBot is fully operational!")
        await client.run_until_disconnected()

    except AuthKeyError:
        logger.error("❌ Invalid STRING_SESSION! Please generate a new one.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Shutting down Tanya UserBot...")
    except Exception as e:
        logger.error(f"💥 Crash: {e}")
        sys.exit(1)
