from pynput import keyboard
import threading

class HotkeyHandler:
    def __init__(self, hotkeys_dict, action_map):
        self.hotkeys = hotkeys_dict
        self.action_map = action_map
        self.current_keys = set()
        self.last_triggered = None 

    def on_press(self, key):
        self.current_keys.add(key)
        
        for name, config in self.hotkeys.items():
            if all(k in self.current_keys for k in config["key_set"]):
                if self.last_triggered != name:
                    self.last_triggered = name
                    func = self.action_map.get(name)
                    
                    if func:
                        # --- KLUCZOWA ZMIANA ---
                        # Tworzymy nowy wątek dla funkcji, aby nie blokować listenera
                        action_thread = threading.Thread(
                            target=func, 
                            args=(config.get("data"),),
                            daemon=True # Wątek zamknie się razem z aplikacją
                        )
                        action_thread.start()
                    
                    # Czyścimy klawisze, by uniknąć natychmiastowego powtórzenia
                    self.current_keys.clear()

    def on_release(self, key):
        try:
            self.current_keys.remove(key)
        except KeyError:
            pass
        
        if not self.current_keys:
            self.last_triggered = None

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()