import json
import os

class HistoryManager:
    def __init__(self, filename="history.json"):
        self.filename = filename
        # Stwórz plik, jeśli nie istnieje
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def save_entry(self, original_text, ai_response):
        """Zapisuje nowe zapytanie do pliku JSON."""
        history = self.load_all()
        entry = {
            "timestamp": os.path.getmtime(self.filename), # prosty znacznik czasu
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