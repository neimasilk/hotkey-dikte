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

from config import AppConfig
from audio import AudioConfig, AudioRecorder, Transcriber
from ui import TrayIcon

class HotkeyDikte:
    """Main application class that coordinates all components."""
    def __init__(self, config_path: Path = None):
        # Load configuration
        self.config = AppConfig.load(config_path)
        
        # Initialize components
        self.audio_config = AudioConfig(
            sample_rate=self.config.sample_rate,
            device_id=self.config.device_id
        )
        
        self.recorder = AudioRecorder(self.audio_config)
        self.transcriber = Transcriber(
            model_size=self.config.model_size,
            language=self.config.language,
            initial_prompt=self.config.initial_prompt
        )
        
        self.tray = TrayIcon(self.config.hotkey)
        self.exit_event = Event()
        
        # Setup callbacks
        self.recorder.set_status_callback(self.tray.update_status)
        self.tray.set_exit_callback(self.stop)
        
    def on_hotkey(self) -> None:
        """Handle hotkey press event."""
        try:
            if self.recorder.is_recording:
                self.recorder.stop_recording()
                self.process_recording()
            else:
                self.recorder.start_recording()
        except Exception as e:
            print(f"❌ Error in hotkey handler: {e}")
            traceback.print_exc()
            
    def process_recording(self) -> None:
        """Process recorded audio and convert to text."""
        try:
            self.tray.update_status("processing")
            
            if not self.recorder.audio_frames:
                print("❌ No audio recorded")
                return
                
            # Combine audio frames and transcribe
            audio_data = np.concatenate(self.recorder.audio_frames).flatten()
            text = self.transcriber.transcribe(
                audio_data,
                self.audio_config.sample_rate
            )
            
            if text:
                time.sleep(0.1)  # Small delay before typing
                pyautogui.write(text)
                
            self.recorder.audio_frames.clear()
            
        except Exception as e:
            print(f"❌ Error processing recording: {e}")
            traceback.print_exc()
        finally:
            self.tray.update_status("idle")
            
    def run(self) -> None:
        """Start the application."""
        try:
            # Start audio stream
            print("🎤 Starting audio stream...")
            self.recorder.start_stream()
            
            # Setup UI
            self.tray.start()
            
            # Register hotkeys
            kb.add_hotkey(self.config.hotkey, self.on_hotkey)
            kb.add_hotkey(self.config.exit_hotkey, self.stop)
            
            # Print usage instructions
            print(f"🔥 PRESS {self.config.hotkey} to start/stop recording")
            print(f"🚪 PRESS {self.config.exit_hotkey} to exit")
            print("💡 Tips: Speak clearly and not too fast")
            print("🟢 Program running...")
            
            # Wait for exit signal
            self.exit_event.wait()
            
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            traceback.print_exc()
        finally:
            self.cleanup()
            
    def stop(self) -> None:
        """Stop the application."""
        self.exit_event.set()
            
    def cleanup(self) -> None:
        """Clean up resources before exit."""
        print("\n⏹️ Stopping application...")
        try:
            self.recorder.stop_stream()
            print("✅ Audio stream stopped")
        except Exception as e:
            print(f"⚠️ Error stopping audio stream: {e}")
        print("👋 Program stopped")

def main():
    """Application entry point."""
    app = HotkeyDikte()
    app.run()

if __name__ == "__main__":
    main()