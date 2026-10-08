"""
Help Menu - Premium Dark Theme
"""

from config import CMD_PREFIX, BOT_NAME
from utils.helpers import edit_or_reply, command_pattern

try:
    from core.version import __version__
except Exception:
    __version__ = "2.0.0"

try:
    from core.theme import HELP_BANNER, FOOTER, MODULE_ICONS, LINE
except Exception:
    HELP_BANNER = (
        "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "\u2551     \U0001f311 TANYA HELP MENU \U0001f311      \u2551\n"
        "\u2551         DARK \u2022 PREMIUM         \u2551\n"
        "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d"
    )
    FOOTER = "\n\u2022\u2550\u2550\u2550\u2550\u2550\u2550\u2550 Tanya UserBot \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2022"
    LINE = "\u2500" * 36
    MODULE_ICONS = {}

HELP_TEXT = {
    "alive": f"**\U0001f7e2 ALIVE**\n`{CMD_PREFIX}alive` `{CMD_PREFIX}ping` `{CMD_PREFIX}stats`",
    "admin": f"**\U0001f6e1\ufe0f ADMIN**\n`{CMD_PREFIX}ban` `{CMD_PREFIX}kick` `{CMD_PREFIX}mute` `{CMD_PREFIX}promote` `{CMD_PREFIX}purge` `{CMD_PREFIX}pin`",
    "tag": f"**\U0001f4e2 TAG**\n`{CMD_PREFIX}tagall` `{CMD_PREFIX}all` `{CMD_PREFIX}admin`",
    "spam": f"**\U0001f4a3 SPAM**\n`{CMD_PREFIX}spam` `{CMD_PREFIX}delayspam` `{CMD_PREFIX}cspam`",
    "raid": f"**\u2694\ufe0f RAID**\n`{CMD_PREFIX}raid` `{CMD_PREFIX}replyraid`",
    "auto": f"**\U0001f916 AUTO**\n`{CMD_PREFIX}autoreply` `{CMD_PREFIX}filter` `{CMD_PREFIX}filters`",
    "afk": f"**\U0001f4a4 AFK**\n`{CMD_PREFIX}afk` `{CMD_PREFIX}unafk`",
    "notes": f"**\U0001f4dd NOTES**\n`{CMD_PREFIX}save` `{CMD_PREFIX}get` `{CMD_PREFIX}notes`",
    "welcome": f"**\U0001f44b WELCOME**\n`{CMD_PREFIX}setwelcome` `{CMD_PREFIX}setgoodbye`",
    "gban": f"**\U0001f528 GBAN**\n`{CMD_PREFIX}gban` `{CMD_PREFIX}ungban` `{CMD_PREFIX}addsudo`",
    "art": f"**\U0001f3a8 ART**\n`{CMD_PREFIX}font` `{CMD_PREFIX}ascii` `{CMD_PREFIX}vapor`",
    "utils": f"**\U0001f6e0\ufe0f UTILS**\n`{CMD_PREFIX}id` `{CMD_PREFIX}info` `{CMD_PREFIX}ui` `{CMD_PREFIX}qr` `{CMD_PREFIX}calc`",
    "userinfo": f"**\U0001f464 USERINFO**\n`{CMD_PREFIX}info` `{CMD_PREFIX}whois` `{CMD_PREFIX}ui`",
    "media": f"**\U0001f4e5 MEDIA**\n`{CMD_PREFIX}dl` `{CMD_PREFIX}yt` `{CMD_PREFIX}song`",
    "ai": f"**\U0001f9e0 AI**\n`{CMD_PREFIX}ai` `{CMD_PREFIX}gemini` `{CMD_PREFIX}gpt`",
    "fun": f"**\U0001f389 FUN**\n`{CMD_PREFIX}quote` `{CMD_PREFIX}joke` `{CMD_PREFIX}meme`",
    "broadcast": f"**\U0001f4e1 BROADCAST**\n`{CMD_PREFIX}broadcast` `{CMD_PREFIX}gcast`",
    "system": f"**\u2699\ufe0f SYSTEM**\n`{CMD_PREFIX}eval` `{CMD_PREFIX}exec` `{CMD_PREFIX}restart`",
    "moderation": f"**\U0001f512 MOD**\n`{CMD_PREFIX}setflood` `{CMD_PREFIX}addblacklist`",
    "pm": f"**\U0001f4ac PM**\n`{CMD_PREFIX}approve` `{CMD_PREFIX}block`",
    "porn": f"**\U0001f311 DARK**\n`{CMD_PREFIX}porn` `{CMD_PREFIX}darkdl`",
}


def register(client):
    @client.on(command_pattern("help"))
    async def help_handler(event):
        args = ""
        try:
            args = (event.pattern_match.group(1) or "").strip().lower()
        except Exception:
            args = ""

        if args and args in HELP_TEXT:
            await edit_or_reply(event, HELP_TEXT[args] + FOOTER)
            return

        modules = [
            ("alive", "Status & Ping"),
            ("admin", "Ban Mute Promote"),
            ("tag", "Tagall"),
            ("spam", "Spam tools"),
            ("raid", "Raid tools"),
            ("auto", "AutoReply & Filters"),
            ("afk", "Away mode"),
            ("notes", "Notes"),
            ("welcome", "Welcome"),
            ("gban", "GBan & Sudo"),
            ("art", "Fonts & Art"),
            ("utils", "Tools"),
            ("userinfo", "110+ user info"),
            ("media", "Download"),
            ("ai", "Gemini & GPT"),
            ("fun", "Fun"),
            ("broadcast", "Broadcast"),
            ("system", "Eval Exec"),
            ("moderation", "Flood Blacklist"),
            ("pm", "PM Permit"),
            ("porn", "Dark video"),
        ]

        text = f"{HELP_BANNER}\n\n"
        text += f"**Version** \u00bb `{__version__}`\n"
        text += f"**Prefix** \u00bb `{CMD_PREFIX}`\n"
        text += f"**Commands** \u00bb `100+`\n\n"
        text += f"{LINE}\n\n"

        for key, desc in modules:
            icon = MODULE_ICONS.get(key, "\u2022")
            text += f"**{icon} `{CMD_PREFIX}help {key}`** \u2014 {desc}\n"

        text += f"\n{LINE}\n\n"
        text += f"**Example:** `{CMD_PREFIX}help admin`\n"
        text += FOOTER

        await edit_or_reply(event, text)
