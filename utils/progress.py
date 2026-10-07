"""Progress bar utilities"""
import time, math
from utils.helpers import edit_or_reply, humanbytes, get_readable_time

async def progress_callback(current, total, event, start_time, action="Downloading", file_name=None):
    now = time.time()
    diff = now - start_time
    if round(diff % 5.0) == 0 or current == total:
        percentage = current * 100 / total if total else 0
        speed = current / diff if diff > 0 else 0
        eta = (total - current) / speed if speed > 0 else 0
        filled = math.floor(percentage / 5)
        bar = "█" * filled + "░" * (20 - filled)
        text = f"**{action}**\n\n`[{bar}]` **{percentage:.1f}%**\n**Speed:** `{humanbytes(speed)}/s`\n**Done:** `{humanbytes(current)} / {humanbytes(total)}`\n**ETA:** `{get_readable_time(int(eta))}`"
        if file_name: text = f"**File:** `{file_name}`\n\n" + text
        try: await edit_or_reply(event, text)
        except: pass

def simple_progress(percentage, length=20):
    filled = int(length * percentage / 100)
    return "█" * filled + "░" * (length - filled)
