import os
from openai import OpenAI
from dotenv import load_dotenv # Importujemy ładowarkę .env
from ui.display import DisplayWindow
import pyperclip
import pyautogui
import time
import json
# 1. Ładujemy zmienne z pliku .env
# Jeśli plik jest w folderze wyżej, używamy ../.env
base_dir = os.path.dirname(os.path.dirname(__file__)) # folder główny projektu
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

# 2. Inicjalizujemy klienta (teraz automatycznie znajdzie klucz w systemie)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

window_manager = DisplayWindow()

def get_ai_explanation(text):
    # Wczytujemy prompt z configa za każdym razem (żeby zmiany działały bez restartu)
    system_instruction = "Jesteś pomocnym asystentem." # Fallback
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
            system_instruction = cfg.get("system_prompt", system_instruction)
    except: pass

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction}, # TU WSTAWIAMY PROMPT
                {"role": "user", "content": f"Wyjaśnij: {text}"}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Błąd API: {e}"

def do_explain(data):
    """Główna akcja wyzwalana skrótem klawiszowym."""
    # 1. Kopiowanie tekstu
    pyperclip.copy("") # Czyścimy schowek
    pyautogui.keyUp('alt')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    
    selected_text = pyperclip.paste()
    
    if not selected_text.strip():
        print("[!] Brak tekstu.")
        return

    # 2. Pobieranie odpowiedzi (Wywołanie API)
    # Wyświetlamy tymczasowy komunikat "Myślę...", żeby użytkownik wiedział, że coś się dzieje
    window_manager.add_to_history(selected_text, "⌛ AI myśli...")
    
    # Pobieramy prawdziwą odpowiedź
    actual_response = get_ai_explanation(selected_text)
    
    # 3. Aktualizacja okna prawdziwą odpowiedzią
    # Usuwamy "Myślę..." z historii i dodajemy prawdziwy tekst
    if window_manager.history:
        window_manager.history.pop() # Usuwamy komunikat ładowania
    window_manager.add_to_history(selected_text, actual_response)

def do_close_ui(data):
    window_manager.close_window()

def do_exit(data):
    print("[SYSTEM] Zamykanie...")
    os._exit(0)

# Funkcja dla Twojego nowego pola "Szybkie Pytanie" w display.py
def handle_quick_question(question, context):
    """Wywoływane bezpośrednio z UI po naciśnięciu Enter."""
    answer = get_ai_explanation(question, context=context)
    return answer