import customtkinter as ctk
import subprocess
import json
import os
import threading
from tkinter import messagebox
import sys

# Ustawienia CustomTkinter
ctk.set_appearance_mode("dark")  # Domyślny tryb ciemny
ctk.set_default_color_theme("blue")  # Niebieski motyw kolorystyczny

# Słownik tłumaczeń
LANGUAGES = {
    "pl": {
        "title": "HeadsetControl GUI - Nowoczesny Panel Sterowania",
        "settings": "Ustawienia",
        "actions": "Akcje",
        "device": "Urządzenie (vendorid:productid):",
        "sidetone": "Poziom słyszalności:",
        "equalizer": "Equalizer (Preset 0-3):",
        "equalizer_preset": "Preset equalizera:",
        "lights": "Oświetlenie:",
        "voice_prompts": "Komunikaty głosowe:",
        "voice_prompt": "Komunikaty głosowe:",
        "mic_mute": "Wyciszenie mikrofonu:",
        "battery": "Bateria:",
        "language": "Język:",
        "theme": "Motyw:",
        "apply": "Zastosuj Ustawienia",
        "apply_settings": "Zastosuj ustawienia",
        "check_battery": "Sprawdź Baterię",
        "on": "Włączone",
        "off": "Wyłączone",
        "dark": "Ciemny",
        "light": "Jasny",
        "system": "Systemowy",
        "status": "Status:",
        "result": "Wynik:",
        "ready": "Gotowy",
        "error": "Błąd",
        "success": "Sukces",
        "connecting": "Łączenie...",
        "device_not_found": "Nie znaleziono urządzenia",
        "command_failed": "Komenda nie powiodła się",
        "battery_level": "Poziom baterii",
        "settings_applied": "Ustawienia zostały zastosowane",
        "about": "O programie",
        "version": "Wersja 2.0 - Nowoczesny interfejs 2025",
        "light_theme": "Jasny",
        "dark_theme": "Ciemny"
    },
    "en": {
        "title": "HeadsetControl GUI - Modern Control Panel",
        "settings": "Settings",
        "actions": "Actions",
        "device": "Device (vendorid:productid):",
        "sidetone": "Sidetone:",
        "equalizer": "Equalizer (Preset 0-3):",
        "equalizer_preset": "Equalizer preset:",
        "lights": "Lights:",
        "voice_prompts": "Voice Prompts:",
        "voice_prompt": "Voice prompt:",
        "mic_mute": "Mic mute:",
        "battery": "Battery:",
        "language": "Language:",
        "theme": "Theme:",
        "apply": "Apply Settings",
        "apply_settings": "Apply Settings",
        "check_battery": "Check Battery",
        "on": "On",
        "off": "Off",
        "dark": "Dark",
        "light": "Light",
        "system": "System",
        "status": "Status:",
        "result": "Result:",
        "ready": "Ready",
        "error": "Error",
        "success": "Success",
        "connecting": "Connecting...",
        "device_not_found": "Device not found",
        "command_failed": "Command failed",
        "battery_level": "Battery Level",
        "settings_applied": "Settings have been applied",
        "about": "About",
        "version": "Version 2.0 - Modern Interface 2025",
        "light_theme": "Light",
        "dark_theme": "Dark"
    }
}


