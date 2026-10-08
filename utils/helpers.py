import re
from datetime import datetime

try:
    import psutil
except Exception:
    psutil = None

from telethon import events
from config import CMD_PREFIX, OWNER_ID


def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(f"{int(result)}{time_suffix[count - 1]}")
        seconds = remainder
    time_list.reverse()
    return ":".join(time_list) if time_list else "0s"


def get_system_stats() -> dict:
    if not psutil:
        return {"cpu": "N/A", "ram": "N/A", "disk": "N/A", "uptime": "N/A"}
    try:
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        boot = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot
        return {
            "cpu": f"{cpu}%",
            "ram": f"{ram.percent}%",
            "disk": f"{disk.percent}%",
            "uptime": str(uptime).split(".")[0],
        }
    except Exception:
        return {"cpu": "N/A", "ram": "N/A", "disk": "N/A", "uptime": "N/A"}


def is_owner(event) -> bool:
    return (not OWNER_ID) or (event.sender_id == OWNER_ID)


def command_pattern(cmd: str, flags: int = 0):
    prefix = re.escape(CMD_PREFIX)
    if "(?:" in cmd or "(.*" in cmd:
        pattern = rf"^{prefix}{cmd}"
    elif cmd.endswith("$"):
        pattern = rf"^{prefix}{cmd}"
    else:
        pattern = rf"^{prefix}{cmd}(?: |$)(.*)"
    return events.NewMessage(
        pattern=pattern,
        outgoing=True,
        forwards=False,
        flags=flags,
    )


async def edit_or_reply(event, text: str, **kwargs):
    try:
        return await event.edit(text, **kwargs)
    except Exception:
        try:
            return await event.reply(text, **kwargs)
        except Exception:
            return await event.respond(text)


def humanbytes(size: float) -> str:
    if not size:
        return "0 B"
    power = 1024.0
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
