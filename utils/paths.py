"""Ścieżki liczone względem katalogu projektu (niezależnie od tego, skąd uruchomiono aplikację)."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
HISTORY_PATH = os.path.join(BASE_DIR, "history.json")
ENV_PATH = os.path.join(BASE_DIR, ".env")
