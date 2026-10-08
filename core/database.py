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
                "blacklist": {},
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

        # Migrate wrong types
        if isinstance(self._data.get("blacklist"), list):
            self._data["blacklist"] = {}
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

    def is_sudo(self, user_id: int) -> bool:
        return user_id in self._data.get("sudo", [])

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


db = Database()
