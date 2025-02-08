# Hotkey Dikte

Program speech-to-text sederhana menggunakan Whisper AI. Program ini dapat mengubah suara menjadi teks secara real-time dengan menekan hotkey.

## Fitur

- Transkripsi suara ke teks menggunakan Whisper AI
- Hotkey untuk mulai/stop rekaman (default: CTRL+ALT+SPACE)
- Konfigurasi yang dapat disesuaikan
- Mendukung Bahasa Indonesia

## Persyaratan

- Python 3.8+
- CUDA-capable GPU (untuk performa optimal)
- Dependencies:
  - sounddevice
  - numpy
  - openai-whisper
  - pyautogui
  - keyboard

## Instalasi

## Penggunaan

1. Jalankan program dengan double click `hotkey_dikte.bat` atau:

2. Program akan berjalan di system tray (icon mikrofon)
3. Tekan CTRL+ALT+SPACE untuk mulai/stop merekam
4. Bicara dengan jelas
5. Lepas hotkey untuk mengubah suara menjadi teks
6. Klik kanan pada icon untuk melihat menu dan keluar

## Konfigurasi

Edit `config.json` untuk menyesuaikan:
- `sample_rate`: Sample rate audio (default: 16000)
- `device_id`: ID perangkat audio input
- `hotkey`: Kombinasi tombol untuk trigger
- `model_size`: Ukuran model Whisper ("tiny", "base", "small", "medium", "large")
- `language`: Kode bahasa ("id" untuk Indonesia)

## Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b fitur-keren`)
3. Commit perubahan (`git commit -am 'Menambah fitur keren'`)
4. Push ke branch (`git push origin fitur-keren`)
5. Buat Pull Request

## Lisensi

MIT License - Lihat [LICENSE](LICENSE) untuk detail lebih lanjut.
