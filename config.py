"""Configuration management for Hotkey Dikte application.

This module handles all configuration settings and provides a clean interface
for accessing and modifying application settings.
"""

from dataclasses import dataclass
from typing import Optional
import json
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration settings."""
    sample_rate: int = 16000
    device_id: int = 1
    hotkey: str = "ctrl+alt+space"
    exit_hotkey: str = "ctrl+alt+q"
    model_size: str = "medium"
    language: str = "id"
    initial_prompt: str = "Transkripsi percakapan Bahasa Indonesia dengan jelas dan akurat."

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'AppConfig':
        """Load configuration from a JSON file.

        Args:
            config_path: Path to the configuration file. If None, uses default settings.

        Returns:
            AppConfig: Configuration instance with loaded or default settings.
        """
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                return cls(**config_data)
            except Exception as e:
                print(f"⚠️ Error loading config: {e}. Using defaults.")
        return cls()

    def save(self, config_path: Path) -> None:
        """Save current configuration to a JSON file.

        Args:
            config_path: Path where to save the configuration file.
        """
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.__dict__, f, indent=4)
        except Exception as e:
            print(f"⚠️ Error saving config: {e}")