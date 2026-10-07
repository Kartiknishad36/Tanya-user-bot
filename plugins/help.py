"""
Help menu plugin - Updated for v2.0 with all modules
"""

from telethon import events
from config import CMD_PREFIX, BOT_NAME
from core.version import __version__
from utils.helpers import edit_or_reply, command_pattern

HELP_TEXT = {
    "alive": f"**🟢 Alive**\n`{CMD_PREFIX}alive` `{CMD_PREFIX}ping` `{CMD_PREFIX}stats` `{CMD_PREFIX}sysinfo`",
    "admin": f"**🛡️ Admin**\n`{CMD_PREFIX}ban` `{CMD_PREFIX}kick` `{CMD_PREFIX}mute` `{CMD_PREFIX}promote` `{CMD_PREFIX}purge` `{CMD_PREFIX}pin` `{CMD_PREFIX}lock`",
    "tag": f"**📢 Tag**\n`{CMD_PREFIX}tagall` `{CMD_PREFIX}all` `{CMD_PREFIX}admin`",
    "spam": f"**💣 Spam/Raid**\n`{CMD_PREFIX}spam` `{CMD_PREFIX}delayspam` `{CMD_PREFIX}raid` `{CMD_PREFIX}replyraid` `{CMD_PREFIX}cspam`",
    "auto": f"**🤖 Auto**\n`{CMD_PREFIX}autoreply` `{CMD_PREFIX}filter` `{CMD_PREFIX}filters` `{CMD_PREFIX}listreply`",
    "afk": f"**💤 AFK**\n`{CMD_PREFIX}afk` `{CMD_PREFIX}unafk`",
    "notes": f"**📝 Notes**\n`{CMD_PREFIX}save` `{CMD_PREFIX}get` `{CMD_PREFIX}clear` `{CMD_PREFIX}notes`",
    "welcome": f"**👋 Welcome**\n`{CMD_PREFIX}setwelcome` `{CMD_PREFIX}setgoodbye` `{CMD_PREFIX}clearwelcome`",
    "gban": f"**🔨 GBan**\n`{CMD_PREFIX}gban` `{CMD_PREFIX}ungban` `{CMD_PREFIX}gbanlist` `{CMD_PREFIX}addsudo`",
    "art": f"**🎨 Art**\n`{CMD_PREFIX}font` `{CMD_PREFIX}ascii` `{CMD_PREFIX}flip` `{CMD_PREFIX}vapor` `{CMD_PREFIX}carbon` `{CMD_PREFIX}zalgo`",
    "utils": f"**🛠️ Utils**\n`{CMD_PREFIX}id` `{CMD_PREFIX}info` `{CMD_PREFIX}qr` `{CMD_PREFIX}calc` `{CMD_PREFIX}weather` `{CMD_PREFIX}paste` `{CMD_PREFIX}remind`",
    "media": f"**📥 Media**\n`{CMD_PREFIX}dl` `{CMD_PREFIX}yt` `{CMD_PREFIX}song`",
    "ai": f"**🤖 AI**\n`{CMD_PREFIX}ai` `{CMD_PREFIX}gemini` `{CMD_PREFIX}gpt`",
    "fun": f"**🎉 Fun**\n`{CMD_PREFIX}quote` `{CMD_PREFIX}joke` `{CMD_PREFIX}meme` `{CMD_PREFIX}ship` `{CMD_PREFIX}decide`",
    "broadcast": f"**📡 Broadcast**\n`{CMD_PREFIX}broadcast` `{CMD_PREFIX}gcast` `{CMD_PREFIX}usercast`",
    "system": f"**⚙️ System**\n`{CMD_PREFIX}eval` `{CMD_PREFIX}exec` `{CMD_PREFIX}restart` `{CMD_PREFIX}clone`",
    "moderation": f"**🛡️ Mod**\n`{CMD_PREFIX}setflood` `{CMD_PREFIX}addblacklist` `{CMD_PREFIX}blacklist`",
}


def register(client):
    @client.on(command_pattern("help(?: |$)(.*)"))
    async def help_handler(event):
        args = event.pattern_match.group(1).strip().lower()

        if args and args in HELP_TEXT:
            await edit_or_reply(event, HELP_TEXT[args])
            return

        text = f"""
**🤖 {BOT_NAME} v{__version__} - Help Menu**

**Modules (type `{CMD_PREFIX}help <name>`):**

• `alive` `admin` `tag` `spam` `auto`
• `afk` `notes` `welcome` `gban` `art`
• `utils` `media` `ai` `fun` `broadcast`
• `system` `moderation`

**Prefix:** `{CMD_PREFIX}` | **Commands:** 100+
"""
        await edit_or_reply(event, text)
