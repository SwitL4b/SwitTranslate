# MIT License
# Copyright (c) 2025 kenftr


import os
import json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..'))
EMBED_JSON_PATH = os.path.join(ROOT, 'bot_reply.json')
class EmbedJson:
    _data = None

    @classmethod
    def _load(cls):
        if cls._data is None:
            with open(EMBED_JSON_PATH, 'r', encoding='utf-8') as f:
                cls._data = json.load(f)
        return cls._data

    @classmethod
    def get(cls, key: str) -> dict:

        data = cls._load()
        return data.get(key, {})

