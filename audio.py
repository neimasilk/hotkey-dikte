"""Audio recording and transcription functionality for Hotkey Dikte application.

This module handles audio recording, processing, and transcription using Whisper AI.
"""

import sounddevice as sd
import numpy as np
from typing import List, Optional, Callable
from dataclasses import dataclass
import whisper
from pathlib import Path
import traceback
from logger import get_logger

logger = get_logger(__name__)

@dataclass
class AudioConfig:
    """Audio configuration settings."""
    sample_rate: int
    device_id: int
    channels: int = 1
    blocksize: int = 1024

class AudioRecorder:
    """Handles audio recording and processing."""
    def __init__(self, config: AudioConfig):
        self.config = config
        self.audio_frames: List[np.ndarray] = []
        self.is_recording = False
        self.stream: Optional[sd.InputStream] = None
        self._status_callback: Optional[Callable[[str], None]] = None

        # Validate audio device
        try:
            device_info = sd.query_devices(self.config.device_id)
            logger.info(f"Using audio device: {device_info['name']}")
        except Exception as e:
            logger.error(f"Invalid audio device {self.config.device_id}: {e}")
            # Try to find a working default device
            try:
                default_device = sd.default.device[0]
                logger.info(f"Falling back to default device {default_device}")
                self.config.device_id = default_device
            except Exception as e:
                logger.critical(f"No working audio device found: {e}")
                raise

    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for status updates.

        Args:
            callback: Function to call with status updates.
        """
        self._status_callback = callback

    def _update_status(self, status: str) -> None:
        """Update status through callback if set."""
        if self._status_callback:
            self._status_callback(status)

    def record_callback(self, indata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags) -> None:
        """Callback for audio recording."""
        try:
            if status:
                logger.warning(f"Audio callback status: {status}")
            if self.is_recording:
                self.audio_frames.append(indata.copy())
        except Exception as e:
            logger.error(f"Error in audio callback: {e}")
            logger.debug(traceback.format_exc())

    def start_stream(self) -> None:
        """Start the audio input stream."""
        try:
            self.stream = sd.InputStream(
                device=self.config.device_id,
                samplerate=self.config.sample_rate,
                channels=self.config.channels,
                callback=self.record_callback,
                blocksize=self.config.blocksize
            )
            self.stream.start()
            logger.info("Audio stream started successfully")
        except Exception as e:
            logger.error(f"Failed to start audio stream: {e}")
            logger.debug(traceback.format_exc())
            raise

    def stop_stream(self) -> None:
        """Stop and close the audio input stream."""
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
                self.stream = None
                logger.info("Audio stream stopped and closed")
            except Exception as e:
                logger.error(f"Error stopping audio stream: {e}")
                logger.debug(traceback.format_exc())

    def start_recording(self) -> None:
        """Start recording audio."""
        self.is_recording = True
        self.audio_frames.clear()
        self._update_status("recording")
        logger.debug("Started recording")

    def stop_recording(self) -> None:
        """Stop recording audio."""
        self.is_recording = False
        logger.debug("Stopped recording")

class Transcriber:
    """Handles audio transcription using Whisper AI."""
    def __init__(self, model_size: str, language: str, initial_prompt: str, use_cuda: bool = True):
        try:
            import torch
            device = "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
            if device == "cpu" and use_cuda:
                logger.warning("CUDA requested but not available, falling back to CPU")
            self.model = whisper.load_model(model_size, device=device)
            logger.info(f"Loaded Whisper model '{model_size}' on {device}")
        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {e}")
            logger.debug(traceback.format_exc())
            raise
            
        self.language = language
        self.initial_prompt = initial_prompt

    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> Optional[str]:
        """Transcribe audio data to text.

        Args:
            audio_data: Audio data as numpy array.
            sample_rate: Sample rate of the audio.

        Returns:
            Transcribed text if successful, None otherwise.
        """
        try:
            duration = len(audio_data) / sample_rate
            logger.debug(f"Processing audio: {duration:.2f} seconds")

            if duration < 0.5:
                logger.warning("Audio too short for transcription")
                return None

            result = self.model.transcribe(
                audio_data,
                language=self.language,
                task="transcribe",
                initial_prompt=self.initial_prompt,
                fp16=True
            )

            text = result["text"].strip()
            logger.debug(f"Transcription completed: {len(text)} characters")
            return text

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            logger.debug(traceback.format_exc())
            return None