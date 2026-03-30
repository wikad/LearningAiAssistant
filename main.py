import pystray
from PIL import Image, ImageDraw
from threading import Thread
import os
from pystray import MenuItem as item
# TWOJE DOTYCHCZASOWE IMPORTY
from utils.config_manager import ConfigLoader
from core.hotkey import HotkeyHandler
import core.openai_client as actions
from ui.settings_window import SettingsWindow # Zakładam, że stworzyłeś ten plik

def manage_actions():
    action_map = {
        "explain_popup": actions.do_explain,
        "close_window": actions.do_close_ui,
        "exit_app": actions.do_exit,
    }
    return action_map

def show_settings(icon, item):
    """Ta funkcja wywołuje się po kliknięciu w Trayu"""
    print("[SYSTEM] Otwieranie okna ustawień...")
    settings = SettingsWindow()
    # Uruchamiamy w osobnym wątku, żeby nie 'zamrozić' ikonki w trayu
    Thread(target=settings.show, daemon=True).start()


# --- LOGIKA IKONY W PASKU ZADAŃ (TRAY) ---
ICON_FILENAME = "assets/icon.png"


def create_icon_image():
    """Wczytuje obraz ikony z pliku z dysku."""
    try:
        # Sprawdzamy pełną ścieżkę do pliku, żeby nie było problemów
        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, ICON_FILENAME)
        
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
            # Opcjonalnie: upewniamy się, że rozmiar jest OK (np. 64x64)
            # image = image.resize((64, 64), Image.Resampling.LANCZOS)
            return image
        else:
            print(f"[!] Nie znaleziono pliku ikony: {ICON_FILENAME}. Tworzę awaryjną.")
            # Awaryjna ikona (gdyby pliku nie było, żeby program nie crachował)
            return Image.new('RGB', (64, 64), color=(200, 50, 50)) 
    except Exception as e:
        print(f"[ERROR] Błąd ładowania ikony: {e}")
        return Image.new('RGB', (64, 64), color=(200, 50, 50))

def on_quit(icon, item):
    print("[SYSTEM] Zamykanie aplikacji...")
    icon.stop()
    os._exit(0)

def show_settings(icon, item):
    # Otwiera okno ustawień w nowym wątku, żeby nie zamrozić traya
    settings = SettingsWindow()
    Thread(target=settings.show, daemon=True).start()

def run_hotkeys():
    """Funkcja, która uruchamia Twój stary mechanizm w tle."""
    loader = ConfigLoader("config.json")
    hotkeys_data = loader.load_hotkeys()
    action_map = manage_actions()

    handler = HotkeyHandler(hotkeys_data, action_map)
    print("AutoExplain: Nasłuchiwanie skrótów aktywne.")
    handler.start() # To pętla blokująca, dlatego wywołujemy ją w wątku

def main():
    # 1. URUCHAMIAMY NASŁUCHIWANIE SKRÓTÓW W OSOBNYM WĄTKU
    hotkey_thread = Thread(target=run_hotkeys, daemon=True)
    hotkey_thread.start()

    # 2. DEFINIUJEMY MENU I IKONĘ TRAYA (Poprawiona składnia)
    menu_items = (
        item("Ustawienia", show_settings),
        item("Zamknij", on_quit)
    )

    icon = pystray.Icon(
        "AutoExplain", 
        create_icon_image(), 
        "AutoExplain", 
        pystray.Menu(*menu_items)
    )

    # 3. URUCHAMIAMY TRAYA
    print("Aplikacja działa w zasobniku systemowym.")
    icon.run()

if __name__ == "__main__":
    main()