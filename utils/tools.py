"""
General purpose tools and helpers
"""

import re
import hashlib
import base64
import random
import string
from typing import Optional


def extract_user(text: str) -> Optional[str]:
    if not text:
        return None
    match = re.search(r"@(\w+)|(\d{5,})", text)
    if match:
        return match.group(1) or match.group(2)
    return text.strip()


def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def b64encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def b64decode(text: str) -> str:
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "Invalid base64"


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def clean_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def split_message(text: str, limit: int = 4096) -> list:
    if len(text) <= limit:
        return [text]
    parts = []
    while text:
        parts.append(text[:limit])
        text = text[limit:]
    return parts


def mention_html(user_id: int, name: str) -> str:
    return f'<a href="tg://user?id={user_id}">{name}</a>'


def mention_markdown(user_id: int, name: str) -> str:
    return f"[{name}](tg://user?id={user_id})"
