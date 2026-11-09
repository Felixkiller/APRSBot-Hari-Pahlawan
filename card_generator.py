"""
Modul Pembuat Kartu Ucapan - APRS Bot Ilmu Informatika UKDC

Membuat gambar kartu ucapan yang dipersonalisasi dengan:
- Gambar perayaan sebagai background
- Call sign pengirim yang ditampilkan di gambar
- Watermark Ilmu Informatika UKDC
"""

import os
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - Pillow is optional at runtime
    Image = None
    ImageDraw = None
    ImageFont = None

from config import GENERATED_CARDS_DIR, TIMEZONE


def _get_local_time():
    """Mendapatkan waktu lokal WIB."""
    try:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    except ImportError:
        pass
    else:
        try:
            return datetime.now(ZoneInfo(TIMEZONE))
        except ZoneInfoNotFoundError:
            pass

    from datetime import timedelta, timezone
    wib = timezone(timedelta(hours=7))
    return datetime.now(wib)


def generate_personalized_card(callsign, event_config):
    """
    Membuat kartu ucapan yang dipersonalisasi dengan call sign pengirim.

    Menggunakan library Pillow (PIL) untuk menggabungkan gambar perayaan
    dengan teks call sign pengirim.

    Args:
        callsign: Call sign pengirim APRS
        event_config: Dictionary konfigurasi event dari EVENTS_2026

    Returns:
        str: Path ke file gambar yang dihasilkan, atau None jika gagal
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[CARD] ERROR: Pillow library not installed. Run: pip install Pillow")
        return None

    event_name = event_config.get("name", "Event")
    base_image_path = event_config.get("image", "")

    if not os.path.exists(base_image_path):
        print(f"[CARD] WARNING: Base image not found: {base_image_path}")
        return _generate_fallback_card(callsign, event_config)

    # QSL Hari Pahlawan memakai contoh kartu yang diberikan pengguna.
    # Logo UKDC dan ORARI sudah tertanam pada template asli.
    if event_config.get("command_trigger") == "merdeka":
        return _generate_hari_pahlawan_qsl(callsign, event_config, base_image_path)

    try:
        # Buka gambar dasar
        img = Image.open(base_image_path).copy()
        # Upscale the supplied square template so QSL text is readable.
        if event_config.get("command_trigger") == "merdeka":
            img = img.convert("RGB").resize((1000, 1000), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Coba gunakan font yang tersedia
        font_large = _get_font(size=max(36, int(height * 0.05)))
        font_medium = _get_font(size=max(24, int(height * 0.035)))
        font_small = _get_font(size=max(18, int(height * 0.025)))

        # ---- Banner Call Sign di bagian bawah ----
        banner_height = int(height * 0.18)
        banner_y = height - banner_height

        # Buat semi-transparent overlay untuk banner
        # Tema merah-putih untuk Hari Pahlawan; event lain tetap memakai biru gelap.
        is_hari_pahlawan = event_config.get("command_trigger") == "merdeka"
        banner_color = (155, 0, 24, 220) if is_hari_pahlawan else (0, 0, 50, 200)
        overlay = Image.new("RGBA", (width, banner_height), banner_color)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        img.paste(overlay, (0, banner_y), overlay)

        draw = ImageDraw.Draw(img)

        # Teks call sign
        cs_text = f"Kepada: {callsign}"
        cs_bbox = draw.textbbox((0, 0), cs_text, font=font_large)
        cs_w = cs_bbox[2] - cs_bbox[0]
        cs_x = (width - cs_w) // 2
        cs_y = banner_y + int(banner_height * 0.28) if event_config.get("command_trigger") == "merdeka" else banner_y + int(banner_height * 0.15)

        # Shadow effect
        draw.text((cs_x + 2, cs_y + 2), cs_text, fill=(0, 0, 0, 200), font=font_large)
        # Teks utama
        draw.text((cs_x, cs_y), cs_text, fill=(255, 215, 0, 255), font=font_large)

        # Teks waktu
        now = _get_local_time()
        time_text = f"{now.strftime('%d %B %Y %H:%M WIB')}"
        time_bbox = draw.textbbox((0, 0), time_text, font=font_small)
        time_w = time_bbox[2] - time_bbox[0]
        time_x = (width - time_w) // 2
        time_y = cs_y + (cs_bbox[3] - cs_bbox[1]) + 10
        draw.text((time_x, time_y), time_text, fill=(200, 200, 200, 255), font=font_small)

        # Teks institusi
        inst_text = "Ilmu Informatika UKDC"
        inst_bbox = draw.textbbox((0, 0), inst_text, font=font_medium)
        inst_w = inst_bbox[2] - inst_bbox[0]
        inst_x = (width - inst_w) // 2
        inst_y = time_y + (time_bbox[3] - time_bbox[1]) + 5
        draw.text((inst_x, inst_y), inst_text, fill=(255, 255, 255, 255), font=font_medium)

        # Branding acara. Teks ini tidak menggantikan file logo resmi;
        # logo UKDC dan ORARI dapat ditambahkan sebagai PNG transparan.
        branding = event_config.get("branding")
        if branding:
            brand_font = _get_font(size=max(18, int(height * 0.025)))
            brand_bbox = draw.textbbox((0, 0), branding, font=brand_font)
            brand_w = brand_bbox[2] - brand_bbox[0]
            brand_y = banner_y + 8
            draw.text(((width - brand_w) // 2, brand_y), branding, fill=(255, 255, 255, 255), font=brand_font)
        subtitle = event_config.get("subtitle")
        if subtitle:
            sub_font = _get_font(size=max(14, int(height * 0.021)))
            sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
            sub_w = sub_bbox[2] - sub_bbox[0]
            # Place subtitle in a compact red strip at the top.
            strip_h = max(34, int(height * 0.08))
            top_overlay = Image.new("RGBA", (width, strip_h), (155, 0, 24, 225))
            img.paste(top_overlay, (0, 0), top_overlay)
            draw = ImageDraw.Draw(img)
            draw.text((max(8, (width - sub_w) // 2), max(4, (strip_h - (sub_bbox[3]-sub_bbox[1])) // 2)), subtitle, fill=(255,255,255,255), font=sub_font)

        # ---- Simpan hasil ----
        safe_callsign = callsign.replace("/", "_").replace("\\", "_")
        event_key = event_config.get("command_trigger", "event")
        filename = f"{event_key}_{safe_callsign}_{now.strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(GENERATED_CARDS_DIR, filename)

        # Convert ke RGB jika perlu (untuk JPEG compatibility)
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (0, 0, 50))
            bg.paste(img, mask=img.split()[3])
            bg.save(output_path, quality=95)
        else:
            img.save(output_path, quality=95)

        print(f"[CARD] Generated: {output_path}")
        return output_path

    except Exception as e:
        print(f"[CARD] Error generating card: {e}")
        return _generate_fallback_card(callsign, event_config)


def _generate_fallback_card(callsign, event_config):
    """
    Membuat kartu ucapan sederhana jika gambar dasar tidak tersedia.

    Args:
        callsign: Call sign pengirim
        event_config: Konfigurasi event

    Returns:
        str: Path ke file gambar fallback
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[CARD] ERROR: Pillow not available for fallback card")
        return None

    try:
        width, height = 800, 600
        img = Image.new("RGB", (width, height), (10, 10, 60))
        draw = ImageDraw.Draw(img)

        font_large = _get_font(size=40)
        font_medium = _get_font(size=28)
        font_small = _get_font(size=20)

        event_name = event_config.get("name", "Perayaan 2026")

        # Judul event
        title_bbox = draw.textbbox((0, 0), event_name, font=font_large)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(
            ((width - title_w) // 2, 80),
            event_name,
            fill=(255, 215, 0),
            font=font_large,
        )

        # Nama institusi
        inst = "Ilmu Informatika UKDC"
        inst_bbox = draw.textbbox((0, 0), inst, font=font_medium)
        inst_w = inst_bbox[2] - inst_bbox[0]
        draw.text(
            ((width - inst_w) // 2, 150),
            inst,
            fill=(255, 255, 255),
            font=font_medium,
        )

        # Call sign
        cs_text = f"Kepada: {callsign}"
        cs_bbox = draw.textbbox((0, 0), cs_text, font=font_large)
        cs_w = cs_bbox[2] - cs_bbox[0]
        draw.text(
            ((width - cs_w) // 2, 300),
            cs_text,
            fill=(255, 215, 0),
            font=font_large,
        )

        # Greeting
        greeting = event_config.get("greeting", "Selamat merayakan!")
        # Wrap greeting text
        words = greeting.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font_small)
            if bbox[2] - bbox[0] > width - 80:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        y_offset = 400
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font_small)
            line_w = line_bbox[2] - line_bbox[0]
            draw.text(
                ((width - line_w) // 2, y_offset),
                line,
                fill=(200, 200, 200),
                font=font_small,
            )
            y_offset += 30

        # Simpan
        safe_callsign = callsign.replace("/", "_").replace("\\", "_")
        event_key = event_config.get("command_trigger", "event")
        now = _get_local_time()
        filename = f"{event_key}_{safe_callsign}_{now.strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(GENERATED_CARDS_DIR, filename)
        img.save(output_path, quality=95)

        print(f"[CARD] Fallback generated: {output_path}")
        return output_path

    except Exception as e:
        print(f"[CARD] Error generating fallback card: {e}")
        return None


def _get_font(size=24):
    """
    Mendapatkan font yang tersedia di sistem.

    Args:
        size: Ukuran font

    Returns:
        ImageFont: Font object
    """
    from PIL import ImageFont

    # Daftar font yang umum tersedia
    font_paths = [
        # Windows fonts
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        # Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        # macOS fonts
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue

    # Fallback ke default font
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()



def _generate_hari_pahlawan_qsl(callsign, event_config, template_path):
    """Buat QSL card landscape Hari Pahlawan berdasarkan contoh pengguna."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import qrcode
    except ImportError as exc:
        print(f"[CARD] QSL dependencies missing: {exc}. Install requirements.txt")
        return None

    try:
        # Rasio dan komposisi dipertahankan dari contoh asli 814x574.
        img = Image.open(template_path).convert("RGB").resize((1221, 861), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img, "RGBA")
        scale = 1.5

        def xy(box):
            return tuple(int(v * scale) for v in box)

        logo_path = os.path.join(os.path.dirname(template_path), "ukdc_logo.png")
        with Image.open(logo_path) as logo_file:
            logo = logo_file.convert("RGBA")
        logo = logo.resize(xy((88, 85)), Image.Resampling.LANCZOS)
        img.paste(logo, xy((23, 49)), logo)
        draw = ImageDraw.Draw(img, "RGBA")

        def font(size, bold=False):
            candidates = [
                "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
            for candidate in candidates:
                if os.path.exists(candidate):
                    return ImageFont.truetype(candidate, int(size * scale))
            return ImageFont.load_default()

        # Panel tengah menutup data contoh (YD3ADB/Brielt dan data QSO 2025),
        # tetapi tidak menutupi logo UKDC/ORARI atau ilustrasi utama.
        panel = xy((252, 222, 760, 410))
        draw.rounded_rectangle(panel, radius=int(12*scale), fill=(244, 226, 177, 232), outline=(87, 53, 30, 245), width=int(2*scale))

        def centered(text, y, fnt, fill, x0=260, x1=752, stroke_width=0, stroke_fill=(0,0,0,255)):
            box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
            w = box[2] - box[0]
            draw.text((int((x0 + (x1-x0)/2)*scale - w/2), int(y*scale)), text,
                      font=fnt, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

        centered("THIS QSL CARD IS GIVEN TO", 232, font(13, True), (75, 55, 38, 255))
        clean_call = str(callsign or "UNKNOWN").strip().upper()[:18]
        centered(clean_call, 252, font(38, True), (174, 30, 39, 255), stroke_width=1, stroke_fill=(255,245,220,255))
        centered("TERIMA KASIH TELAH BERPARTISIPASI", 300, font(13, True), (55, 63, 80, 255))
        centered("SPECIAL EVENT STATION • YC3ADM", 322, font(15, True), (70, 48, 30, 255))

        # Data event/QSL. Frekuensi dan mode mengikuti contoh; RST tidak
        # diklaim sebagai hasil pengukuran, sehingga ditandai N/A.
        row = xy((266, 350, 746, 399))
        draw.rounded_rectangle(row, radius=int(5*scale), fill=(255, 248, 226, 238), outline=(130, 91, 48, 220), width=int(scale))
        cols = [
            ("DATE", "10 NOV 2026"), ("UTC", "--:--:--"),
            ("BAND", "2M"), ("FREQ", "144.390"), ("MODE", "APRS"), ("RST", "N/A"),
        ]
        left, right = 270, 742
        colw = (right-left)/len(cols)
        for i, (label, value) in enumerate(cols):
            cx = left + colw*(i+0.5)
            for text, yy, fnt, color in [
                (label, 354, font(10, True), (65, 55, 45, 255)),
                (value, 374, font(10, False), (30, 30, 30, 255)),
            ]:
                bb = draw.textbbox((0,0), text, font=fnt)
                draw.text((int(cx*scale-(bb[2]-bb[0])/2), int(yy*scale)), text, font=fnt, fill=color)

        # QR dinamis menuju halaman APRS.fi untuk callsign penerima.
        qr_payload = f"https://aprs.fi/?call={clean_call}"
        qr = qrcode.QRCode(version=3, box_size=5, border=2)
        qr.add_data(qr_payload)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_img.thumbnail((105, 105), Image.Resampling.NEAREST)
        # Letakkan QR pada area QR contoh di kanan bawah, di atas kode lama.
        qr_img = qr_img.resize((105,105), Image.Resampling.NEAREST)
        qx, qy = xy((500, 445))
        draw.rectangle(xy((495, 440, 610, 560)), fill=(245, 229, 190, 245), outline=(80,55,35,255), width=int(2*scale))
        img.paste(qr_img, (qx, qy))
        draw = ImageDraw.Draw(img, "RGBA")
        draw.text(xy((502, 543)), "SCAN: APRS.FI", font=font(7, True), fill=(50,40,30,255))

        draw.rectangle(xy((456, 176, 705, 208)), fill=(115, 74, 40, 255))
        draw.text(xy((470, 179)), "10 NOVEMBER 2026", font=font(17, True), fill=(255,255,255,255))

        now = _get_local_time()
        os.makedirs(GENERATED_CARDS_DIR, exist_ok=True)
        safe_callsign = "".join(c if c.isalnum() or c in "-_" else "_" for c in clean_call)
        filename = f"qsl_hari_pahlawan_{safe_callsign}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
        output_path = os.path.join(GENERATED_CARDS_DIR, filename)
        img.save(output_path, quality=94, optimize=True)
        print(f"[CARD] Hari Pahlawan QSL generated: {output_path}")
        return output_path
    except Exception as exc:
        print(f"[CARD] QSL generation failed: {exc}")
        return _generate_fallback_card(callsign, event_config)