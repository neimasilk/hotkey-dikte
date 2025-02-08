"""
Hotkey Dikte - Speech-to-Text dengan Whisper AI
============================================

Program untuk mengubah suara menjadi teks menggunakan Whisper AI.
Tekan CTRL+ALT+SPACE untuk mulai/stop merekam, ESC untuk keluar.

Requires:
- sounddevice
- numpy
- openai-whisper
- pyautogui
- keyboard
- pystray
- Pillow

Author: Mukhlis Amien
License: MIT
"""

import sounddevice as sd
import numpy as np
import whisper
import pyautogui
import keyboard as kb
import time
from pathlib import Path
import json
import pystray
from PIL import Image, ImageDraw
from threading import Thread, Event
import sys

class Config:
    def __init__(self):
        self.sample_rate = 16000
        self.device_id = 1
        self.hotkey = "ctrl+alt+space"
        self.model_size = "small"
        self.language = "id"
        
    @classmethod
    def load(cls, path="config.json"):
        config = cls()
        if Path(path).exists():
            with open(path, "r") as f:
                data = json.load(f)
                config.sample_rate = data.get("sample_rate", config.sample_rate)
                config.device_id = data.get("device_id", config.device_id)
                config.hotkey = data.get("hotkey", config.hotkey)
                config.model_size = data.get("model_size", config.model_size)
                config.language = data.get("language", config.language)
        return config
    
    def save(self, path="config.json"):
        with open(path, "w") as f:
            json.dump({
                "sample_rate": self.sample_rate,
                "device_id": self.device_id,
                "hotkey": self.hotkey,
                "model_size": self.model_size,
                "language": self.language
            }, f, indent=4)

    def create_default_config(self):
        self.save("config.json")
        print("✅ Config file created: config.json")

class TrayIcon:
    def __init__(self, config):
        self.config = config
        self.icon = None
        self.status = "idle"
        self.menu = None
        self.update_event = Event()
        
        # Generate icon images
        self.images = {
            "idle": self.create_image("green"),
            "recording": self.create_image("red"),
            "processing": self.create_image("yellow")
        }
        
        self.init_menu()
        
    def create_image(self, color):
        # Buat gambar dengan background transparan
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        # Gambar mikrofon
        # Base mikrofon
        dc.rectangle((28, 40, 36, 48), fill=color)
        dc.ellipse((26, 38, 38, 42), fill=color)
        
        # Badan mikrofon
        dc.rectangle((24, 16, 40, 40), fill=color)
        dc.ellipse((24, 14, 40, 18), fill=color)  # Top rounded
        dc.ellipse((24, 38, 40, 42), fill=color)  # Bottom rounded
        
        # Stand mikrofon
        if color == "red":  # Recording state
            # Tambah gelombang suara
            for i in range(3):
                offset = (i + 1) * 6
                dc.arc((20-offset, 12-offset, 44+offset, 36+offset), 
                      -60, 60, fill=color, width=2)
        
        return image
        
    def init_menu(self):
        self.menu = pystray.Menu(
            pystray.MenuItem(
                "Hotkey Dikte",
                lambda: None,
                enabled=False
            ),
            pystray.MenuItem(
                f"Hotkey: {self.config.hotkey}",
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Status: " + self.status.capitalize(),
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Keluar",
                self.exit_program
            )
        )
        
    def update_status(self, status):
        self.status = status
        if self.icon:
            self.icon.icon = self.images[status]
            self.icon.title = f"Hotkey Dikte - {status.capitalize()}"
            
    def exit_program(self):
        self.icon.stop()
        sys.exit(0)
        
    def run(self):
        self.icon = pystray.Icon(
            "hotkey_dikte",
            icon=self.images["idle"],
            menu=self.menu,
            title="Hotkey Dikte - Ready"
        )
        # Tambahkan flag ini agar ikon selalu terlihat
        if hasattr(self.icon, '_icon'):  # Windows
            self.icon._icon.version = None
        self.icon.run()

# Global variables
audio_frames = []
is_recording = False
tray = None  # Will store TrayIcon instance

# Load config and model
config = Config.load()
model = whisper.load_model(config.model_size, device="cuda")

def record_callback(indata, frames, time, status):
    global audio_frames
    if is_recording:
        audio_frames.append(indata.copy())

def transcribe_and_type():
    global audio_frames, tray
    if not audio_frames:
        print("❌ No audio")
        return
    
    if tray:
        tray.update_status("processing")
    
    # Proses audio
    audio = np.concatenate(audio_frames).flatten()
    
    # Debug info
    duration = len(audio) / config.sample_rate
    print(f"📊 Debug: {len(audio_frames)} frames, durasi {duration:.2f} detik")
    
    # Skip jika terlalu pendek
    if duration < 0.5:
        print("❌ Audio terlalu pendek")
        audio_frames.clear()
        if tray:
            tray.update_status("idle")
        return
    
    # Transkripsi
    result = model.transcribe(
        audio,
        language=config.language,
        task="transcribe",
        initial_prompt="Transkripsi percakapan Bahasa Indonesia dengan jelas dan akurat.",
        fp16=True
    )
    
    text = result["text"].strip()
    print(f"🖨️ Hasil: '{text}'")
    
    if text:
        time.sleep(0.1)
        pyautogui.write(text)
    audio_frames.clear()
    
    if tray:
        tray.update_status("idle")

def on_hotkey():
    global is_recording, tray
    is_recording = not is_recording
    if is_recording:
        print("🎤 RECORDING...")
        if tray:
            tray.update_status("recording")
        audio_frames.clear()
    else:
        print("⏳ Processing...")
        transcribe_and_type()

def main():
    global tray, config
    
    # Load atau buat config
    config = Config.load()
    if not Path("config.json").exists():
        config.create_default_config()
    
    # Setup tray icon
    tray = TrayIcon(config)
    tray_thread = Thread(target=tray.run, daemon=True)
    tray_thread.start()

    # Setup audio stream
    stream = sd.InputStream(
        device=config.device_id,
        samplerate=config.sample_rate,
        channels=1,
        callback=record_callback,
        blocksize=1024
    )
    stream.start()

    # Hotkey handler
    kb.add_hotkey(config.hotkey, on_hotkey)
    print(f"🔥 PRESS {config.hotkey} | ESC to EXIT")
    print("💡 Tips: Bicara dengan jelas dan tidak terlalu cepat")

    try:
        kb.wait("esc")
    finally:
        stream.stop()
        print("\nProgram berhenti...")
        if tray and tray.icon:
            tray.icon.stop()

if __name__ == "__main__":
    main()