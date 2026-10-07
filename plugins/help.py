"""
Help Menu - Premium Dark Theme
"""

from telethon import events
from config import CMD_PREFIX, BOT_NAME
from core.version import __version__
from core.theme import HELP_BANNER, FOOTER, MODULE_ICONS, LINE
from utils.helpers import edit_or_reply, command_pattern

HELP_TEXT = {
    "alive": f"\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n\u2551  \U0001f7e2 ALIVE MODULE           \u2551\n\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n`{CMD_PREFIX}alive` \u2014 Bot status + system\n`{CMD_PREFIX}ping` \u2014 Response speed\n`{CMD_PREFIX}stats` \u2014 System statistics",
    "admin": f"\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n\u2551  \U0001f6e1\ufe0f ADMIN MODULE           \u2551\n\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n\n`{CMD_PREFIX}ban` `{CMD_PREFIX}unban` `{CMD_PREFIX}kick`\n`{CMD_PREFIX}mute` `{CMD_PREFIX}unmute`\n`{CMD_PREFIX}promote` `{CMD_PREFIX}demote`\n`{CMD_PREFIX}purge` `{CMD_PREFIX}del` `{CMD_PREFIX}pin` `{CMD_PREFIX}unpin`\n`{CMD_PREFIX}purgeme` `{CMD_PREFIX}lock` `{CMD_PREFIX}unlock` `{CMD_PREFIX}locks`",
    "tag": f"**\U0001f4e2 TAG**\n`{CMD_PREFIX}tagall` `{CMD_PREFIX}all` `{CMD_PREFIX}admin`",
    "spam": f"**\U0001f4a3 SPAM (Owner)**\n`{CMD_PREFIX}spam` `{CMD_PREFIX}delayspam` `{CMD_PREFIX}spamreply` `{CMD_PREFIX}cspam`",
    "raid": f"**\u2694\ufe0f RAID (Owner)**\n`{CMD_PREFIX}raid` `{CMD_PREFIX}replyraid` `{CMD_PREFIX}draid`",
    "auto": f"**\U0001f916 AUTO**\n`{CMD_PREFIX}autoreply` `{CMD_PREFIX}delreply` `{CMD_PREFIX}listreply`\n`{CMD_PREFIX}filter` `{CMD_PREFIX}stop` `{CMD_PREFIX}filters`",
    "afk": f"**\U0001f4a4 AFK**\n`{CMD_PREFIX}afk` `{CMD_PREFIX}unafk`",
    "notes": f"**\U0001f4dd NOTES**\n`{CMD_PREFIX}save` `{CMD_PREFIX}get` `{CMD_PREFIX}clear` `{CMD_PREFIX}notes`",
    "welcome": f"**\U0001f44b WELCOME**\n`{CMD_PREFIX}setwelcome` `{CMD_PREFIX}setgoodbye` `{CMD_PREFIX}clearwelcome`",
    "gban": f"**\U0001f528 GBAN & SUDO**\n`{CMD_PREFIX}gban` `{CMD_PREFIX}ungban` `{CMD_PREFIX}gbanlist`\n`{CMD_PREFIX}addsudo` `{CMD_PREFIX}rmsudo` `{CMD_PREFIX}sudolist`",
    "art": f"**\U0001f3a8 ART**\n`{CMD_PREFIX}font` `{CMD_PREFIX}ascii` `{CMD_PREFIX}flip` `{CMD_PREFIX}vapor` `{CMD_PREFIX}zalgo` `{CMD_PREFIX}carbon`",
    "utils": f"**\U0001f6e0\ufe0f UTILS**\n`{CMD_PREFIX}id` `{CMD_PREFIX}info` `{CMD_PREFIX}ui` (110+ fields)\n`{CMD_PREFIX}qr` `{CMD_PREFIX}tts` `{CMD_PREFIX}paste` `{CMD_PREFIX}calc`\n`{CMD_PREFIX}weather` `{CMD_PREFIX}remind` `{CMD_PREFIX}chatinfo`",
    "userinfo": f"**\U0001f464 USERINFO**\n`{CMD_PREFIX}info` `{CMD_PREFIX}whois` `{CMD_PREFIX}userinfo` `{CMD_PREFIX}ui`\n110+ fields full detailed info",
    "media": f"**\U0001f4e5 MEDIA**\n`{CMD_PREFIX}dl` `{CMD_PREFIX}yt` `{CMD_PREFIX}song`",
    "ai": f"**\U0001f9e0 AI**\n`{CMD_PREFIX}ai` `{CMD_PREFIX}gemini` `{CMD_PREFIX}gpt`",
    "fun": f"**\U0001f389 FUN**\n`{CMD_PREFIX}quote` `{CMD_PREFIX}joke` `{CMD_PREFIX}meme` `{CMD_PREFIX}ship` `{CMD_PREFIX}decide`",
    "broadcast": f"**\U0001f4e1 BROADCAST**\n`{CMD_PREFIX}broadcast` `{CMD_PREFIX}gcast` `{CMD_PREFIX}usercast`",
    "system": f"**\u2699\ufe0f SYSTEM**\n`{CMD_PREFIX}eval` `{CMD_PREFIX}exec` `{CMD_PREFIX}restart` `{CMD_PREFIX}clone` `{CMD_PREFIX}revert`",
    "moderation": f"**\U0001f512 MODERATION**\n`{CMD_PREFIX}setflood` `{CMD_PREFIX}flood` `{CMD_PREFIX}addblacklist` `{CMD_PREFIX}blacklist`",
    "pm": f"**\U0001f4ac PM PERMIT**\n`{CMD_PREFIX}approve` `{CMD_PREFIX}disapprove` `{CMD_PREFIX}block` `{CMD_PREFIX}unblock`",
}


def register(client):
    @client.on(command_pattern("help(?: |$)(.*)"))
    async def help_handler(event):
        args = event.pattern_match.group(1).strip().lower()

        if args and args in HELP_TEXT:
            await edit_or_reply(event, HELP_TEXT[args] + FOOTER)
            return

        modules = [
            ("alive", "Status & Ping"),
            ("admin", "Ban Mute Promote"),
            ("tag", "Tagall & Admin tag"),
            ("spam", "Spam tools"),
            ("raid", "Raid tools"),
            ("auto", "AutoReply & Filters"),
            ("afk", "Away mode"),
            ("notes", "Save notes"),
            ("welcome", "Welcome msgs"),
            ("gban", "Global ban & Sudo"),
            ("art", "Fonts & Styles"),
            ("utils", "Tools & Utils"),
            ("userinfo", "Full user info 110+"),
            ("media", "Download media"),
            ("ai", "Gemini & GPT"),
            ("fun", "Fun commands"),
            ("broadcast", "Mass message"),
            ("system", "Eval Exec Clone"),
            ("moderation", "Flood Blacklist"),
            ("pm", "PM Permit"),
        ]

        text = f"""
{HELP_BANNER}

**Version** \u00bb `{__version__}`
**Prefix** \u00bb `{CMD_PREFIX}`
**Commands** \u00bb `100+`

{LINE}

"""
        for key, desc in modules:
            icon = MODULE_ICONS.get(key, "\u2022")
            text += f"**{icon} `{CMD_PREFIX}help {key}`** \u2014 {desc}\n"

        text += f"""
{LINE}

**Example:** `{CMD_PREFIX}help admin`
**Full list:** ALL_COMMANDS.md

{FOOTER}
"""
        await edit_or_reply(event, text)
