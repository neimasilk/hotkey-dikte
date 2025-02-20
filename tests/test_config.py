"""Unit tests for configuration validation.

This module contains tests for configuration loading, validation, and error handling.
"""

import pytest
from pathlib import Path
from config_schema import AppConfig, AudioConfig, TranscriberConfig, HotkeyConfig

def test_default_config():
    """Test default configuration values."""
    config = AppConfig()
    assert config.audio.sample_rate == 16000
    assert config.audio.device_id == 1
    assert config.transcriber.model_size == "medium"
    assert config.transcriber.language == "id"

def test_audio_config_validation():
    """Test audio configuration validation."""
    # Test valid sample rates
    for rate in [8000, 16000, 22050, 44100, 48000]:
        config = AudioConfig(sample_rate=rate, device_id=1)
        assert config.sample_rate == rate

    # Test invalid sample rate
    with pytest.raises(ValueError):
        AudioConfig(sample_rate=10000, device_id=1)

    # Test invalid device id
    with pytest.raises(ValueError):
        AudioConfig(sample_rate=16000, device_id=-1)

def test_transcriber_config_validation():
    """Test transcriber configuration validation."""
    # Test valid model sizes
    for size in ["tiny", "base", "small", "medium", "large"]:
        config = TranscriberConfig(model_size=size)
        assert config.model_size == size

    # Test invalid model size
    with pytest.raises(ValueError):
        TranscriberConfig(model_size="invalid")

    # Test valid languages
    for lang in ["id", "en"]:
        config = TranscriberConfig(language=lang)
        assert config.language == lang

    # Test invalid language
    with pytest.raises(ValueError):
        TranscriberConfig(language="invalid")

def test_hotkey_config_validation():
    """Test hotkey configuration validation."""
    # Test valid hotkeys
    valid_hotkeys = [
        "ctrl+alt+space",
        "ctrl+shift+a",
        "win+alt+x"
    ]
    for hotkey in valid_hotkeys:
        config = HotkeyConfig(record_hotkey=hotkey)
        assert config.record_hotkey == hotkey

    # Test invalid hotkeys
    invalid_hotkeys = [
        "space",  # No modifier
        "invalid+x",  # Invalid modifier
        "ctrl+"  # No key
    ]
    for hotkey in invalid_hotkeys:
        with pytest.raises(ValueError):
            HotkeyConfig(record_hotkey=hotkey)

def test_config_file_handling(tmp_path):
    """Test configuration file loading and saving."""
    config_path = tmp_path / "config.json"
    
    # Create test config
    config = AppConfig(
        audio=AudioConfig(sample_rate=44100, device_id=2),
        transcriber=TranscriberConfig(model_size="small", language="en"),
        hotkeys=HotkeyConfig(record_hotkey="ctrl+shift+r")
    )
    
    # Save and reload
    config.save(config_path)
    loaded_config = AppConfig.load(config_path)
    
    # Verify loaded values match original
    assert loaded_config.audio.sample_rate == 44100
    assert loaded_config.audio.device_id == 2
    assert loaded_config.transcriber.model_size == "small"
    assert loaded_config.transcriber.language == "en"
    assert loaded_config.hotkeys.record_hotkey == "ctrl+shift+r"