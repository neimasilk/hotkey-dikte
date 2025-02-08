# transcribe_audio.py
import whisper

# Config
MODEL = "medium"  # "base", "small", "medium", "large"
AUDIO_FILE = "test_recording.wav"

# Load model
model = whisper.load_model(MODEL, device="cuda")

# Transkripsi
result = model.transcribe(
    AUDIO_FILE,
    language="id",  # Bahasa Indonesia
    initial_prompt="Transkripsi percakapan bahasa Indonesia",  # Prompt konteks
    fp16=True  # Gunakan GPU
)

# Output
print("=== HASIL TRANSCRIPTION ===")
print(result["text"])