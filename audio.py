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
                print(f"⚠️ Status: {status}")
            if self.is_recording:
                self.audio_frames.append(indata.copy())
        except Exception as e:
            print(f"❌ Error in callback: {e}")
            traceback.print_exc()

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
        except Exception as e:
            print(f"❌ Error starting stream: {e}")
            traceback.print_exc()
            raise

    def stop_stream(self) -> None:
        """Stop and close the audio input stream."""
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            except Exception as e:
                print(f"❌ Error stopping stream: {e}")
                traceback.print_exc()

    def start_recording(self) -> None:
        """Start recording audio."""
        self.is_recording = True
        self.audio_frames.clear()
        self._update_status("recording")

    def stop_recording(self) -> None:
        """Stop recording audio."""
        self.is_recording = False

class Transcriber:
    """Handles audio transcription using Whisper AI."""
    def __init__(self, model_size: str, language: str, initial_prompt: str):
        self.model = whisper.load_model(model_size, device="cuda")
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
            print(f"📊 Debug: Audio duration {duration:.2f} seconds")

            if duration < 0.5:
                print("❌ Audio too short")
                return None

            result = self.model.transcribe(
                audio_data,
                language=self.language,
                task="transcribe",
                initial_prompt=self.initial_prompt,
                fp16=True
            )

            return result["text"].strip()

        except Exception as e:
            print(f"❌ Error in transcribe: {e}")
            traceback.print_exc()
            return None