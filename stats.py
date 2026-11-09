"""
Command: stats - Laporan Statistik
APRS Bot Ilmu Informatika UKDC

Trigger: Kirim pesan "stats" ke bot
Response: Ringkasan statistik call sign pengirim
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from statistics import format_stats_report, log_event


def handle_command(from_call=None):
    """
    Handler untuk command 'stats'.

    Args:
        from_call: Call sign pengirim

    Returns:
        str: Ringkasan statistik
    """
    if from_call:
        log_event("STATS_REQUEST", from_call, "Requested statistics")

    report = format_stats_report()
    return report
