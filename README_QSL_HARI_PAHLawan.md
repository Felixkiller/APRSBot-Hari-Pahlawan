# QSL Card Hari Pahlawan — APRSBot

## Format uji coba
- Tujuan pesan APRS: `YC3ADM-10`
- Isi pesan: `MERDEKA`
- Stasiun pada desain QSL: `YC3ADM`
- Tanggal acara pada kartu: 10 November 2026

## Desain
- Logo UKDC pada bagian kiri atas memakai file resmi `modules/images/ukdc_logo.png`; logo ORARI pada template tetap digunakan.
- Call sign pengirim APRS dimasukkan otomatis pada bagian tengah kartu.
- Informasi BAND/FREQ/MODE mengikuti contoh (2M / 144.390 / APRS).
- UTC dan RST ditampilkan `--:--:--` dan `N/A` karena data tersebut belum disediakan oleh pesan APRS biasa. Jangan menganggapnya sebagai hasil pengukuran radio.
- QR Code mengarah ke pencarian callsign penerima di APRS.fi.

## Menjalankan
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```
Untuk membuat dan memeriksa kartu secara lokal tanpa koneksi APRS-IS:
```powershell
.\.venv\Scripts\python.exe -c "import test_bot; test_bot.test_card_generator()"
```
Tes ini membuat kartu contoh untuk `YB3TEST-9` di folder `generated_cards`.

Pastikan `CALLSIGN` dan `PASSCODE` di `config.py` adalah kredensial APRS-IS yang benar untuk stasiun bot. Passcode lama tidak otomatis berlaku untuk callsign berbeda. Setelah konfigurasi benar, kirim pesan `MERDEKA` ke `YC3ADM-10`.

Kartu hasil dibuat di folder `generated_cards`. Upload publik membutuhkan koneksi internet dan layanan Catbox yang dapat dijangkau.
