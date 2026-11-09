"""Upload kartu APRS ke Catbox.moe dan mengembalikan URL publik."""
import mimetypes
import os
import uuid
import urllib.request


def upload_card(path):
    """Upload file gambar ke Catbox. Return URL atau None jika gagal."""
    if not path or not os.path.isfile(path):
        return None
    boundary = "----APRSBot" + uuid.uuid4().hex
    filename = os.path.basename(path)
    mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        data = f.read()
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        "fileupload\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        "https://catbox.moe/user/api.php",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                 "User-Agent": "APRSBot-UKDC/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            url = response.read().decode("utf-8", errors="replace").strip()
        if url.startswith("https://files.catbox.moe/"):
            print(f"[UPLOAD] Public card URL: {url}")
            return url
        print(f"[UPLOAD] Catbox returned unexpected response: {url[:200]}")
    except Exception as exc:
        print(f"[UPLOAD] Failed to upload {filename}: {exc}")
    return None