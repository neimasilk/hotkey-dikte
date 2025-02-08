# save_audio.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import keyboard as kb

# Config
SAMPLE_RATE = 16000
DEVICE_ID = 1  # Ganti dengan ID mic Anda
HOTKEY = "ctrl+alt+space"

# Variables
is_recording = False
audio_frames = []

def record_callback(indata, frames, time, status):
    global audio_frames
    if is_recording:
        audio_frames.append(indata.copy())

def toggle_recording():
    global is_recording, audio_frames
    is_recording = not is_recording
    
    if not is_recording and len(audio_framerjemahan olehes) > 0:
        # Save to WAV
        audio = np.concatenate(audio_frames).flatten()
        write("test_recording.wav", SAMPLE_RATE, audio)
        print("🎧 Saved to test_recording.wav. Putar file ini!")
        audio_frames.clear()

# Setup audio stream
stream = sd.InputStream(
    device=DEVICE_ID,
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=record_callback,
    blocksize=1024
)
stream.start()

# Hotkey handler
kb.add_hotkey(HOTKEY, toggle_recording)
print(f"🔥 Tekan {HOTKEY} untuk mulai/menghentikan rekaman")
print("🚪 Tekan Ctrl+C untuk keluar")

# Keep running
try:
    while True:
        pass
except KeyboardInterrupt:
    stream.stop()
    print("\nKeluar...")