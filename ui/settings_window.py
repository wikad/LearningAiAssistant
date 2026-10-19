import customtkinter as ctk
import json
import os
from tkinter import colorchooser

from utils.paths import CONFIG_PATH

class SettingsWindow:
    def __init__(self):
        self.config_path = CONFIG_PATH
        self.DEFAULT_ACCENT = "#1f538d"
        self.DEFAULT_BG = "#2b2b2b"
        self.DEFAULT_PROMPT = "Jesteś pomocnym asystentem. Wyjaśniaj pojęcia krótko, konkretnie i prostym językiem, po polsku."
        
        self.accent_color = self.DEFAULT_ACCENT
        self.bg_color = self.DEFAULT_BG

    def load_current_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return {}

    def pick_color(self, initial, button_ref, attr_name):
        color = colorchooser.askcolor(initialcolor=initial)[1]
        if color:
            setattr(self, attr_name, color)
            button_ref.configure(fg_color=color, text=f"Kolor: {color}")

    def show(self):
        root = ctk.CTk()
        root.title("AutoExplain - Ustawienia")
        root.geometry("500x850")

        current_cfg = self.load_current_config()
        self.accent_color = current_cfg.get("accent_color", self.DEFAULT_ACCENT)
        self.bg_color = current_cfg.get("bg_color", self.DEFAULT_BG)
        system_prompt = current_cfg.get("system_prompt", self.DEFAULT_PROMPT)
        hotkeys = current_cfg.get("hotkeys", {})

        ctk.CTkLabel(root, text="🎨 PERSONALIZACJA", font=("Segoe UI", 20, "bold")).pack(pady=20)
        color_frame = ctk.CTkFrame(root)
        color_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(color_frame, text="Kolor Akcentu (Ramka/Pasek):").pack(pady=5)
        btn_acc = ctk.CTkButton(color_frame, text=self.accent_color, fg_color=self.accent_color,
                                command=lambda: self.pick_color(self.accent_color, btn_acc, "accent_color"))
        btn_acc.pack(pady=5)

        ctk.CTkLabel(color_frame, text="Kolor Tła (Panel tekstu):").pack(pady=5)
        btn_bg = ctk.CTkButton(color_frame, text=self.bg_color, fg_color=self.bg_color,
                               command=lambda: self.pick_color(self.bg_color, btn_bg, "bg_color"))
        btn_bg.pack(pady=5)

        ctk.CTkLabel(root, text="⌨️ SKRÓTY KLAWISZOWE", font=("Segoe UI", 14, "bold")).pack(pady=(20, 10))

        def create_hk_input(label, default_keys):
            ctk.CTkLabel(root, text=label).pack()
            entry = ctk.CTkEntry(root, width=250, justify="center")
            entry.insert(0, "+".join(default_keys))
            entry.pack(pady=5)
            return entry

        hk_explain = create_hk_input("Wyjaśnianie (AI):", hotkeys.get("explain_popup", {}).get("keys", ["alt_l", "q"]))
        hk_close = create_hk_input("Zamykanie okna:", hotkeys.get("close_window", {}).get("keys", ["alt_l", "a"]))
        hk_exit = create_hk_input("Wyjście z aplikacji:", hotkeys.get("exit_app", {}).get("keys", ["alt_l", "p"]))

        ctk.CTkLabel(root, text="🤖 INSTRUKCJA DLA AI (PROMPT)", font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))
        self.prompt_box = ctk.CTkTextbox(root, width=400, height=100)
        self.prompt_box.insert("0.0", system_prompt)
        self.prompt_box.pack(pady=5)
        def restore_defaults():
            self.accent_color = self.DEFAULT_ACCENT
            self.bg_color = self.DEFAULT_BG
            btn_acc.configure(fg_color=self.accent_color, text=f"Kolor: {self.accent_color}")
            btn_bg.configure(fg_color=self.bg_color, text=f"Kolor: {self.bg_color}")
            # Reset Promptu
            self.prompt_box.delete("0.0", "end")
            self.prompt_box.insert("0.0", self.DEFAULT_PROMPT)
            hk_explain.delete(0, 'end')
            hk_explain.insert(0, "alt_l+q")
            hk_close.delete(0, 'end')
            hk_close.insert(0, "alt_l+a")
            hk_exit.delete(0, 'end')
            hk_exit.insert(0, "alt_l+p")
            
            print("[SETTINGS] Przywrócono wartości domyślne do widoku.")
        btn_restore = ctk.CTkButton(root, text="Przywróć domyślne", fg_color="transparent", 
                                    border_width=1, border_color="#555", text_color="#aaa",
                                    hover_color="#333", command=restore_defaults)
        btn_restore.pack(pady=(20, 0))

        def save_all():
            new_config = {
                "accent_color": self.accent_color,
                "bg_color": self.bg_color,
                "system_prompt": self.prompt_box.get("0.0", "end").strip(),
                "hotkeys": {
                    "explain_popup": {"keys": hk_explain.get().lower().split("+"), "data": "popup"},
                    "close_window": {"keys": hk_close.get().lower().split("+"), "data": None},
                    "exit_app": {"keys": hk_exit.get().lower().split("+"), "data": None}
                }
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            root.destroy()

        ctk.CTkButton(root, text="ZAPISZ I ZASTOSUJ", fg_color="#28a745", hover_color="#218838", 
                      height=45, font=("Segoe UI", 12, "bold"), command=save_all).pack(pady=30)
        
        root.mainloop()