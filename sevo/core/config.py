"""Configuration management with YAML file support."""

import os
import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "data_dir": "/tmp/sevo",
    "identity": {
        "name": "sevo-agent",
        "role": "AI助手",
        "core_values": ["诚实", "善良", "公平", "成长", "安全"],
    },
    "emotion": {
        "base_valence": 0.7,
        "base_arousal": 0.6,
        "base_dominance": 0.5,
    },
    "cognitive": {
        "openness": 0.7,
        "conscientiousness": 0.9,
        "agreeableness": 0.8,
        "extraversion": 0.6,
        "neuroticism": 0.3,
    },
    "memory": {
        "retention_days": 30,
        "auto_cleanup": True,
        "max_items": 10000,
    },
    "learning": {
        "auto_reflection": True,
        "reflection_interval": 10,
        "llm_provider": None,
        "llm_model": None,
        "llm_api_key": None,
    },
}


class Config:
    """Manages configuration from file, env, and defaults."""

    def __init__(self, config_path: str = None):
        self._data = dict(DEFAULT_CONFIG)  # deep copy
        if config_path and os.path.exists(config_path):
            self._load_file(config_path)
        self._apply_env_overrides()

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split(".")
        node = self._data
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return default
        return node

    def to_dict(self) -> dict:
        return dict(self._data)

    # ── Internal ──

    def _load_file(self, path: str) -> None:
        with open(path) as f:
            if path.endswith(".json"):
                overrides = json.load(f)
            elif path.endswith((".yaml", ".yml")):
                try:
                    import yaml
                    overrides = yaml.safe_load(f)
                except ImportError:
                    return  # yaml not available, ignore
            else:
                return
            self._deep_merge(self._data, overrides)

    def _apply_env_overrides(self) -> None:
        env_map = {
            "SEVO_DATA_DIR": "data_dir",
            "SEVO_LLM_PROVIDER": "learning.llm_provider",
            "SEVO_LLM_MODEL": "learning.llm_model",
            "SEVO_LLM_API_KEY": "learning.llm_api_key",
        }
        for env, key in env_map.items():
            val = os.environ.get(env)
            if val:
                self._set_nested(key, val)

    def _set_nested(self, key: str, value: Any) -> None:
        parts = key.split(".")
        node = self._data
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = value

    @staticmethod
    def _deep_merge(base: dict, overrides: dict) -> None:
        for k, v in overrides.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict):
                Config._deep_merge(base[k], v)
            else:
                base[k] = v