# AutoExplain 🤖

**Aplikacja do szybkiego wyjaśniania tekstu za pomocą AI**

AutoExplain to lekka aplikacja Python działająca w pasku zadań systemowym (tray), która umożliwia szybkie wyjaśnianie dowolnego tekstu poprzez globalne skróty klawiszowe. Aplikacja wykorzystuje API OpenAI do generowania przystępnych, zwięzłych wyjaśnień w języku polskim.

---

## 🎯 Główne Cechy

- **Globalne Skróty Klawiszowe**: Dostęp do funkcji z dowolnego miejsca w systemie
  - `Alt + Q` → Wyjaśnij zaznaczony tekst (popup)
  - `Alt + A` → Zamknij menu wyjaśnień
  - `Alt + P` → Zamknij aplikację

- **Integracja z OpenAI**: Używa modelu `gpt-4o-mini` dla szybkich i tanich wyjaśnień

- **System Tray**: Działa w tle jako ikona w pasku zadań

- **GUI z CustomTkinter**: Nowoczesny interfejs do wyświetlania wyjaśnień i ustawień

- **Schowek**: Automatycznie pobiera zaznaczony tekst z schowka systemowego

- **Historia**: Przechowuje historię wyjaśnień

---

## 📋 Struktura Projektu

```
AutoExplain/
├── main.py                    # Punkt wejścia aplikacji
├── config.json                # Konfiguracja skrótów i ustawień
├── requirements.txt           # Zależności Python
├── config.json               # Konfiguracja aplikacji
├── history.json              # Historia wyjaśnień
│
├── core/                      # Część logiki biznesowej
│   ├── hotkey.py             # Obsługa globalnych skrótów klawiszowych
│   └── openai_client.py      # Integracja z OpenAI API
│
├── ui/                        # Interfejs użytkownika
│   ├── display.py            # Okno wyswietlania wyjaśnień
│   ├── overlay.py            # Nakładka ekranu
│   └── settings_window.py    # Okno ustawień
│
├── utils/                     # Narzędziowe funkcje
│   ├── config_manager.py     # Zarządzanie konfiguracją
│   └── history_manager.py    # Zarządzanie historią
│
├── assets/                    # Zasoby (ikony, obrazki)
└── env/                       # Wirtualne środowisko Python
```

---

## 🚀 Instalacja i Uruchomienie

### Wymagania
- Python 3.9+
- Klucz API z OpenAI

### Kroki

1. **Klonuj/Pobierz projekt**
   ```bash
   cd AutoExplain
   ```

2. **Utwórz wirtualne środowisko** (opcjonalnie)
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   ```

3. **Zainstaluj zależności**
   ```bash
   pip install -r requirements.txt
   ```

4. **Utwórz plik `.env`** w głównym folderze z kluczem API
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Uruchom aplikację**
   ```bash
   python main.py
   ```

---

## ⚙️ Konfiguracja

### Skróty Klawiszowe (`config.json`)
```json
{
    "hotkeys": {
        "explain_popup": {
            "keys": ["alt_l", "q"],
            "data": "popup"
        },
        "close_window": {
            "keys": ["alt_l", "a"],
            "data": null
        },
        "exit_app": {
            "keys": ["alt_l", "p"],
            "data": null
        }
    }
}
```

---

## 🛠️ Technologia i Zależności

| Biblioteka | Zastosowanie |
|-----------|------------|
| **openai** | Komunikacja z OpenAI API |
| **pynput** | Globalne skróty klawiszowe |
| **pyperclip** | Odczyt/zapis schowka systemowego |
| **pystray** | Ikona w pasku zadań (tray) |
| **Pillow** | Obsługa obrazów (wymagane przez pystray) |
| **customtkinter** | Nowoczesny interfejs GUI |

---

## 📖 Jak Działa

1. **Zaznacz tekst** na ekranie i wciśnij `Alt + Q`
2. **Aplikacja kopiuje** zaznaczony tekst do schowka
3. **OpenAI API** generuje wyjaśnienie
4. **Popup** wyświetla wyjaśnienie w czytelnym formacie
5. Możesz **zadać dodatkowe pytania** o kontekst wyjaśnienia

---

## 🔐 Bezpieczeństwo

- Klucz API przechowywany w pliku `.env` (nie w repozytorium)
- `.env` powinien być w `.gitignore`
- Historia zapisywana lokalnie

---

## 📝 Plany Rozwoju

- [ ] Obsługa wielu modeli AI
- [ ] Własne ustawienia skrótów klawiszowych w GUI
- [ ] Eksport historii do PDF/Excel
- [ ] Wsparcie dla wielu języków
- [ ] Cache wyjaśnień dla powtarzalnych pytań

---

## 💡 Wskazówki

- **Wydajność**: Model `gpt-4o-mini` jest szybki i tani
- **Format Markdown**: Wyjaśnienia mogą zawierać **pogrubienie** i `kod`
- **Kontekst**: Aplikacja pamięta poprzednią odpowiedź do follow-up pytań

---

## 📄 Licencja

Projekt prywatny.

---

## 👨‍💻 Autor

AutoExplain - Aplikacja AI do wyjaśniania tekstu
