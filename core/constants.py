"""
Constants and static data for Tanya UserBot
"""

BOT_NAME = "Tanya UserBot"
BOT_VERSION = "2.0.0"
BOT_CREATOR = "@Kartiknishad36"
SUPPORT = "https://github.com/Kartiknishad36/Tanya-user-bot"

ALIVE_ART = r"""
████████╗ █████╗ ███╗   ██╗██╗   ██╗ █████╗ 
╚══██╔══╝██╔══██╗████╗  ██║╚██╗ ██╔╝██╔══██╗
   ██║   ███████║██╔██╗ ██║ ╚████╔╝ ███████║
   ██║   ██╔══██║██║╚██╗██║  ╚██╔╝  ██╔══██║
   ██║   ██║  ██║██║ ╚████║   ██║   ██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
"""

RAID_ART = r"""
██████╗  █████╗ ██╗██████╗ 
██╔══██╗██╔══██╗██║██╔══██╗
██████╔╝███████║██║██║  ██║
██╔══██╗██╔══██║██║██║  ██║
██║  ██║██║  ██║██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ 
"""

AFK_DEFAULT = "I'm currently AFK. Please wait for my response."
WELCOME_DEFAULT = "Welcome {mention} to {chat}! 🎉"
GOODBYE_DEFAULT = "Goodbye {mention}! See you soon 👋"

MAX_SPAM_COUNT = 50
MAX_RAID_COUNT = 30
MAX_TAGALL = 100
MAX_WARN = 3

EMOJIS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "ban": "🔨",
    "mute": "🔇",
    "unmute": "🔊",
    "kick": "🥢",
    "pin": "📌",
    "star": "⭐",
    "heart": "❤️",
    "fire": "🔥",
    "rocket": "🚀",
}

FONTS = {
    "bold": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
    ),
    "italic": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍"
    ),
    "monospace": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
    ),
    "bubble": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
    ),
}
