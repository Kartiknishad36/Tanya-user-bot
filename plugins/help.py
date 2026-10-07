"""
Help menu plugin
"""

from telethon import events, Button
from config import CMD_PREFIX, BOT_NAME, BOT_VERSION
from utils.helpers import edit_or_reply, command_pattern

HELP_TEXT = {
    "alive": f"""
**🟢 Alive Module**

`{CMD_PREFIX}alive` - Check if bot is alive + system stats
`{CMD_PREFIX}ping` - Check response speed
`{CMD_PREFIX}stats` - Detailed system statistics
""",
    "admin": f"""
**🛡️ Admin Tools**

`{CMD_PREFIX}ban` - Ban a user (reply or username)
`{CMD_PREFIX}unban` - Unban a user
`{CMD_PREFIX}kick` - Kick a user
`{CMD_PREFIX}mute` - Mute a user
`{CMD_PREFIX}unmute` - Unmute a user
`{CMD_PREFIX}promote` - Promote to admin
`{CMD_PREFIX}demote` - Demote admin
`{CMD_PREFIX}purge` - Delete messages (reply to start)
`{CMD_PREFIX}del` - Delete replied message
`{CMD_PREFIX}pin` - Pin a message
`{CMD_PREFIX}unpin` - Unpin message
""",
    "utils": f"""
**🛠️ Utilities**

`{CMD_PREFIX}id` - Get user/chat ID
`{CMD_PREFIX}info` - Get detailed user info
`{CMD_PREFIX}whois` - Whois of replied user
`{CMD_PREFIX}tr <lang>` - Translate text (reply)
`{CMD_PREFIX}tts` - Text to speech
`{CMD_PREFIX}qr` - Generate QR code
""",
    "media": f"""
**📥 Media Tools**

`{CMD_PREFIX}dl` - Download media (reply)
`{CMD_PREFIX}yt` - Download YouTube video/audio
`{CMD_PREFIX}song` - Download song by name
""",
    "ai": f"""
**🤖 AI Features**

`{CMD_PREFIX}ai <query>` - Ask Gemini / OpenAI
`{CMD_PREFIX}gemini <query>` - Google Gemini
`{CMD_PREFIX}gpt <query>` - ChatGPT
""",
    "fun": f"""
**🎉 Fun & Entertainment**

`{CMD_PREFIX}quote` - Random inspirational quote
`{CMD_PREFIX}joke` - Random joke
`{CMD_PREFIX}meme` - Random meme
`{CMD_PREFIX}truth` - Truth question
`{CMD_PREFIX}dare` - Dare challenge
""",
    "system": f"""
**⚙️ System (Owner Only)**

`{CMD_PREFIX}eval` - Evaluate Python code
`{CMD_PREFIX}exec` - Execute shell command
`{CMD_PREFIX}restart` - Restart the bot
`{CMD_PREFIX}logs` - Get recent logs
""",
    "pm": f"""
**💬 PM Permit**

`{CMD_PREFIX}approve` - Approve user for PM
`{CMD_PREFIX}disapprove` - Disapprove user
`{CMD_PREFIX}block` - Block user
`{CMD_PREFIX}unblock` - Unblock user
""",
}


def register(client):
    @client.on(command_pattern("help(?: |$)(.*)"))
    async def help_handler(event):
        args = event.pattern_match.group(1).strip().lower()

        if args and args in HELP_TEXT:
            await edit_or_reply(event, HELP_TEXT[args])
            return

        # Main help menu
        text = f"""
**🤖 {BOT_NAME} v{BOT_VERSION} - Help Menu**

**Available Modules:**

• `{CMD_PREFIX}help alive` - Alive, Ping, Stats
• `{CMD_PREFIX}help admin` - Admin tools
• `{CMD_PREFIX}help utils` - Utility commands
• `{CMD_PREFIX}help media` - Media download/upload
• `{CMD_PREFIX}help ai` - AI features
• `{CMD_PREFIX}help fun` - Fun commands
• `{CMD_PREFIX}help system` - System commands
• `{CMD_PREFIX}help pm` - PM Permit

**Prefix:** `{CMD_PREFIX}`
**Total Commands:** 50+

Type `{CMD_PREFIX}help <module>` for detailed commands.
"""
        await edit_or_reply(event, text)
