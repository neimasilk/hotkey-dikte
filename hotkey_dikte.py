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
import winreg
import traceback  # Tambah ini untuk debug

# Config
SAMPLE_RATE = 16000
DEVICE_ID = 1
HOTKEY = "ctrl+alt+space"
MODEL_SIZE = "medium"  # Ganti dari "small" ke "medium"
EXIT_HOTKEY = "ctrl+alt+q"

# Global variables
audio_frames = []
is_recording = False
tray = None

class TrayIcon:
    def __init__(self):
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
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        # Gambar mikrofon
        dc.rectangle((28, 40, 36, 48), fill=color)
        dc.ellipse((26, 38, 38, 42), fill=color)
        dc.rectangle((24, 16, 40, 40), fill=color)
        dc.ellipse((24, 14, 40, 18), fill=color)
        dc.ellipse((24, 38, 40, 42), fill=color)
        
        if color == "red":  # Recording state
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
                f"Hotkey: {HOTKEY}",
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
        kb._exit_flag = True
        self.icon.stop()
        
    def run(self):
        self.icon = pystray.Icon(
            "hotkey_dikte",
            icon=self.images["idle"],
            menu=self.menu,
            title="Hotkey Dikte - Ready"
        )
        self.icon.run()

def record_callback(indata, frames, time, status):
    global audio_frames
    try:
        if status:
            print(f"⚠️ Status: {status}")
        if is_recording:
            audio_frames.append(indata.copy())
    except Exception as e:
        print(f"❌ Error in callback: {e}")
        traceback.print_exc()

def transcribe_and_type():
    global audio_frames, tray
    try:
        if not audio_frames:
            print("❌ No audio")
            return
        
        if tray:
            tray.update_status("processing")
        
        audio = np.concatenate(audio_frames).flatten()
        duration = len(audio) / SAMPLE_RATE
        print(f"📊 Debug: {len(audio_frames)} frames, durasi {duration:.2f} detik")
        
        if duration < 0.5:
            print("❌ Audio terlalu pendek")
            audio_frames.clear()
            if tray:
                tray.update_status("idle")
            return
        
        result = model.transcribe(
            audio,
            language="id",
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
    except Exception as e:
        print(f"❌ Error in transcribe: {e}")
        traceback.print_exc()
        audio_frames.clear()

def on_hotkey():
    global is_recording, tray
    try:
        is_recording = not is_recording
        if is_recording:
            print("🎤 RECORDING...")
            if tray:
                tray.update_status("recording")
            audio_frames.clear()
        else:
            print("⏳ Processing...")
            transcribe_and_type()
    except Exception as e:
        print(f"❌ Error in hotkey: {e}")
        traceback.print_exc()

def set_tray_behavior():
    try:
        # Hanya set registry untuk menampilkan semua ikon
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer",
            0, 
            winreg.KEY_ALL_ACCESS
        )
        winreg.SetValueEx(key, "EnableAutoTray", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except:
        pass

def main():
    try:
        print(f"🤖 Loading model {MODEL_SIZE}...")
        global model, tray
        model = whisper.load_model(MODEL_SIZE, device="cuda")

        # Setup audio stream
        stream = sd.InputStream(
            device=DEVICE_ID,
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=record_callback,
            blocksize=1024
        )
        
        print("🎤 Starting audio stream...")
        stream.start()

        # Setup tray icon
        tray = TrayIcon()
        tray_thread = Thread(target=tray.run, daemon=True)
        tray_thread.start()

        # Hotkey handler
        kb.add_hotkey(HOTKEY, on_hotkey)
        kb.add_hotkey(EXIT_HOTKEY, lambda: setattr(kb, "_exit_flag", True))
        
        print(f"🔥 PRESS {HOTKEY} untuk mulai/stop rekam")
        print(f"🚪 PRESS {EXIT_HOTKEY} untuk keluar")
        print("💡 Tips: Bicara dengan jelas dan tidak terlalu cepat")

        # Keep program running
        print("🟢 Program running...")
        kb._exit_flag = False
        while not kb._exit_flag:
            if not stream.active:
                print("⚠️ Warning: Stream tidak aktif!")
                break
            time.sleep(0.1)

    except Exception as e:
        print(f"❌ Error in main: {e}")
        traceback.print_exc()
    finally:
        print("\n⏹️ Stopping stream...")
        try:
            stream.stop()
            stream.close()
            print("✅ Stream berhasil dihentikan")
        except Exception as e:
            print(f"⚠️ Error saat menghentikan stream: {e}")
        print("👋 Program berhenti...")

if __name__ == "__main__":
    main()