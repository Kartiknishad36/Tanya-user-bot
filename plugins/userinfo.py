"""
Full Detailed User Information Plugin
Commands: .info , .whois , .userinfo , .ui
Shows 100+ details about any user
"""

import time
from datetime import datetime, timezone
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.types import (
    UserStatusOnline,
    UserStatusOffline,
    UserStatusRecently,
    UserStatusLastWeek,
    UserStatusLastMonth,
    UserStatusEmpty,
    UserProfilePhoto,
    UserProfilePhotoEmpty,
)
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import errors_handler


def format_status(status):
    if status is None:
        return "Unknown / Hidden"
    if isinstance(status, UserStatusOnline):
        return f"\U0001f7e2 Online (expires: {status.expires})"
    if isinstance(status, UserStatusOffline):
        try:
            was_online = status.was_online
            if was_online.tzinfo is None:
                was_online = was_online.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = now - was_online
            days = diff.days
            hours = diff.seconds // 3600
            mins = (diff.seconds % 3600) // 60
            if days > 0:
                ago = f"{days}d {hours}h ago"
            elif hours > 0:
                ago = f"{hours}h {mins}m ago"
            else:
                ago = f"{mins}m ago"
            return f"\U0001f534 Offline \u2014 Last seen: {was_online.strftime('%Y-%m-%d %H:%M:%S UTC')} ({ago})"
        except Exception:
            return f"\U0001f534 Offline \u2014 Last seen: {status.was_online}"
    if isinstance(status, UserStatusRecently):
        return "\U0001f7e1 Last seen recently"
    if isinstance(status, UserStatusLastWeek):
        return "\U0001f7e0 Last seen within a week"
    if isinstance(status, UserStatusLastMonth):
        return "\U0001f7e0 Last seen within a month"
    if isinstance(status, UserStatusEmpty):
        return "\u26ab Status hidden"
    return str(status)


def yesno(val):
    if val is True:
        return "\u2705 Yes"
    if val is False:
        return "\u274c No"
    return "\u2753 Unknown"


