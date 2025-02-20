# Hotkey Dikte

Program speech-to-text sederhana menggunakan Whisper AI untuk mengubah suara menjadi teks secara real-time dengan hotkey. Cocok untuk pengguna yang ingin mendiktekan teks dengan cepat dan mudah.

## Fitur

- 🎙️ Transkripsi suara ke teks real-time menggunakan Whisper AI
- ⌨️ Hotkey kustomisasi untuk kontrol rekaman (default: CTRL+ALT+SPACE)
- ⚙️ Konfigurasi yang fleksibel dan mudah disesuaikan
- 🇮🇩 Dukungan penuh untuk Bahasa Indonesia
- 🖥️ Berjalan di system tray untuk penggunaan yang nyaman

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- CUDA-capable GPU (opsional, untuk performa optimal)
- Mikrofon yang berfungsi dengan baik
- Sistem Operasi: Windows

## Dependencies

- sounddevice - untuk perekaman audio
- numpy - untuk pemrosesan data audio
- openai-whisper - model AI untuk speech recognition
- pyautogui - untuk input teks otomatis
- keyboard - untuk manajemen hotkey
- pystray - untuk sistem tray icon
- Pillow - untuk pemrosesan gambar icon

## Instalasi

1. Install [Anaconda](https://www.anaconda.com/download) atau [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. Buka Anaconda Prompt dan buat environment baru:
   ```bash
   conda create -n dikte python=3.8
   conda activate dikte
   ```

3. Clone repository ini atau download sebagai ZIP:
   ```bash
   git clone https://github.com/username/hotkey-dikte.git
   cd hotkey-dikte
   ```

4. Install dependencies yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

5. Setup shortcut (opsional):
   - Buat shortcut untuk `dikte.vbs`
   - Klik kanan shortcut > Properties
   - Centang "Run as administrator"
   - Untuk autostart: copy shortcut ke `shell:startup`

## Penggunaan

1. Aktifkan environment conda:
   ```bash
   conda activate dikte
   ```

2. Jalankan aplikasi:
   - Double click `hotkey_dikte.bat`, atau
   - Jalankan `python app.py` di terminal

3. Program akan berjalan di system tray (icon mikrofon)
   - 🟢 Hijau: Siap digunakan
   - 🔴 Merah: Sedang merekam
   - 🟡 Kuning: Memproses audio

4. Penggunaan dasar:
   - Tekan CTRL+ALT+SPACE untuk mulai merekam
   - Bicara dengan jelas dan tidak terlalu cepat
   - Lepas hotkey untuk mengkonversi suara ke teks
   - Klik kanan pada icon tray untuk menu tambahan

## Konfigurasi

Edit file `config.json` untuk menyesuaikan pengaturan:

```json
{
    "sample_rate": 16000,
    "device_id": null,
    "hotkey": "ctrl+alt+space",
    "exit_hotkey": "ctrl+alt+q",
    "model_size": "base",
    "language": "id",
    "initial_prompt": ""
}
```

- `sample_rate`: Sample rate audio (default: 16000)
- `device_id`: ID perangkat audio input (null untuk default)
- `hotkey`: Kombinasi tombol untuk trigger rekaman
- `exit_hotkey`: Kombinasi tombol untuk keluar aplikasi
- `model_size`: Ukuran model Whisper ("tiny", "base", "small", "medium", "large")
- `language`: Kode bahasa ("id" untuk Indonesia)
- `initial_prompt`: Prompt awal untuk meningkatkan akurasi (opsional)

## Troubleshooting

1. **Tidak ada suara terekam**
   - Pastikan mikrofon terpasang dengan benar
   - Periksa `device_id` di config.json
   - Periksa izin mikrofon di Windows

2. **Hasil transkripsi tidak akurat**
   - Coba gunakan model yang lebih besar
   - Bicara lebih jelas dan pelan
   - Sesuaikan `initial_prompt` untuk konteks spesifik

3. **Program tidak berjalan**
   - Pastikan semua dependencies terinstall
   - Jalankan sebagai administrator
   - Periksa log error di terminal

## Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b fitur-keren`)
3. Commit perubahan (`git commit -am 'Menambah fitur keren'`)
4. Push ke branch (`git push origin fitur-keren`)
5. Buat Pull Request

## Lisensi

MIT License - Lihat [LICENSE](LICENSE) untuk detail lebih lanjut.

## Kredit

Dibuat dengan ❤️ menggunakan:
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Python](https://www.python.org/)
