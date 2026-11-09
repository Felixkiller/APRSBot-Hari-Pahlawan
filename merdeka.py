"""Command MERDEKA untuk uji coba QSL Card Hari Pahlawan 10 November 2026."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from event_manager import get_event_by_trigger
from card_generator import generate_personalized_card
from card_host import upload_card
from statistics import log_callsign, log_event

def handle_command(from_call=None):
    event_key, event_config = get_event_by_trigger("merdeka")
    if not event_config:
        return "Event Hari Pahlawan belum dikonfigurasi."
    greeting = event_config.get("greeting", "Selamat Hari Pahlawan! MERDEKA!")
    if not from_call:
        return greeting
    log_callsign(from_call, event_config["name"], "merdeka")
    log_event("RECEIVED", from_call, "Command: MERDEKA")
    card_path = generate_personalized_card(from_call, event_config)
    card_url = upload_card(card_path) if card_path else None
    if card_path:
        log_event("CARD_GENERATED", from_call, f"Card: {card_path}")
    if card_url:
        log_event("CARD_UPLOADED", from_call, f"URL: {card_url}")
        return f"{greeting} QSL: {card_url}"
    return f"{greeting} QSL dibuat lokal; upload Catbox gagal, cek log bot."
