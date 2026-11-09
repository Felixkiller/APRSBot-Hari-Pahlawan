# APRSBot Hari Pahlawan

Bot APRS berbasis Python untuk menerima pesan melalui APRS-IS, menjalankan perintah acara, membalas pengirim, dan membuat kartu ucapan/QSL yang dipersonalisasi.

## Fitur

- Menerima pesan APRS melalui APRS-IS.
- Memproses perintah yang dimuat dari modul perintah.
- Mendukung perintah acara `merdeka` (Hari Pahlawan) dan `tahutek` (Tahu Tek), sesuai konfigurasi acara.
- Membuat kartu personal dan menyimpannya di `generated_cards/`.
- Mencatat aktivitas dan statistik ke berkas CSV di `logs/`.
- Dapat mencoba mengunggah kartu ke Catbox agar tautannya dapat dikirim melalui APRS.

> Perintah acara hanya aktif sesuai konfigurasi tanggal pada `config.py`. Modul perintah tambahan perlu tersedia di direktori yang digunakan aplikasi.

## Persyaratan

- Python 3.9 atau lebih baru direkomendasikan.
- Koneksi internet untuk mengakses APRS-IS dan, bila digunakan, Catbox.
- Kredensial APRS-IS yang valid untuk callsign bot.

## Instalasi

```bash
git clone https://github.com/Felixkiller/APRSBot-Hari-Pahlawan.git
cd APRSBot-Hari-Pahlawan
python -m venv .venv
```

Aktifkan lingkungan virtual, lalu pasang dependensi:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Konfigurasi dan keamanan

Sesuaikan pengaturan callsign dan koneksi APRS-IS di `config.py` sebelum menjalankan bot. Jangan membagikan atau melakukan commit passcode/kredensial. Jika kredensial yang pernah disimpan di repositori masih aktif, segera ganti atau cabut melalui layanan terkait dan gunakan nilai baru secara lokal.

## Menjalankan

```bash
python main.py
```

Bot akan terhubung ke APRS-IS dan menunggu pesan yang ditujukan ke callsign yang dikonfigurasi. Untuk acara Hari Pahlawan, gunakan perintah `merdeka`; untuk acara Tahu Tek, gunakan `tahutek` saat acara tersebut aktif.

Kartu yang dibuat disimpan di `generated_cards/`. Pengunggahan ke Catbox membutuhkan internet dan mungkin tidak selalu tersedia; kartu lokal tetap tersimpan jika unggah gagal.

## Struktur utama

- `main.py` — titik masuk, koneksi APRS-IS, dan pemrosesan pesan.
- `config.py` — callsign, server, direktori, dan pengaturan acara.
- `event_manager.py` — pemeriksaan acara aktif.
- `card_generator.py` — pembuatan kartu.
- `card_host.py` — pengunggahan kartu.
- `statistics.py` — pencatatan statistik dan aktivitas.
- `requirements.txt` — dependensi Python.
- `commands/` — kode perintah yang ada di repositori.
- `generated_cards/` — keluaran kartu.

## Dependensi

Dependensi utama tercantum di `requirements.txt`: `aprslib`, `Pillow`, `tzdata`, dan `qrcode`.
