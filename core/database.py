"""
Simple JSON-based database for Tanya UserBot
"""

import json
import os
import threading
from typing import Any, Dict, List, Optional
from config import DATA_DIR

_lock = threading.Lock()


class Database:
    def __init__(self, name: str = "tanya_db.json"):
        self.path = os.path.join(DATA_DIR, name)
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {
                "notes": {},
                "filters": {},
                "afk": {},
                "approved": [],
                "blacklist": [],
                "whitelist": [],
                "gbans": [],
                "sudo": [],
                "welcome": {},
                "goodbye": {},
                "auto_reply": {},
                "locks": {},
                "warns": {},
                "settings": {},
            }
            self._save()

    def _save(self):
        with _lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self._save()

    def delete(self, key: str):
        if key in self._data:
            del self._data[key]
            self._save()

    def add_note(self, chat_id: int, name: str, content: str):
        notes = self._data.setdefault("notes", {})
        chat_notes = notes.setdefault(str(chat_id), {})
        chat_notes[name.lower()] = content
        self._save()

    def get_note(self, chat_id: int, name: str) -> Optional[str]:
        return self._data.get("notes", {}).get(str(chat_id), {}).get(name.lower())

    def get_all_notes(self, chat_id: int) -> Dict[str, str]:
        return self._data.get("notes", {}).get(str(chat_id), {})

    def delete_note(self, chat_id: int, name: str) -> bool:
        notes = self._data.get("notes", {}).get(str(chat_id), {})
        if name.lower() in notes:
            del notes[name.lower()]
            self._save()
            return True
        return False

    def add_filter(self, chat_id: int, keyword: str, response: str):
        filters = self._data.setdefault("filters", {})
        chat_f = filters.setdefault(str(chat_id), {})
        chat_f[keyword.lower()] = response
        self._save()

    def get_filters(self, chat_id: int) -> Dict[str, str]:
        return self._data.get("filters", {}).get(str(chat_id), {})

    def delete_filter(self, chat_id: int, keyword: str) -> bool:
        filters = self._data.get("filters", {}).get(str(chat_id), {})
        if keyword.lower() in filters:
            del filters[keyword.lower()]
            self._save()
            return True
        return False

    def set_afk(self, user_id: int, reason: str = ""):
        afk = self._data.setdefault("afk", {})
        afk[str(user_id)] = {"reason": reason, "time": __import__("time").time()}
        self._save()

    def get_afk(self, user_id: int) -> Optional[dict]:
        return self._data.get("afk", {}).get(str(user_id))

    def remove_afk(self, user_id: int):
        afk = self._data.get("afk", {})
        if str(user_id) in afk:
            del afk[str(user_id)]
            self._save()

    def add_auto_reply(self, trigger: str, reply: str):
        ar = self._data.setdefault("auto_reply", {})
        ar[trigger.lower()] = reply
        self._save()

    def get_auto_replies(self) -> Dict[str, str]:
        return self._data.get("auto_reply", {})

    def delete_auto_reply(self, trigger: str) -> bool:
        ar = self._data.get("auto_reply", {})
        if trigger.lower() in ar:
            del ar[trigger.lower()]
            self._save()
            return True
        return False

    def add_gban(self, user_id: int, reason: str = ""):
        gbans = self._data.setdefault("gbans", [])
        entry = {"id": user_id, "reason": reason}
        if not any(g["id"] == user_id for g in gbans):
            gbans.append(entry)
            self._save()

    def remove_gban(self, user_id: int) -> bool:
        gbans = self._data.get("gbans", [])
        new = [g for g in gbans if g["id"] != user_id]
        if len(new) != len(gbans):
            self._data["gbans"] = new
            self._save()
            return True
        return False

    def is_gbanned(self, user_id: int) -> bool:
        return any(g["id"] == user_id for g in self._data.get("gbans", []))

    def add_sudo(self, user_id: int):
        sudo = self._data.setdefault("sudo", [])
        if user_id not in sudo:
            sudo.append(user_id)
            self._save()

    def remove_sudo(self, user_id: int):
        sudo = self._data.get("sudo", [])
        if user_id in sudo:
            sudo.remove(user_id)
            self._save()

    def is_sudo(self, user_id: int) -> bool:
        return user_id in self._data.get("sudo", [])


db = Database()
