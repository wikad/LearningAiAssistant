import json
from pynput import keyboard

class ConfigLoader:
    def __init__(self, path="config.json"):
        self.path = path

    def _parse_key(self, key_str):
        """Zamienia string na obiekt klawisza pynput."""
        if hasattr(keyboard.Key, key_str):
            return getattr(keyboard.Key, key_str)
        return keyboard.KeyCode(char=key_str)

    def load_hotkeys(self):
        """Ładuje i zwraca tylko przetworzoną sekcję hotkeys."""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            raw_hotkeys = data.get("hotkeys", {})
            processed = {}

            for action_name, info in raw_hotkeys.items():
                processed[action_name] = {
                    "key_set": {self._parse_key(k) for k in info["keys"]},
                    "data": info.get("data")
                }
            return processed
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Błąd konfiguracji: {e}")
            return {}

    def load_settings(self):
        """Ładuje globalne ustawienia."""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f).get("settings", {})
        except:
            return {}