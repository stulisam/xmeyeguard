"""
配置管理：读写 JSON 配置文件，管理 PIN 码和用户设置
"""
import os
import json
import hashlib
import secrets


CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'config.json')

DEFAULT_CONFIG = {
    'pin_hash': None,
    'pin_salt': None,
    'reminder_interval': 25,   # 分钟
    'rest_duration': 3,        # 分钟
    'voice_enabled': True,
    'auto_start': True,
}


class Config:
    def __init__(self):
        self._ensure_data_dir()
        self._data = self._load()

    def _ensure_data_dir(self):
        data_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # 补全缺失的默认值
                for k, v in DEFAULT_CONFIG.items():
                    if k not in data:
                        data[k] = v
                return data
            except Exception:
                pass
        return dict(DEFAULT_CONFIG)

    def _save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    # ── PIN 码 ──────────────────────────────────────────
    def has_pin(self):
        return bool(self._data.get('pin_hash'))

    def set_pin(self, pin: str):
        salt = secrets.token_hex(16)
        pin_hash = hashlib.sha256((salt + pin).encode()).hexdigest()
        self._data['pin_salt'] = salt
        self._data['pin_hash'] = pin_hash
        self._save()

    def verify_pin(self, pin: str) -> bool:
        salt = self._data.get('pin_salt', '')
        stored_hash = self._data.get('pin_hash', '')
        if not stored_hash:
            return False
        return hashlib.sha256((salt + pin).encode()).hexdigest() == stored_hash

    # ── 设置项 ───────────────────────────────────────────
    @property
    def reminder_interval(self) -> int:
        return self._data.get('reminder_interval', 25)

    @reminder_interval.setter
    def reminder_interval(self, value: int):
        self._data['reminder_interval'] = value
        self._save()

    @property
    def rest_duration(self) -> int:
        return self._data.get('rest_duration', 3)

    @rest_duration.setter
    def rest_duration(self, value: int):
        self._data['rest_duration'] = value
        self._save()

    @property
    def voice_enabled(self) -> bool:
        return self._data.get('voice_enabled', True)

    @voice_enabled.setter
    def voice_enabled(self, value: bool):
        self._data['voice_enabled'] = value
        self._save()
