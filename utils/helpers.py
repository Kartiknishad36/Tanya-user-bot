import time
import psutil
from datetime import datetime
import pytz
from telethon import events
from config import CMD_PREFIX, OWNER_ID

IST = pytz.timezone("Asia/Kolkata")


def get_readable_time(seconds: int) -> str:
    """Convert seconds to human readable time"""
    count = 0
    time_list = []
    time_suffix = ["s", "m", "h", "days"]
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
    """Get system resource usage"""
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot
    return {
        "cpu": f"{cpu}%",
        "ram": f"{ram.percent}% ({round(ram.used / 1024**3, 2)}/{round(ram.total / 1024**3, 2)} GB)",
        "disk": f"{disk.percent}% ({round(disk.used / 1024**3, 2)}/{round(disk.total / 1024**3, 2)} GB)",
        "uptime": str(uptime).split(".")[0],
    }


def is_owner(event) -> bool:
    """Check if the user is the bot owner"""
    return event.sender_id == OWNER_ID if OWNER_ID else True


def command_pattern(cmd: str, flags: int = 0):
    """Create a command pattern with prefix"""
    return events.NewMessage(pattern=rf"^{CMD_PREFIX}{cmd}(?: |$)(.*)", outgoing=True, flags=flags)


async def edit_or_reply(event, text: str, **kwargs):
    """Edit message if possible, else reply"""
    try:
        return await event.edit(text, **kwargs)
    except Exception:
        return await event.reply(text, **kwargs)


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Progress bar for downloads/uploads"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff if diff > 0 else 0
        elapsed = round(diff)
        eta = round((total - current) / speed) if speed > 0 else 0
        progress_str = "[{0}{1}] {2}%\n".format(
            "".join("\u25cf" for _ in range(math.floor(percentage / 5))),
            "".join("\u25cb" for _ in range(20 - math.floor(percentage / 5))),
            round(percentage, 2),
        )
        tmp = (
            progress_str
            + f"**Speed:** `{humanbytes(speed)}/s`\n"
            + f"**ETA:** `{get_readable_time(eta)}`\n"
            + f"**Progress:** `{humanbytes(current)} / {humanbytes(total)}`"
        )
        if file_name:
            await edit_or_reply(event, f"**{type_of_ps}**\n\n**File:** `{file_name}`\n\n{tmp}")
        else:
            await edit_or_reply(event, f"**{type_of_ps}**\n\n{tmp}")


def humanbytes(size: float) -> str:
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    power = 1024
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


import math  # for progress bar
