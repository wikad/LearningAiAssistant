import json
import os
import time

from utils.paths import HISTORY_PATH

class HistoryManager:
    def __init__(self, filename=HISTORY_PATH):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def save_entry(self, original_text, ai_response):
        history = self.load_all()
        entry = {
            "timestamp": time.time(),
            "input": original_text,
            "output": ai_response
        }
        history.append(entry)
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def load_all(self):
        """Wczytuje całą historię z pliku."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []