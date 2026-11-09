"""
Command: help - Bantuan
APRS Bot Ilmu Informatika UKDC

Trigger: Kirim pesan "help" ke bot
Response: Daftar perintah yang tersedia
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event_manager import get_all_triggers, get_active_events
from statistics import log_event


def handle_command(from_call=None):
    """
    Handler untuk command 'help'.

    Args:
        from_call: Call sign pengirim

    Returns:
        str: Daftar perintah yang tersedia
    """
    if from_call:
        log_event("HELP_REQUEST", from_call, "Requested help")

    triggers = get_all_triggers()
    active_events = get_active_events()

    response_parts = [
        "APRS Bot Informatika UKDC.",
        "Perintah: " + ", ".join(triggers) + ", stats, help, report.",
    ]

    if active_events:
        active_names = [e[1]["name"] for e in active_events]
        response_parts.append("Aktif: " + ", ".join(active_names))
    else:
        response_parts.append("Tidak ada event aktif saat ini.")

    return " ".join(response_parts)
