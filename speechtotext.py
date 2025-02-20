"""Sandbox for testing speech-to-text functionality.

This module provides a simplified environment for testing audio recording
and real-time transcription using Whisper AI.
"""

import sounddevice as sd
import numpy as np
from pathlib import Path
import whisper
import torch
from typing import Optional

class SimpleSpeechToText:
    def __init__(self):
        # Audio configuration
        self.sample_rate = 16000
        self.channels = 1
        self.blocksize = 1024
        self.device_id = 1  # Default device
        self.is_recording = False
        self.audio_frames = []
        self.max_audio_length = 5.0  # Maximum audio length in seconds
        
        # Initialize Whisper model
        print("Loading Whisper model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model("base", device=device)  # Using smaller base model
        print(f"Model loaded on {device}")
        
        # Try to find a working audio device
        try:
            device_info = sd.query_devices(self.device_id)
            print(f"Using audio device: {device_info['name']}")
        except Exception:
            # Try to find a working default device
            self.device_id = sd.default.device[0]
            device_info = sd.query_devices(self.device_id)
            print(f"Using default device: {device_info['name']}")
    
    def audio_callback(self, indata, frames, time, status):
        """Handle incoming audio data and perform real-time transcription."""
        if status:
            print(f"Audio callback status: {status}")
        if self.is_recording:
            # Append new audio data
            self.audio_frames.append(indata.copy())
            
            # Calculate current buffer duration
            audio_length = len(self.audio_frames) * self.blocksize / self.sample_rate
            
            # Process every 1 second of audio for better memory management
            if audio_length >= 1.0:
                try:
                    # Concatenate audio frames
                    audio_data = np.concatenate(self.audio_frames)
                    
                    # Convert to float32 if needed and ensure proper memory cleanup
                    if audio_data.dtype != np.float32:
                        audio_data = audio_data.astype(np.float32)
                    
                    # Clear CUDA cache before transcription
                    if hasattr(torch.cuda, 'empty_cache'):
                        torch.cuda.empty_cache()
                    
                    # Transcribe with memory-efficient settings
                    result = self.model.transcribe(
                        audio_data,
                        language="id",
                        task="transcribe",
                        initial_prompt="Transkripsi percakapan Bahasa Indonesia",
                        fp16=True,
                        beam_size=1
                    )
                    
                    # Clear CUDA cache and delete unused variables
                    if hasattr(torch.cuda, 'empty_cache'):
                        torch.cuda.empty_cache()
                    del audio_data
                    
                    text = result["text"].strip()
                    if text:
                        print(f"\rTranscription: {text}", end="", flush=True)
                    
                    # Clear result from memory
                    del result
                except Exception as e:
                    print(f"\nError processing audio: {e}")
                finally:
                    # Keep only the last 0.2 seconds of audio for context
                    retain_frames = int(0.2 * self.sample_rate / self.blocksize)
                    if len(self.audio_frames) > retain_frames:
                        self.audio_frames = self.audio_frames[-retain_frames:]
    
    def transcribe(self, audio_data: np.ndarray) -> Optional[str]:
        """Transcribe audio data to text."""
        try:
            # Process audio in smaller chunks
            chunk_duration = 30  # Process 30 seconds at a time
            chunk_samples = int(chunk_duration * self.sample_rate)
            
            # Initialize result text
            full_text = []
            
            # Process audio in chunks
            for i in range(0, len(audio_data), chunk_samples):
                # Get chunk of audio
                chunk = audio_data[i:i + chunk_samples]
                
                # Ensure audio data is in the correct format
                if chunk.dtype != np.float32:
                    chunk = chunk.astype(np.float32)
                
                # Clear CUDA cache before transcription
                if hasattr(torch.cuda, 'empty_cache'):
                    torch.cuda.empty_cache()
                
                # Transcribe with memory-efficient settings
                result = self.model.transcribe(
                    chunk,
                    language="id",
                    task="transcribe",
                    initial_prompt="Transkripsi percakapan Bahasa Indonesia",
                    fp16=True,
                    beam_size=1
                )
                
                # Append transcribed text
                if result["text"].strip():
                    full_text.append(result["text"].strip())
                
                # Clear memory
                del chunk
                del result
                if hasattr(torch.cuda, 'empty_cache'):
                    torch.cuda.empty_cache()
            
            # Combine all transcribed text
            return " ".join(full_text) if full_text else None
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def run(self):
        """Run the speech-to-text demo."""
        try:
            # Setup audio stream
            stream = sd.InputStream(
                device=self.device_id,
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self.audio_callback,
                blocksize=self.blocksize
            )
            
            print("\nSpeech-to-Text Demo")
            print("====================")
            print("Press Enter to start/stop recording")
            print("Press Ctrl+C to exit")
            
            with stream:
                while True:
                    # Wait for user input
                    input("Press Enter to start recording...")
                    print("Recording... Press Enter to stop")
                    
                    # Start recording
                    self.is_recording = True
                    self.audio_frames.clear()
                    
                    # Wait for user to stop recording
                    input()
                    self.is_recording = False
                    
                    if self.audio_frames:
                        # Process recorded audio
                        print("Processing audio...")
                        audio_data = np.concatenate(self.audio_frames)
                        text = self.transcribe(audio_data)
                        
                        if text:
                            print(f"\nTranscription: {text}\n")
                        else:
                            print("\nNo transcription available\n")
                    else:
                        print("\nNo audio recorded\n")
                    
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error: {e}")

def main():
    app = SimpleSpeechToText()
    app.run()

if __name__ == "__main__":
    main()