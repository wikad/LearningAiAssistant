import customtkinter as ctk
import pyautogui
from threading import Thread
from utils.history_manager import HistoryManager
import os
import json

class DisplayWindow:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        self.history_mgr = HistoryManager()
        full_history = self.history_mgr.load_all()
        self.history = [item["output"] for item in full_history]
        self.current_index = len(self.history) - 1
        self.root = None
        
        # Domyślne kolory (zostaną nadpisane przez load_theme)
        self.accent_color = "#1f538d"
        self.bg_color = "#2b2b2b"
        self.include_context = False
        
        self.load_theme()

    def load_theme(self):
        """Wczytuje kolory akcentu i tła z pliku config.json."""
        try:
            if os.path.exists("config.json"):
                with open("config.json", 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    # Czytamy oba klucze, które dodaliśmy w ustawieniach
                    self.accent_color = cfg.get("accent_color", "#1f538d")
                    self.bg_color = cfg.get("bg_color", "#2b2b2b")
        except Exception as e:
            print(f"Błąd wczytywania motywu: {e}")

    def close_window(self):
        try:
            if self.root:
                self.root.after(0, self.root.destroy)
                self.root = None
        except:
            pass

    def add_to_history(self, original, response):
        self.history_mgr.save_entry(original, response)
        self.history.append(response)
        self.current_index = len(self.history) - 1
        self.show_window()

    def show_window(self):
        window_exists = False
        try:
            if self.root and self.root.winfo_exists():
                window_exists = True
        except:
            window_exists = False

        if window_exists:
            self.root.after(0, self._update_ui)
            self.root.after(0, lambda: self.root.deiconify())
            self.root.after(0, lambda: self.root.attributes("-topmost", True))
        else:
            self.root = None
            thread = Thread(target=self._create_window, daemon=True)
            thread.start()

    def _update_ui(self):
        if not hasattr(self, 'text_area'): return
        
        self.text_area.configure(state="normal")
        self.text_area.delete("0.0", "end")
        if self.history:
            self.text_area.insert("0.0", self.history[self.current_index])
        self.text_area.configure(state="disabled")
        
        # Kolor przycisku wstecz
        if self.current_index > 0:
            self.btn_back.configure(state="normal", text_color="white")
        else:
            self.btn_back.configure(state="disabled", text_color="#444")

    def _go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self._update_ui()

    def _toggle_context(self):
        self.include_context = not self.include_context
        if self.include_context:
            self.btn_context.configure(fg_color=self.accent_color, text="🔗+")
        else:
            self.btn_context.configure(fg_color="#333", text="🔗")

    def _on_quick_question(self, event=None):
        question = self.entry_question.get()
        if not question.strip(): return
        
        last_answer = self.history[self.current_index] if (self.include_context and self.history) else None
        self.entry_question.delete(0, 'end')

        self.add_to_history("Pytanie...", "⌛ AI generuje odpowiedź...")
        
        from core.openai_client import handle_quick_question
        answer = handle_quick_question(question, last_answer)
        
        if self.history: self.history.pop()
        self.add_to_history(question, answer)

    def _create_window(self):
        self.load_theme() # Odśwież kolory przed narysowaniem
        
        self.root = ctk.CTk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        # Ustawiamy tło głównego okna na kolor tła (bg_color)
        self.root.configure(fg_color=self.bg_color)

        # Logika przesuwania
        def start_move(event):
            self.root._offsetx, self.root._offsety = event.x, event.y
        def do_move(event):
            x = self.root.winfo_x() + event.x - self.root._offsetx
            y = self.root.winfo_y() + event.y - self.root._offsety
            self.root.geometry(f"+{x}+{y}")

        # Pozycjonowanie
        mouse_x, mouse_y = pyautogui.position()
        w, h = 400, 320
        target_x = mouse_x + 20
        target_y = mouse_y - h - 10
        if target_y < 0: target_y = mouse_y + 20
        
        screen_w = self.root.winfo_screenwidth()
        if target_x + w > screen_w: target_x = screen_w - w - 10
        self.root.geometry(f"{w}x{h}+{target_x}+{target_y}")

        # --- GŁÓWNY FRAME (RAMKA) ---
        main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=15, 
            border_width=2, 
            border_color=self.accent_color, # Kolor obramowania
            fg_color=self.bg_color           # Kolor wypełnienia (tło)
        )
        main_frame.pack(expand=True, fill='both', padx=2, pady=2)

        # --- PASEK GÓRNY (NAWIGACJA) ---
        nav_bar = ctk.CTkFrame(
            main_frame, 
            fg_color=self.accent_color,     # Pasek ma kolor akcentu
            height=35,
            corner_radius=10
        )
        nav_bar.pack(fill='x', padx=5, pady=5)
        nav_bar.bind("<ButtonPress-1>", start_move)
        nav_bar.bind("<B1-Motion>", do_move)

        title_label = ctk.CTkLabel(nav_bar, text="AUTO EXPLAIN", font=("Segoe UI", 10, "bold"), text_color="white")
        title_label.pack(side='left', expand=True)
        title_label.bind("<ButtonPress-1>", start_move)
        title_label.bind("<B1-Motion>", do_move)

        self.btn_back = ctk.CTkButton(nav_bar, text="←", width=30, height=25, fg_color="transparent", command=self._go_back)
        self.btn_back.pack(side='left', padx=5)

        btn_close = ctk.CTkButton(nav_bar, text="✕", width=30, height=25, fg_color="transparent", hover_color="#c42b1c", command=self.close_window)
        btn_close.pack(side='right', padx=5)

        # --- POLE TEKSTOWE ---
        self.text_area = ctk.CTkTextbox(
            main_frame, 
            fg_color=self.bg_color,         # Tło tekstu takie samo jak bg_color
            font=("Segoe UI", 13), 
            wrap="word",
            text_color="white"
        )
        self.text_area.pack(expand=True, fill='both', padx=10, pady=5)

        # --- KONTENER NA PYTANIE ---
        question_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        question_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.btn_context = ctk.CTkButton(question_frame, text="🔗", width=35, height=35,
                                         fg_color="#333", hover_color="#444",
                                         command=self._toggle_context, corner_radius=10)
        self.btn_context.pack(side='left', padx=(0, 5))

        self.entry_question = ctk.CTkEntry(
            question_frame, 
            placeholder_text="Zadaj pytanie...", 
            height=35, 
            corner_radius=10,
            fg_color=self.bg_color,         # Tło wpisywania
            border_color=self.accent_color  # Ramka wpisywania
        )
        self.entry_question.pack(side='left', expand=True, fill='x')
        self.entry_question.bind("<Return>", self._on_quick_question)

        self._update_ui()
        self.root.mainloop()