"""
Command: tahutek - OI BACA AJG 

Trigger: Kirim pesan "tahutek" ke bot
Response: Ucapan Tahun Baru + Gambar personalized dengan call sign pengirim
"""

import sys
import os

# Tambahkan root project ke path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event_manager import get_event_by_trigger
from card_generator import generate_personalized_card
from card_host import upload_card
from statistics import log_callsign, log_event


def handle_command(from_call=None):
    """
    Handler untuk command 'tahutek'.

    Args:
        from_call: Call sign pengirim (opsional, untuk personalisasi)

    Returns:
        str: Pesan balasan ucapan Tahutek
    """
    event_key, event_config = get_event_by_trigger("tahutek")

    if not event_config:
        return "Event Tahu tek belum dikonfigurasi."

    greeting = event_config.get("greeting", "Selamat Tahun Baru 2026!")

    # Jika ada call sign pengirim, buat kartu personalized
    if from_call:
        # Log ke statistik
        log_callsign(from_call, event_config["name"], "tahutek")
        log_event("RECEIVED", from_call, "Command: tahutek")

        # Generate kartu ucapan personalized
        card_path = generate_personalized_card(from_call, event_config)
        card_url = None
        if card_path:
            log_event("CARD_GENERATED", from_call, f"Card: {card_path}")
            print(f"[TAHUTEK] Card generated for {from_call}: {card_path}")
            # Upload the generated greeting/QSL card so recipients can view it online.
            card_url = upload_card(card_path)
            if card_url:
                log_event("CARD_UPLOADED", from_call, f"URL: {card_url}")

        log_event("REPLIED", from_call, f"Greeting sent for Tahun Baru")

        # Format response dengan call sign
        response = f"Hai {from_call}! {greeting}"
        if card_url:
            response += f" Kartu/QSL: {card_url}"
        else:
            response += " Kartu dibuat lokal; link online gagal dibuat."
    else:
        response = greeting

    return response
