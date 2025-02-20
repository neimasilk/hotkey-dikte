# Hotkey Dikte

Program speech-to-text sederhana menggunakan Whisper AI. Program ini dapat mengubah suara menjadi teks secara real-time dengan menekan hotkey.

## Fitur

- Transkripsi suara ke teks menggunakan Whisper AI
- Hotkey untuk mulai/stop rekaman (default: CTRL+ALT+SPACE)
- Hotkey untuk keluar dari aplikasi (default: CTRL+ALT+Q)
- Konfigurasi yang dapat disesuaikan
- Mendukung Bahasa Indonesia
- Logging system untuk troubleshooting
- System tray icon dengan status indikator

## Persyaratan

- Python 3.8+
- CUDA-capable GPU (untuk performa optimal)
- Dependencies:
  - sounddevice
  - numpy
  - openai-whisper
  - pyautogui
  - keyboard
  - torch (untuk Whisper AI)

## Instalasi

1. Install Anaconda dari https://www.anaconda.com/download

2. Clone repository ini:
   ```bash
   git clone https://github.com/yourusername/hotkey-dikte.git
   cd hotkey-dikte
   ```

3. Buat environment baru:
   ```bash
   conda create -n dikte python=3.8
   conda activate dikte
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Penggunaan

1. Jalankan program dengan perintah:
   ```bash
   python app.py
   ```

2. Program akan berjalan di system tray (icon mikrofon)
3. Gunakan hotkey berikut:
   - CTRL+ALT+SPACE: Mulai/stop merekam
   - CTRL+ALT+Q: Keluar dari aplikasi
4. Bicara dengan jelas saat merekam
5. Lepas hotkey untuk mengubah suara menjadi teks
6. Klik kanan pada icon tray untuk melihat menu dan keluar

## Konfigurasi

Edit `config.json` untuk menyesuaikan:

### Audio Settings
- `sample_rate`: Sample rate audio (default: 16000)
- `device_id`: ID perangkat audio input
- `channels`: Jumlah channel audio (default: 1)
- `blocksize`: Ukuran block audio (default: 1024)

### Transcriber Settings
- `model_size`: Ukuran model Whisper ("tiny", "base", "small", "medium", "large")
- `language`: Kode bahasa ("id" untuk Indonesia)
- `initial_prompt`: Prompt awal untuk meningkatkan akurasi
- `use_cuda`: Gunakan GPU untuk transcription (true/false)

### Hotkey Settings
- `record_hotkey`: Hotkey untuk mulai/stop rekaman (default: "ctrl+alt+space")
- `exit_hotkey`: Hotkey untuk keluar aplikasi (default: "ctrl+alt+q")

### Logging Settings
- `log_path`: Path untuk file log (default: "app.log")

## Troubleshooting

1. **No audio device found**:
   - Pastikan microphone terpasang dan berfungsi
   - Cek device_id di config.json

2. **CUDA not available**:
   - Pastikan driver NVIDIA terinstall
   - Cek instalasi PyTorch dengan CUDA support

3. **Transcription tidak akurat**:
   - Gunakan model yang lebih besar ("medium" atau "large")
   - Sesuaikan initial_prompt
   - Bicara lebih jelas dan pelan

## Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b fitur-keren`)
3. Commit perubahan (`git commit -am 'Menambah fitur keren'`)
4. Push ke branch (`git push origin fitur-keren`)
5. Buat Pull Request

## Lisensi

MIT License - Lihat [LICENSE](LICENSE) untuk detail lebih lanjut.
