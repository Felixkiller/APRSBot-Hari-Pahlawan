"""
Command: report - Export Laporan Statistik Lengkap
APRS Bot Ilmu Informatika UKDC

Trigger: Kirim pesan "report" ke bot
Response: Menggenerate laporan statistik lengkap dan memberi notifikasi
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from statistics import export_full_report, log_event


def handle_command(from_call=None):
    """
    Handler untuk command 'report'.

    Args:
        from_call: Call sign pengirim

    Returns:
        str: Konfirmasi pembuatan laporan
    """
    if from_call:
        log_event("REPORT_REQUEST", from_call, "Requested full report")

    try:
        report_path = export_full_report()
        filename = os.path.basename(report_path)
        return (
            f"Laporan statistik berhasil dibuat: {filename}. "
            f"Informatika UKDC APRS Bot."
        )
    except Exception as e:
        return f"Error membuat laporan: {str(e)}"
