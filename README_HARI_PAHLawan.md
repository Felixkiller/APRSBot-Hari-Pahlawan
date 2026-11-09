# Uji Coba APRS Bot — Hari Pahlawan 10 November 2026

- Command yang diproses: `MERDEKA` (tidak peka huruf besar/kecil).
- Template latar: `modules/images/hari_pahlawan_2026.jpg` (gambar yang diberikan).
- Bot membuat kartu personal dengan callsign pengirim, lalu mencoba mengunggahnya ke Catbox agar URL dapat dibalas melalui APRS.
- Contoh standar uji: kirim pesan APRS ke `YC3ADM-10` dengan isi `MERDEKA`.

## Konfigurasi sebelum menjalankan

Di `config.py`, isi `CALLSIGN` dengan callsign bot yang benar-benar akan menerima pesan dan atur `PASSCODE` milik callsign tersebut. Instruksi uji menyebut `YC3ADM-10`; pastikan ini memang callsign bot yang digunakan. Jangan memakai passcode milik callsign lain.

## Logo UKDC dan ORARI

ZIP ini menggunakan label teks `UKDC | ORARI` sebagai penanda sementara. Gambar yang diberikan tidak memuat logo resmi UKDC/ORARI, sehingga logo resmi belum ditempelkan. Letakkan file logo PNG transparan yang resmi jika ingin dipasang di kartu.

## Install & run (Windows)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Uji sintaks tidak sama dengan uji koneksi APRS-IS/Catbox; koneksi harus diuji di jaringan dan dengan kredensial yang valid.