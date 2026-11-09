# APRSBot - perbaikan struktur ZIP dan impor VS Code

ZIP ini sudah dirapikan agar folder proyek tidak bersarang tiga kali dan tidak membawa `.venv` dari komputer lain. Buka folder yang berisi `main.py`, `config.py`, `event_manager.py`, dan `card_generator.py` langsung di VS Code.

## Menyiapkan Python di Windows

Buka Terminal di folder proyek dan jalankan:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m compileall -q .
```

Pilih interpreter `.venv\Scripts\python.exe` melalui `Ctrl+Shift+P` -> `Python: Select Interpreter`. Kemudian gunakan `Ctrl+Shift+P` -> `Pylance: Restart Language Server`.

## Jika Pylance masih tidak menemukan modul lokal

Pastikan file `config.py`, `event_manager.py`, `card_generator.py`, dan `statistics.py` berada satu tingkat dengan `main.py`. Jangan membuka folder induk/luar yang hanya berisi folder `APRSBot-main` lain.

## Catatan Catbox

`card_host.py` menggunakan endpoint Catbox untuk mencoba menghasilkan URL publik. Upload dan pengiriman APRS-IS memerlukan koneksi internet dan belum bisa dijamin berhasil hanya dari pemeriksaan kode.