async def get_full_user_info(client, user):
    lines = []
    uid = user.id

    lines.append("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557")
    lines.append("\u2551     \U0001f464 FULL USER INFORMATION     \u2551")
    lines.append("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d")
    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f194 BASIC IDENTITY \u2501\u2501\u2501\u2501\u2501**")
    lines.append(f"**01. User ID:** `{uid}`")
    lines.append(f"**02. Access Hash:** `{getattr(user, 'access_hash', 'N/A')}`")
    lines.append(f"**03. First Name:** `{user.first_name or 'None'}`")
    lines.append(f"**04. Last Name:** `{user.last_name or 'None'}`")
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "No Name"
    lines.append(f"**05. Full Name:** [{full_name}](tg://user?id={uid})")
    lines.append(f"**06. Username:** @{user.username or 'None'}")
    lines.append(f"**07. Phone:** `{getattr(user, 'phone', None) or 'Hidden / None'}`")
    lines.append(f"**08. Mention Link:** [Click Here](tg://user?id={uid})")
    lines.append(f"**09. Profile Link:** https://t.me/{user.username}" if user.username else "**09. Profile Link:** `No username`")
    lines.append(f"**10. Deep Link:** `tg://user?id={uid}`")

    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f3f7\ufe0f ACCOUNT FLAGS \u2501\u2501\u2501\u2501\u2501**")
    lines.append(f"**11. Is Bot:** {yesno(user.bot)}")
    lines.append(f"**12. Is Verified:** {yesno(user.verified)}")
    lines.append(f"**13. Is Restricted:** {yesno(user.restricted)}")
    lines.append(f"**14. Is Scam:** {yesno(getattr(user, 'scam', False))}")
    lines.append(f"**15. Is Fake:** {yesno(getattr(user, 'fake', False))}")
    lines.append(f"**16. Is Premium:** {yesno(getattr(user, 'premium', False))}")
    lines.append(f"**17. Is Support:** {yesno(getattr(user, 'support', False))}")
    lines.append(f"**18. Is Min:** {yesno(getattr(user, 'min', False))}")
    lines.append(f"**19. Is Self:** {yesno(getattr(user, 'is_self', False))}")
    lines.append(f"**20. Is Contact:** {yesno(getattr(user, 'contact', False))}")
    lines.append(f"**21. Is Mutual Contact:** {yesno(getattr(user, 'mutual_contact', False))}")
    lines.append(f"**22. Is Deleted:** {yesno(getattr(user, 'deleted', False))}")
    lines.append(f"**23. Is Close Friend:** {yesno(getattr(user, 'close_friend', False))}")
    lines.append(f"**24. Stories Hidden:** {yesno(getattr(user, 'stories_hidden', False))}")
    lines.append(f"**25. Stories Unavailable:** {yesno(getattr(user, 'stories_unavailable', False))}")

    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f310 LANGUAGE & RESTRICTION \u2501\u2501\u2501\u2501\u2501**")
    lines.append(f"**26. Lang Code:** `{getattr(user, 'lang_code', None) or 'N/A'}`")
    lines.append(f"**27. Restriction Reason:** `{getattr(user, 'restriction_reason', None) or 'None'}`")

    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f4f6 ONLINE STATUS \u2501\u2501\u2501\u2501\u2501**")
    status_str = format_status(getattr(user, 'status', None))
    lines.append(f"**28. Status:** {status_str}")
    lines.append(f"**29. Status Type:** `{type(getattr(user, 'status', None)).__name__ if getattr(user, 'status', None) else 'None'}`")

    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f5bc\ufe0f PROFILE PHOTO \u2501\u2501\u2501\u2501\u2501**")
    photo = getattr(user, 'photo', None)
    if photo and not isinstance(photo, UserProfilePhotoEmpty):
        lines.append(f"**30. Has Profile Photo:** \u2705 Yes")
        lines.append(f"**31. Photo ID:** `{getattr(photo, 'photo_id', 'N/A')}`")
        lines.append(f"**32. DC ID:** `{getattr(photo, 'dc_id', 'N/A')}`")
        lines.append(f"**33. Has Video:** {yesno(getattr(photo, 'has_video', False))}")
        lines.append(f"**34. Personal Photo:** {yesno(getattr(photo, 'personal', False))}")
        lines.append(f"**35. Photo Stripped:** `{bool(getattr(photo, 'stripped_thumb', None))}`")
    else:
        lines.append(f"**30. Has Profile Photo:** \u274c No")
        lines.append(f"**31. Photo ID:** `N/A`")
        lines.append(f"**32. DC ID:** `N/A`")
        lines.append(f"**33. Has Video:** \u274c No")
        lines.append(f"**34. Personal Photo:** \u274c No")
        lines.append(f"**35. Photo Stripped:** `False`")

    full = None
    try:
        full = await client(GetFullUserRequest(uid))
    except Exception as e:
        lines.append(f"\n\u26a0\ufe0f FullUserRequest failed: `{e}`")

    if full:
        fu = full.full_user
        lines.append("")
        lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f4cb FULL PROFILE DATA \u2501\u2501\u2501\u2501\u2501**")
        lines.append(f"**36. About / Bio:** `{fu.about or 'No bio set'}`")
        lines.append(f"**37. Common Chats Count:** `{fu.common_chats_count}`")
        lines.append(f"**38. Blocked:** {yesno(getattr(fu, 'blocked', False))}")
        lines.append(f"**39. Phone Calls Available:** {yesno(getattr(fu, 'phone_calls_available', False))}")
        lines.append(f"**40. Phone Calls Private:** {yesno(getattr(fu, 'phone_calls_private', False))}")
        lines.append(f"**41. Video Calls Available:** {yesno(getattr(fu, 'video_calls_available', False))}")
        lines.append(f"**42. Voice Messages Forbidden:** {yesno(getattr(fu, 'voice_messages_forbidden', False))}")
        lines.append(f"**43. Translations Disabled:** {yesno(getattr(fu, 'translations_disabled', False))}")
        lines.append(f"**44. Stories Pinned Available:** {yesno(getattr(fu, 'stories_pinned_available', False))}")
        lines.append(f"**45. Blocked (my side):** {yesno(getattr(fu, 'blocked', False))}")
        lines.append(f"**46. Can View Revenue:** {yesno(getattr(fu, 'can_view_revenue', False))}")
        lines.append(f"**47. Folder ID:** `{getattr(fu, 'folder_id', None) or 'None'}`")
        lines.append(f"**48. Pinned Message ID:** `{getattr(fu, 'pinned_msg_id', None) or 'None'}`")
        lines.append(f"**49. Scheduled Messages:** `{getattr(fu, 'scheduled', False)}`")

        lines.append("")
        lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f514 NOTIFY SETTINGS \u2501\u2501\u2501\u2501\u2501**")
        notify = getattr(fu, 'notify_settings', None)
        if notify:
            lines.append(f"**50. Show Previews:** {yesno(getattr(notify, 'show_previews', None))}")
            lines.append(f"**51. Silent:** {yesno(getattr(notify, 'silent', None))}")
            lines.append(f"**52. Mute Until:** `{getattr(notify, 'mute_until', None) or 'Not muted'}`")
            lines.append(f"**53. Sound:** `{getattr(notify, 'sound', None) or 'Default'}`")
        else:
            lines.append("**50-53. Notify Settings:** `Not available`")

        if user.bot:
            lines.append("")
            lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f916 BOT INFORMATION \u2501\u2501\u2501\u2501\u2501**")
            lines.append(f"**54. Bot Info Version:** `{getattr(fu, 'bot_info_version', 'N/A')}`")
            lines.append(f"**55. Bot Inline Placeholder:** `{getattr(fu, 'bot_inline_placeholder', None) or 'None'}`")
            bot_info = getattr(fu, 'bot_info', None)
            if bot_info:
                lines.append(f"**56. Bot Description:** `{getattr(bot_info, 'description', None) or 'None'}`")
                cmds = getattr(bot_info, 'commands', None) or []
                lines.append(f"**57. Bot Commands Count:** `{len(cmds)}`")
                for i, cmd in enumerate(cmds[:15], 1):
                    lines.append(f"   \u2022 `/{cmd.command}` \u2014 {cmd.description}")
            else:
                lines.append("**56. Bot Description:** `N/A`")
                lines.append("**57. Bot Commands Count:** `0`")
        else:
            lines.append("")
            lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f916 BOT INFORMATION \u2501\u2501\u2501\u2501\u2501**")
            lines.append("**54-57.** Not a bot")

        try:
            photos = await client(GetUserPhotosRequest(user_id=uid, offset=0, max_id=0, limit=100))
            count = getattr(photos, 'count', len(getattr(photos, 'photos', [])))
            lines.append("")
            lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f4f8 PHOTOS \u2501\u2501\u2501\u2501\u2501**")
            lines.append(f"**58. Total Profile Photos:** `{count}`")
        except Exception:
            lines.append("")
            lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f4f8 PHOTOS \u2501\u2501\u2501\u2501\u2501**")
            lines.append("**58. Total Profile Photos:** `Unable to fetch`")

        personal_channel = getattr(fu, 'personal_channel_id', None)
        lines.append(f"**59. Personal Channel ID:** `{personal_channel or 'None'}`")
        lines.append(f"**60. Personal Channel Message:** `{getattr(fu, 'personal_channel_message', None) or 'None'}`")

        bday = getattr(fu, 'birthday', None)
        if bday:
            lines.append(f"**61. Birthday:** `{getattr(bday, 'day', '?')}/{getattr(bday, 'month', '?')}/{getattr(bday, 'year', '') or '----'}`")
        else:
            lines.append("**61. Birthday:** `Not set / Hidden`")

        lines.append(f"**62. Private Forward Name:** `{getattr(fu, 'private_forward_name', None) or 'None'}`")
        lines.append(f"**63. Theme Emoticon:** `{getattr(fu, 'theme_emoticon', None) or 'None'}`")
        lines.append(f"**64. Wallpaper:** `{bool(getattr(fu, 'wallpaper', None))}`")
        lines.append(f"**65. Stories:** `{bool(getattr(fu, 'stories', None))}`")

    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f4e6 RAW USER OBJECT \u2501\u2501\u2501\u2501\u2501**")
    skip = {'photo', 'status', 'restriction_reason', 'emoji_status'}
    idx = 66
    for attr in sorted(dir(user)):
        if attr.startswith('_') or attr in skip:
            continue
        try:
            val = getattr(user, attr)
            if callable(val):
                continue
            if isinstance(val, (str, int, bool, type(None), float)):
                lines.append(f"**{idx}. {attr}:** `{val}`")
                idx += 1
                if idx > 95:
                    break
        except Exception:
            pass

    lines.append("")
    lines.append("**\u2501\u2501\u2501\u2501\u2501 \U0001f4ca CALCULATED / EXTRA \u2501\u2501\u2501\u2501\u2501**")
    lines.append(f"**96. ID Length:** `{len(str(uid))}` digits")
    lines.append(f"**97. Is Even ID:** {yesno(uid % 2 == 0)}")
    lines.append(f"**98. Username Length:** `{len(user.username) if user.username else 0}`")
    lines.append(f"**99. Name Length:** `{len(full_name)}`")
    lines.append(f"**100. Has Last Name:** {yesno(bool(user.last_name))}")
    lines.append(f"**101. Has Username:** {yesno(bool(user.username))}")
    lines.append(f"**102. Has Phone Visible:** {yesno(bool(getattr(user, 'phone', None)))}")
    lines.append(f"**103. Account Type:** `{'Bot' if user.bot else 'User'}`")
    lines.append(f"**104. Premium Badge:** `{'\u2b50 Premium' if getattr(user, 'premium', False) else 'Standard'}`")
    lines.append(f"**105. Trust Level:** `{'Verified \u2705' if user.verified else ('Scam \u26a0\ufe0f' if getattr(user, 'scam', False) else ('Fake \u26a0\ufe0f' if getattr(user, 'fake', False) else 'Normal'))}`")
    lines.append(f"**106. DC Hint:** `{getattr(photo, 'dc_id', 'Unknown') if photo and not isinstance(photo, UserProfilePhotoEmpty) else 'Unknown'}`")
    lines.append(f"**107. Can Be Mentioned:** \u2705 Yes")
    lines.append(f"**108. Telegram Link:** `https://web.telegram.org/k/#{uid}`")
    lines.append(f"**109. Fetched At:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"**110. Fetched By:** Tanya UserBot")

    lines.append("")
    lines.append("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550")
    lines.append("**End of Full User Information**")
    lines.append("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550")

    return "\n".join(lines)


def register(client):
    async def _resolve_user(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            return await event.client.get_entity(reply.sender_id)
        args = event.pattern_match.group(1).strip()
        if args:
            try:
                return await event.client.get_entity(args)
            except Exception:
                return None
        return await event.client.get_me()

    @client.on(command_pattern("info(?: |$)(.*)"))
    @errors_handler
    async def info_handler(event):
        msg = await edit_or_reply(event, "\U0001f50d **Fetching full user information...**")
        user = await _resolve_user(event)
        if not user:
            return await msg.edit("\u274c User not found. Reply to a user or provide username/ID.")
        try:
            text = await get_full_user_info(event.client, user)
            if len(text) > 4000:
                parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
                await msg.edit(parts[0])
                for part in parts[1:]:
                    await event.respond(part)
            else:
                await msg.edit(text)
        except Exception as e:
            await msg.edit(f"\u274c Error fetching info:\n`{type(e).__name__}: {e}`")

    @client.on(command_pattern("whois(?: |$)(.*)"))
    @errors_handler
    async def whois_handler(event):
        await info_handler(event)

    @client.on(command_pattern("userinfo(?: |$)(.*)"))
    @errors_handler
    async def userinfo_handler(event):
        await info_handler(event)

    @client.on(command_pattern("ui(?: |$)(.*)"))
    @errors_handler
    async def ui_handler(event):
        await info_handler(event)
