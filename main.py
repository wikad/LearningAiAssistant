import pystray
from PIL import Image, ImageDraw
from threading import Thread
import os
from pystray import MenuItem as item
from utils.config_manager import ConfigLoader
from utils.paths import CONFIG_PATH
from core.hotkey import HotkeyHandler
import core.openai_client as actions
from ui.settings_window import SettingsWindow

def manage_actions():
    action_map = {
        "explain_popup": actions.do_explain,
        "close_window": actions.do_close_ui,
        "exit_app": actions.do_exit,
    }
    return action_map

ICON_FILENAME = "assets/icon.png"


def create_icon_image():
    try:
        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, ICON_FILENAME)
        
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
            return image
        else:
            print(f"[!] Nie znaleziono pliku ikony: {ICON_FILENAME}. Tworzę awaryjną.")
            return Image.new('RGB', (64, 64), color=(200, 50, 50)) 
    except Exception as e:
        print(f"[ERROR] Błąd ładowania ikony: {e}")
        return Image.new('RGB', (64, 64), color=(200, 50, 50))

def on_quit(icon, item):
    print("[SYSTEM] Zamykanie aplikacji...")
    icon.stop()
    os._exit(0)

def show_settings(icon, item):
    print("[SYSTEM] Otwieranie okna ustawień...")
    settings = SettingsWindow()
    Thread(target=settings.show, daemon=True).start()

def run_hotkeys():
    loader = ConfigLoader(CONFIG_PATH)
    hotkeys_data = loader.load_hotkeys()
    action_map = manage_actions()

    handler = HotkeyHandler(hotkeys_data, action_map)
    print("AutoExplain: Nasłuchiwanie skrótów aktywne.")
    handler.start()

def main():
    hotkey_thread = Thread(target=run_hotkeys, daemon=True)
    hotkey_thread.start()

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

    print("Aplikacja działa w zasobniku systemowym.")
    icon.run()

if __name__ == "__main__":
    main()