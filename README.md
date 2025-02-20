# 🎙️ Hotkey Dikte

Program speech-to-text sederhana menggunakan Whisper AI untuk mengubah suara menjadi teks secara real-time dengan hotkey. Cocok untuk pengguna yang ingin mendiktekan teks dengan cepat dan mudah.

## ✨ Fitur

- 🎙️ Transkripsi suara ke teks real-time menggunakan Whisper AI
- ⌨️ Hotkey kustomisasi untuk kontrol rekaman (default: CTRL+ALT+SPACE)
- 🚪 Hotkey untuk keluar dari aplikasi (default: CTRL+ALT+Q)
- ⚙️ Konfigurasi yang fleksibel dan mudah disesuaikan
- 🇮🇩 Dukungan penuh untuk Bahasa Indonesia
- 📝 Logging system untuk troubleshooting
- 🖥️ Berjalan di system tray dengan indikator status

## 💻 Persyaratan Sistem

- Python 3.8 atau lebih baru
- CUDA-capable GPU (opsional, untuk performa optimal)
- Mikrofon yang berfungsi dengan baik
- Sistem Operasi: Windows

## 📦 Dependencies

- sounddevice - untuk perekaman audio
- numpy - untuk pemrosesan data audio
- openai-whisper - model AI untuk speech recognition
- pyautogui - untuk input teks otomatis
- keyboard - untuk manajemen hotkey
- pystray - untuk sistem tray icon
- Pillow - untuk pemrosesan gambar icon
- torch - untuk Whisper AI

## 🚀 Instalasi

1. Install [Anaconda](https://www.anaconda.com/download) atau [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. Clone repository ini atau download sebagai ZIP:
   ```bash
   git clone https://github.com/username/hotkey-dikte.git
   cd hotkey-dikte
   ```

3. Buat environment baru:
   ```bash
   conda create -n dikte python=3.8
   conda activate dikte
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

## 🎯 Penggunaan

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

## ⚙️ Konfigurasi

Konfigurasi dapat diubah melalui file `config.json` dengan format berikut:

```json
{
    "sample_rate": 16000,
    "device_id": 1,
    "hotkey": "ctrl+alt+space",
    "exit_hotkey": "ctrl+alt+q",
    "model_size": "medium",
    "language": "id",
    "initial_prompt": "Transkripsi percakapan Bahasa Indonesia dengan jelas dan akurat."
}
```

## 🔧 Troubleshooting

1. **Mikrofon tidak terdeteksi**
   - Pastikan mikrofon terpasang dengan benar
   - Cek pengaturan mikrofon di Windows
   - Sesuaikan `device_id` di config

2. **Transkripsi tidak akurat**
   - Bicara lebih jelas dan pelan
   - Coba ganti `model_size` ke "large"
   - Sesuaikan `initial_prompt`

3. **Program tidak merespon**
   - Restart program
   - Cek log di console
   - Pastikan hotkey tidak konflik

## 📄 Lisensi

Dilepaskan di bawah lisensi MIT. Lihat file `LICENSE` untuk detailnya.
