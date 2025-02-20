"""Configuration schema and validation for Hotkey Dikte application.

This module defines Pydantic models for configuration validation and provides
helper functions for loading and validating configuration files.
"""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, validator
from loguru import logger

class AudioConfig(BaseModel):
    """Audio configuration settings with validation."""
    sample_rate: int = Field(default=16000, ge=8000, le=48000)
    device_id: int = Field(default=1, ge=0)
    channels: int = Field(default=1, ge=1, le=2)
    blocksize: int = Field(default=1024, ge=256, le=4096)

    @validator('sample_rate')
    def validate_sample_rate(cls, v):
        if v not in [8000, 16000, 22050, 44100, 48000]:
            logger.warning(f"Unusual sample rate: {v}")
        return v

class TranscriberConfig(BaseModel):
    """Transcriber configuration settings with validation."""
    model_size: str = Field(default="medium")
    language: str = Field(default="id")
    initial_prompt: str = Field(default="Transkripsi percakapan Bahasa Indonesia dengan jelas dan akurat.")
    use_cuda: bool = Field(default=True)

    @validator('model_size')
    def validate_model_size(cls, v):
        valid_sizes = ["tiny", "base", "small", "medium", "large"]
        if v not in valid_sizes:
            raise ValueError(f"Model size must be one of {valid_sizes}")
        return v

    @validator('language')
    def validate_language(cls, v):
        valid_langs = ["id", "en"]
        if v not in valid_langs:
            raise ValueError(f"Language must be one of {valid_langs}")
        return v

class HotkeyConfig(BaseModel):
    """Hotkey configuration settings with validation."""
    record_hotkey: str = Field(default="ctrl+alt+space")
    exit_hotkey: str = Field(default="ctrl+alt+q")

    @validator('record_hotkey', 'exit_hotkey')
    def validate_hotkey(cls, v):
        valid_modifiers = ['ctrl', 'alt', 'shift', 'win']
        parts = v.lower().split('+')
        
        if len(parts) < 2:
            raise ValueError("Hotkey must include at least one modifier key")
            
        for modifier in parts[:-1]:
            if modifier not in valid_modifiers:
                raise ValueError(f"Invalid modifier key: {modifier}")
        
        return v

class AppConfig(BaseModel):
    """Main application configuration with validation."""
    audio: AudioConfig = Field(default_factory=AudioConfig)
    transcriber: TranscriberConfig = Field(default_factory=TranscriberConfig)
    hotkeys: HotkeyConfig = Field(default_factory=HotkeyConfig)
    log_path: Optional[Path] = None

    class Config:
        arbitrary_types_allowed = True

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
                logger.error(f"Error loading config: {e}. Using defaults.")
        return cls()