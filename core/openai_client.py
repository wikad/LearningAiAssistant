import os
from openai import OpenAI
from dotenv import load_dotenv
from ui.display import DisplayWindow
import pyperclip
import pyautogui
import time
import json

base_dir = os.path.dirname(os.path.dirname(__file__))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

window_manager = DisplayWindow()

def get_ai_explanation(text, context=None):
    """Pobiera odpowiedź od AI, uwzględniając opcjonalny kontekst rozmowy."""
    system_instruction = "Jesteś pomocnym asystentem."
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
            system_instruction = cfg.get("system_prompt", system_instruction)
    except: pass

    try:
        # Budujemy listę wiadomości dla modelu
        messages = [{"role": "system", "content": system_instruction}]
        
        # Jeśli przekazano poprzednią odpowiedź (kontekst), dodajemy ją
        if context:
            messages.append({"role": "assistant", "content": context})
            messages.append({"role": "user", "content": f"Dopytuję o to: {text}"})
        else:
            messages.append({"role": "user", "content": f"Wyjaśnij: {text}"})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Błąd API: {e}"

def do_explain(data):
    pyperclip.copy("")
    pyautogui.keyUp('alt')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    
    selected_text = pyperclip.paste()
    
    if not selected_text.strip():
        print("[!] Brak tekstu.")
        return

    # Wyświetlamy status ładowania
    window_manager.add_to_history(selected_text, "⌛ AI myśli...")
    
    actual_response = get_ai_explanation(selected_text)
    
    # Podmieniamy "⌛ AI myśli..." na faktyczną odpowiedź
    if window_manager.history:
        window_manager.history.pop()
    window_manager.add_to_history(selected_text, actual_response)

def do_close_ui(data):
    window_manager.close_window()

def do_exit(data):
    print("[SYSTEM] Zamykanie...")
    os._exit(0)

def handle_quick_question(question, context):
    """Funkcja pomocnicza wywoływana z poziomu okna display."""
    answer = get_ai_explanation(question, context=context)
    return answer