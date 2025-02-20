"""Main application module for Hotkey Dikte.

This module integrates configuration, audio, and UI components to provide
a complete speech-to-text application with hotkey support.
"""

from pathlib import Path
import keyboard as kb
import pyautogui
import time
import traceback
from threading import Event
import numpy as np

from config_schema import AppConfig
from audio import AudioConfig, AudioRecorder, Transcriber
from ui import TrayIcon
from logger import setup_logging, get_logger

logger = get_logger(__name__)

class HotkeyDikte:
    """Main application class that coordinates all components."""
    def __init__(self, config_path: Path = None):
        # Load and validate configuration
        try:
            self.config = AppConfig.load(config_path)
            setup_logging(self.config.log_path)
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
        
        # Initialize components with error handling
        try:
            self.audio_config = self.config.audio
            self.recorder = AudioRecorder(self.audio_config)
            self.transcriber = Transcriber(
                model_size=self.config.transcriber.model_size,
                language=self.config.transcriber.language,
                initial_prompt=self.config.transcriber.initial_prompt,
                use_cuda=self.config.transcriber.use_cuda
            )
            logger.info("Components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
        
        self.tray = TrayIcon(self.config.hotkeys.record_hotkey)
        self.exit_event = Event()
        
        # Setup callbacks
        self.recorder.set_status_callback(self.tray.update_status)
        self.tray.set_exit_callback(self.stop)
        
    def on_hotkey(self) -> None:
        """Handle hotkey press event."""
        try:
            if self.recorder.is_recording:
                logger.debug("Stopping recording")
                self.recorder.stop_recording()
                self.process_recording()
            else:
                logger.debug("Starting recording")
                self.recorder.start_recording()
        except Exception as e:
            logger.error(f"Error in hotkey handler: {e}")
            logger.debug(traceback.format_exc())
            
    def process_recording(self) -> None:
        """Process recorded audio and convert to text."""
        try:
            self.tray.update_status("processing")
            
            if not self.recorder.audio_frames:
                logger.warning("No audio recorded")
                return
                
            # Combine audio frames and transcribe
            audio_data = np.concatenate(self.recorder.audio_frames).flatten()
            logger.debug(f"Processing {len(audio_data)} audio samples")
            
            text = self.transcriber.transcribe(
                audio_data,
                self.audio_config.sample_rate
            )
            
            if text:
                time.sleep(0.1)  # Small delay before typing
                pyautogui.write(text)
                logger.info(f"Transcribed text: {text}")
            else:
                logger.warning("Transcription failed or returned empty result")
                
            self.recorder.audio_frames.clear()
            
        except Exception as e:
            logger.error(f"Error processing recording: {e}")
            logger.debug(traceback.format_exc())
        finally:
            self.tray.update_status("idle")
            
    def run(self) -> None:
        """Start the application."""
        try:
            # Start audio stream
            logger.info("Starting audio stream...")
            self.recorder.start_stream()
            
            # Setup UI
            self.tray.start()
            
            # Register hotkeys
            kb.add_hotkey(self.config.hotkeys.record_hotkey, self.on_hotkey)
            kb.add_hotkey(self.config.hotkeys.exit_hotkey, self.stop)
            
            # Print usage instructions
            logger.info(f"PRESS {self.config.hotkeys.record_hotkey} to start/stop recording")
            logger.info(f"PRESS {self.config.hotkeys.exit_hotkey} to exit")
            logger.info("Tips: Speak clearly and not too fast")
            logger.info("Program running...")
            
            # Wait for exit signal
            self.exit_event.wait()
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            logger.debug(traceback.format_exc())
        finally:
            self.cleanup()
            
    def stop(self) -> None:
        """Stop the application."""
        logger.info("Stopping application...")
        self.exit_event.set()
            
    def cleanup(self) -> None:
        """Clean up resources before exit."""
        try:
            self.recorder.stop_stream()
            logger.info("Audio stream stopped")
        except Exception as e:
            logger.error(f"Error stopping audio stream: {e}")
        logger.info("Program stopped")

def main():
    """Application entry point."""
    try:
        app = HotkeyDikte()
        app.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.debug(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()