class ModernHeadsetControlGUI:
    def __init__(self):
        self.current_language = "pl"
        self.config_file = "headsetcontrol_config.json"
        self.load_config()

        # Główne okno
        self.root = ctk.CTk()
        self.root.title(self.get_text("title"))
        self.root.geometry("900x800")
        self.root.minsize(900, 700)
        self.root.resizable(True, True)

        # Ikona okna (jeśli dostępna)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Zmienne dla kontrolek
        self.device_var = ctk.StringVar()
        self.sidetone_var = ctk.IntVar(value=64)
        self.equalizer_var = ctk.StringVar(value="0")
        self.lights_var = ctk.BooleanVar(value=True)
        self.voice_prompts_var = ctk.BooleanVar(value=True)
        self.mic_mute_var = ctk.BooleanVar(value=False)
        self.language_var = ctk.StringVar(value=self.current_language)
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())

        self.create_widgets()
        self.update_language()

    def get_text(self, key):
        return LANGUAGES[self.current_language].get(key, key)

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_language = config.get('language', 'pl')
                    theme = config.get('theme', 'dark')
                    ctk.set_appearance_mode(theme)
        except Exception as e:
            print(f"Błąd ładowania konfiguracji: {e}")

    def save_config(self):
        try:
            config = {
                'language': self.current_language,
                'theme': ctk.get_appearance_mode()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Błąd zapisywania konfiguracji: {e}")

    def create_widgets(self):
        # Główny kontener z przewijaniem
        self.main_scroll_frame = ctk.CTkScrollableFrame(self.root, corner_radius=0)
        self.main_scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Ulepszone bindowanie przewijania - bardziej stabilne
        self._setup_mousewheel_binding()

        # Prostsze bindowanie przewijania dla Linuxa
        self.main_scroll_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.main_scroll_frame.bind("<Leave>", self._unbind_from_mousewheel)

        # Używaj lokalnej zmiennej dla czytelności poniżej
        main_frame = self.main_scroll_frame

        # Nagłówek z tytułem
        header_frame = ctk.CTkFrame(main_frame, height=80, corner_radius=15)
        header_frame.pack(fill="x", padx=10, pady=(10, 20))
        header_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            header_frame,
            text=self.get_text("title"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=25)

        # Panel ustawień języka i motywu
        settings_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        settings_frame.pack(fill="x", padx=10, pady=(0, 20))

        settings_grid = ctk.CTkFrame(settings_frame)
        settings_grid.pack(fill="x", padx=20, pady=20)

        # Język
        self.language_label = ctk.CTkLabel(settings_grid, text=self.get_text("language"),
                                           font=ctk.CTkFont(size=14, weight="bold"))
        self.language_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

        self.language_combo = ctk.CTkComboBox(
            settings_grid,
            values=["pl", "en"],
            variable=self.language_var,
            command=self.change_language,
            width=120
        )
        self.language_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Motyw
        self.theme_label = ctk.CTkLabel(settings_grid, text=self.get_text("theme"),
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.theme_label.grid(row=0, column=2, padx=(20, 10), pady=10, sticky="w")

        self.theme_combo = ctk.CTkComboBox(
            settings_grid,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self.change_theme,
            width=120
        )
        self.theme_combo.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Główny panel kontroli
        control_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        control_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))

        # Sekcja urządzenia
        device_section = ctk.CTkFrame(control_frame, corner_radius=10)
        device_section.pack(fill="x", padx=20, pady=20)

        self.device_label = ctk.CTkLabel(device_section, text=self.get_text("device"),
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.device_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.device_entry = ctk.CTkEntry(
            device_section,
            textvariable=self.device_var,
            placeholder_text="1038:12ad (opcjonalne)",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.device_entry.pack(fill="x", padx=20, pady=(0, 20))

        # Sekcja kontroli audio
        audio_section = ctk.CTkFrame(control_frame, corner_radius=10)
        audio_section.pack(fill="x", padx=20, pady=(0, 20))

        audio_title = ctk.CTkLabel(audio_section, text="🎵 Kontrola Audio", font=ctk.CTkFont(size=16, weight="bold"))
        audio_title.pack(pady=(20, 10))

        # Sidetone z nowoczesnym sliderem
        sidetone_frame = ctk.CTkFrame(audio_section)
        sidetone_frame.pack(fill="x", padx=20, pady=10)

        self.sidetone_label = ctk.CTkLabel(sidetone_frame, text=self.get_text("sidetone"), font=ctk.CTkFont(size=14))
        self.sidetone_label.pack(anchor="w", padx=20, pady=(15, 5))

        slider_frame = ctk.CTkFrame(sidetone_frame)
        slider_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.sidetone_slider = ctk.CTkSlider(
            slider_frame,
            from_=0,
            to=128,
            variable=self.sidetone_var,
            command=self.update_sidetone_label,
            width=300
        )
        self.sidetone_slider.pack(side="left", padx=(20, 10), pady=10)

        self.sidetone_value_label = ctk.CTkLabel(slider_frame, text="64", font=ctk.CTkFont(size=14, weight="bold"))
        self.sidetone_value_label.pack(side="left", padx=10, pady=10)

        # Equalizer
        eq_frame = ctk.CTkFrame(audio_section)
        eq_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.equalizer_label = ctk.CTkLabel(eq_frame, text=self.get_text("equalizer_preset"), font=ctk.CTkFont(size=14))
        self.equalizer_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.equalizer_combo = ctk.CTkComboBox(
            eq_frame,
            values=["0", "1", "2", "3"],
            variable=self.equalizer_var,
            width=200
        )
        self.equalizer_combo.pack(anchor="w", padx=20, pady=(0, 15))

        # Sekcja przełączników
        switches_section = ctk.CTkFrame(control_frame, corner_radius=10)
        switches_section.pack(fill="x", padx=20, pady=(0, 20))

        switches_title = ctk.CTkLabel(switches_section, text="⚙️ Ustawienia Funkcji",
                                      font=ctk.CTkFont(size=16, weight="bold"))
        switches_title.pack(pady=(20, 15))

        switches_grid = ctk.CTkFrame(switches_section)
        switches_grid.pack(padx=20, pady=(0, 20))

        # Oświetlenie
        lights_frame = ctk.CTkFrame(switches_grid)
        lights_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.lights_label = ctk.CTkLabel(lights_frame, text="💡", font=ctk.CTkFont(size=20))
        self.lights_label.pack(side="left", padx=(15, 5), pady=15)

        self.lights_label_text = ctk.CTkLabel(lights_frame, text=self.get_text("lights"), font=ctk.CTkFont(size=14))
        self.lights_label_text.pack(side="left", padx=(5, 15), pady=15)

        self.lights_switch = ctk.CTkSwitch(lights_frame, variable=self.lights_var, text="")
        self.lights_switch.pack(side="right", padx=15, pady=15)

        # Komunikaty głosowe
        voice_frame = ctk.CTkFrame(switches_grid)
        voice_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.voice_label = ctk.CTkLabel(voice_frame, text="🔊", font=ctk.CTkFont(size=20))
        self.voice_label.pack(side="left", padx=(15, 5), pady=15)

        self.voice_prompts_label_text = ctk.CTkLabel(voice_frame, text=self.get_text("voice_prompts"),
                                                     font=ctk.CTkFont(size=14))
        self.voice_prompts_label_text.pack(side="left", padx=(5, 15), pady=15)

        self.voice_prompts_switch = ctk.CTkSwitch(voice_frame, variable=self.voice_prompts_var, text="")
        self.voice_prompts_switch.pack(side="right", padx=15, pady=15)

        # Wyciszenie mikrofonu
        mic_frame = ctk.CTkFrame(switches_grid)
        mic_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.mic_label = ctk.CTkLabel(mic_frame, text="🎤", font=ctk.CTkFont(size=20))
        self.mic_label.pack(side="left", padx=(15, 5), pady=15)

        self.mic_mute_label_text = ctk.CTkLabel(mic_frame, text=self.get_text("mic_mute"), font=ctk.CTkFont(size=14))
        self.mic_mute_label_text.pack(side="left", padx=(5, 15), pady=15)

        self.mic_mute_switch = ctk.CTkSwitch(mic_frame, variable=self.mic_mute_var, text="")
        self.mic_mute_switch.pack(side="right", padx=15, pady=15)

        # Konfiguracja grid weights
        switches_grid.columnconfigure(0, weight=1)
        switches_grid.columnconfigure(1, weight=1)

        # Panel przycisków
        buttons_frame = ctk.CTkFrame(control_frame, corner_radius=10)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        buttons_container = ctk.CTkFrame(buttons_frame)
        buttons_container.pack(pady=20)

        self.apply_button = ctk.CTkButton(
            buttons_container,
            text=self.get_text("apply"),
            command=self.apply_settings,
            height=45,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self.apply_button.pack(side="left", padx=10)

        self.battery_button = ctk.CTkButton(
            buttons_container,
            text=self.get_text("check_battery"),
            command=self.check_battery,
            height=45,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        self.battery_button.pack(side="left", padx=10)

        # Panel statusu

        status_frame = ctk.CTkFrame(main_frame, height=60, corner_radius=15)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))
        status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text=f"{self.get_text('status')} {self.get_text('ready')}",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=20)

        # Progress bar (ukryty domyślnie)
        self.progress_bar = ctk.CTkProgressBar(status_frame, width=400)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()

        # Widżet wyników
        output_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        output_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.output_label = ctk.CTkLabel(output_frame, text=self.get_text("result"), font=ctk.CTkFont(size=14, weight="bold"))
        self.output_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.output_text = ctk.CTkTextbox(output_frame, height=140, font=ctk.CTkFont(family="Consolas", size=10), wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _is_pointer_over_scrollframe(self, event) -> bool:
        try:
            x0 = self.main_scroll_frame.winfo_rootx()
            y0 = self.main_scroll_frame.winfo_rooty()
            w = self.main_scroll_frame.winfo_width()
            h = self.main_scroll_frame.winfo_height()
            return x0 <= event.x_root <= x0 + w and y0 <= event.y_root <= y0 + h
        except Exception:
            return False

    def _setup_mousewheel_binding(self):
        """Konfiguruje przewijanie kółkiem myszy w sposób bardziej stabilny"""
        try:
            # Bind bezpośrednio do scroll frame i jego dzieci
            def bind_recursive(widget):
                # Linux scroll events
                widget.bind("<Button-4>", self._on_mousewheel, "+")
                widget.bind("<Button-5>", self._on_mousewheel, "+")
                # Windows/Mac scroll events
                widget.bind("<MouseWheel>", self._on_mousewheel, "+")

                # Bind do wszystkich dzieci
                for child in widget.winfo_children():
                    bind_recursive(child)

            # Bind do głównego scroll frame
            bind_recursive(self.main_scroll_frame)

            # Dodatkowe bindowanie do root okna jako fallback
            self.root.bind("<Button-4>", self._on_mousewheel_global, "+")
            self.root.bind("<Button-5>", self._on_mousewheel_global, "+")
            self.root.bind("<MouseWheel>", self._on_mousewheel_global, "+")

        except Exception as e:
            print(f"Błąd konfiguracji przewijania: {e}")

    def _bind_to_mousewheel(self, event):
        """Przestarzałe - zastąpione przez _setup_mousewheel_binding"""
        pass

    def _unbind_from_mousewheel(self, event):
        """Przestarzałe - zastąpione przez _setup_mousewheel_binding"""
        pass

    def _on_mousewheel_global(self, event):
        """Handler przewijania dla całego okna - sprawdza czy kursor jest nad scroll area"""
        try:
            # Sprawdź czy kursor jest nad scroll frame
            x = self.root.winfo_pointerx() - self.main_scroll_frame.winfo_rootx()
            y = self.root.winfo_pointery() - self.main_scroll_frame.winfo_rooty()

            if (0 <= x <= self.main_scroll_frame.winfo_width() and
                0 <= y <= self.main_scroll_frame.winfo_height()):
                return self._on_mousewheel(event)
        except Exception:
            pass
        return None

    def _on_mousewheel(self, event):
        """Obsługuje przewijanie kółkiem myszy - ulepszona wersja"""
        try:
            # Sprawdź czy scroll frame ma canvas do przewijania
            canvas = None

            # Próbuj różne atrybuty canvas w CTkScrollableFrame
            for attr in ['_parent_canvas', '_canvas', 'canvas']:
                if hasattr(self.main_scroll_frame, attr):
                    canvas = getattr(self.main_scroll_frame, attr)
                    if canvas and hasattr(canvas, 'yview_scroll'):
                        break

            if not canvas:
                return "break"

            # Określ kierunek przewijania
            if hasattr(event, 'num'):
                # Linux: Button-4 (scroll up), Button-5 (scroll down)
                if event.num == 4:
                    delta = -1
                elif event.num == 5:
                    delta = 1
                else:
                    return "break"
            elif hasattr(event, 'delta'):
                # Windows/Mac: event.delta (positive = up, negative = down)
                delta = 1 if event.delta < 0 else -1
            else:
                return "break"

            # Przewiń canvas
            canvas.yview_scroll(delta, "units")
            return "break"

        except Exception as e:
            print(f"Błąd przewijania: {e}")
            return "break"

    def update_sidetone_label(self, value):
        self.sidetone_value_label.configure(text=str(int(float(value))))

    def change_language(self, value):
        self.current_language = value
        self.update_language()
        self.save_config()

    def change_theme(self, value):
        ctk.set_appearance_mode(value)
        self.save_config()

    def update_language(self):
        """Aktualizuje wszystkie teksty w interfejsie"""
        self.root.title(self.get_text("title"))
        self.title_label.configure(text=self.get_text("title"))
        self.language_label.configure(text=self.get_text("language"))
        self.theme_label.configure(text=self.get_text("theme"))
        self.device_label.configure(text=self.get_text("device"))
        self.sidetone_label.configure(text=self.get_text("sidetone"))
        self.equalizer_label.configure(text=self.get_text("equalizer_preset"))
        self.lights_label_text.configure(text=self.get_text("lights"))
        self.voice_prompts_label_text.configure(text=self.get_text("voice_prompts"))
        self.mic_mute_label_text.configure(text=self.get_text("mic_mute"))
        self.apply_button.configure(text=self.get_text("apply"))
        self.battery_button.configure(text=self.get_text("check_battery"))
        self.status_label.configure(text=f"{self.get_text('status')} {self.get_text('ready')}")
        if hasattr(self, 'output_label'):
            self.output_label.configure(text=self.get_text("result"))

    def show_progress(self, show=True):
        """Pokazuje/ukrywa pasek postępu"""
        if show:
            self.progress_bar.pack(pady=10)
            self.progress_bar.set(0)
        else:
            self.progress_bar.pack_forget()

    def update_status(self, message, is_error=False):
        """Aktualizuje status aplikacji"""
        color = "red" if is_error else ("gray10", "gray90")  # Używamy domyślnego koloru zamiast None
        self.status_label.configure(text=f"{self.get_text('status')} {message}", text_color=color)
        self.root.update()

    def display_output(self, text):
        try:
            self.output_text.insert("end", text + "\n")
            self.output_text.see("end")
        except Exception:
            pass

    def clear_output(self):
        """Czyści pole wyników"""
        try:
            self.output_text.delete("1.0", "end")
        except Exception:
            pass

    def run_headsetcontrol_command(self, command):
        """Uruchamia komendę headsetcontrol i loguje wynik do widżetu"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            cmd = " ".join(command)
            out = (result.stdout or "").strip()
            err = (result.stderr or "").strip()
            if out:
                self.display_output(f"$ {cmd}\n{out}")
            if err:
                self.display_output(f"[stderr] {err}")
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.display_output("Błąd: Timeout")
            return False, "", "Timeout"
        except Exception as e:
            self.display_output(f"Błąd: {e}")
            return False, "", str(e)

    def apply_settings(self):
        """Stosuje wszystkie ustawienia słuchawek"""
        # Wyczyść pole wyników przed nową operacją
        self.clear_output()

        self.update_status(self.get_text("connecting"))
        self.show_progress(True)

        def apply_thread():
            try:
                # Sprawdź czy headsetcontrol jest dostępny
                test_command = ["headsetcontrol", "--help"]
                test_result = subprocess.run(test_command, capture_output=True, text=True, timeout=5)
                if test_result.returncode != 0:
                    self.display_output("Błąd: headsetcontrol nie jest zainstalowany lub niedostępny w PATH")
                    self.update_status("Błąd: brak headsetcontrol", True)
                    return

                base_command = ["headsetcontrol"]
                device = self.device_var.get().strip()
                if device:
                    base_command.extend(["-d", device])

                # Zbierz wszystkie ustawienia w jedną komendę zamiast wielu osobnych
                all_args = base_command.copy()

                # Sidetone
                sidetone = self.sidetone_var.get()
                all_args.extend(["-s", str(sidetone)])

                # Equalizer preset
                eq = self.equalizer_var.get()
                all_args.extend(["-p", str(eq)])

                # Lights
                lights = "1" if self.lights_var.get() else "0"
                all_args.extend(["-l", lights])

                # Voice prompts
                voice = "1" if self.voice_prompts_var.get() else "0"
                all_args.extend(["-v", voice])

                # Microphone mute (używamy -r zgodnie ze starą wersją)
                mic_mute = "1" if self.mic_mute_var.get() else "0"
                all_args.extend(["-r", mic_mute])

                # Wykonaj jedną komendę ze wszystkimi ustawieniami
                self.display_output(f"Wykonuję: {' '.join(all_args)}")
                success, stdout, stderr = self.run_headsetcontrol_command(all_args)

                if success:
                    self.update_status(self.get_text("settings_applied"))
                    self.display_output("✓ Ustawienia zostały zastosowane pomyślnie")
                else:
                    error_msg = stderr.strip() if stderr else "Nieznany błąd"
                    self.update_status(f"Błąd: {error_msg}", True)
                    self.display_output(f"✗ Błąd: {error_msg}")

            except Exception as e:
                error_msg = str(e)
                self.update_status(f"Błąd: {error_msg}", True)
                self.display_output(f"✗ Wyjątek: {error_msg}")
            finally:
                self.show_progress(False)

        # Uruchom w osobnym wątku
        thread = threading.Thread(target=apply_thread)
        thread.daemon = True
        thread.start()

    def check_battery(self):
        """Sprawdza poziom baterii słuchawek"""
        # Wyczyść pole wyników przed nową operacją
        self.clear_output()

        self.update_status(self.get_text("connecting"))

        def battery_thread():
            try:
                base_command = ["headsetcontrol", "-b"]

                # Dodaj device ID jeśli podane
                device = self.device_var.get().strip()
                if device:
                    base_command.extend(["-d", device])

                success, stdout, stderr = self.run_headsetcontrol_command(base_command)

                if success and stdout.strip():
                    battery_info = stdout.strip()
                    self.update_status(f"{self.get_text('battery_level')}: {battery_info}")
                    self.display_output(f"{self.get_text('battery_level')}: {battery_info}")
                else:
                    error_msg = stderr if stderr else self.get_text("device_not_found")
                    self.update_status(f"{self.get_text('error')}: {error_msg}", True)
                    self.display_output(f"{self.get_text('error')}: {error_msg}")

            except Exception as e:
                self.update_status(f"{self.get_text('error')}: {str(e)}", True)
                self.display_output(f"{self.get_text('error')}: {str(e)}")

        # Uruchom w osobnym wątku
        thread = threading.Thread(target=battery_thread)
        thread.daemon = True
        thread.start()

    def run(self):
        """Uruchamia aplikację"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Obsługuje zamykanie aplikacji"""
        self.save_config()
        self.root.destroy()


if __name__ == "__main__":
    try:
        app = ModernHeadsetControlGUI()
        app.run()
    except Exception as e:
        print(f"Błąd uruchamiania aplikacji: {e}")
        sys.exit(1)