import customtkinter as ctk
import subprocess
import json
import os
import threading
import shlex
import sys
import tkinter as tk

if sys.platform.startswith("linux"):
    os.environ.setdefault("TK_APPNAME", "headsetcontrol-gui")

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
        "dark_theme": "Ciemny",
        "device_profile": "Profil słuchawek:",
        "custom_profile": "Własne",
        "feature_section_title": "Dostępne funkcje",
        "include_setting": "Aktywuj zmianę",
        "no_change": "Bez zmian",
        "notification_sound": "Dźwięk powiadomień:",
        "notification_sound_hint": "ID dźwięku (np. 0-9)",
        "inactive_time": "Czas bezczynności (minuty):",
        "inactive_time_hint": "0 wyłącza automatyczne usypianie",
        "chatmix": "ChatMix:",
        "chatmix_hint": "0 = więcej gry, 128 = więcej czatu",
        "rotate_to_mute": "Obrót = wycisz:",
        "parametric_equalizer": "Equalizer parametryczny:",
        "parametric_equalizer_hint": "Format: 300,3.5,1.5,peaking;...",
        "microphone_mute_led_brightness": "Jasność LED wyciszenia mikrofonu:",
        "microphone_volume": "Głośność mikrofonu:",
        "volume_limiter": "Limiter głośności:",
        "bluetooth_when_powered_on": "Bluetooth po włączeniu:",
        "bluetooth_call_volume": "Głośność połączeń Bluetooth:",
        "bluetooth_call_volume_hint": "0 = brak, 1 = średnia, 2 = wysoka",
        "equalizer_curve": "Krzywa equalizera:",
        "battery_not_supported": "Pomiar baterii nieobsługiwany przez ten profil",
        "no_changes_selected": "Brak wybranych zmian do zastosowania",
        "invalid_value": "Nieprawidłowa wartość dla {feature}: {detail}",
    "value_required": "Wprowadź wartość dla {feature}",
    "headsetcontrol_missing": "headsetcontrol nie jest zainstalowany lub dostępny w PATH",
    "executing_command": "Wykonuję"
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
        "dark_theme": "Dark",
        "device_profile": "Headset profile:",
        "custom_profile": "Custom",
        "feature_section_title": "Available features",
        "include_setting": "Enable change",
        "no_change": "No change",
        "notification_sound": "Notification sound:",
        "notification_sound_hint": "Sound ID (e.g. 0-9)",
        "inactive_time": "Inactive time (minutes):",
        "inactive_time_hint": "0 disables auto sleep",
        "chatmix": "ChatMix:",
        "chatmix_hint": "0 = more game, 128 = more chat",
        "rotate_to_mute": "Rotate to mute:",
        "parametric_equalizer": "Parametric equalizer:",
        "parametric_equalizer_hint": "Format: 300,3.5,1.5,peaking;...",
        "microphone_mute_led_brightness": "Mic mute LED brightness:",
        "microphone_volume": "Microphone volume:",
        "volume_limiter": "Volume limiter:",
        "bluetooth_when_powered_on": "Bluetooth when powered on:",
        "bluetooth_call_volume": "Bluetooth call volume:",
        "bluetooth_call_volume_hint": "0 = none, 1 = medium, 2 = high",
        "equalizer_curve": "Equalizer curve:",
        "battery_not_supported": "Battery readings are not supported for this profile",
        "no_changes_selected": "No changes selected to apply",
        "invalid_value": "Invalid value for {feature}: {detail}",
    "value_required": "Enter a value for {feature}",
    "headsetcontrol_missing": "headsetcontrol is not installed or available in PATH",
    "executing_command": "Executing"
    }
}

FEATURE_ORDER = [
    "sidetone",
    "notification_sound",
    "lights",
    "inactive_time",
    "chatmix",
    "voice_prompts",
    "rotate_to_mute",
    "equalizer_preset",
    "equalizer",
    "parametric_equalizer",
    "microphone_mute_led_brightness",
    "microphone_volume",
    "volume_limiter",
    "bluetooth_when_powered_on",
    "bluetooth_call_volume"
]

FEATURE_DEFINITIONS = {
    "sidetone": {
        "label_key": "sidetone",
        "type": "slider",
        "flag": "-s",
        "min": 0,
        "max": 128,
        "step": 1
    },
    "notification_sound": {
        "label_key": "notification_sound",
        "type": "int",
        "flag": "-n",
        "min": 0,
        "max": 99,
        "hint_key": "notification_sound_hint"
    },
    "lights": {
        "label_key": "lights",
        "type": "toggle",
        "flag": "-l"
    },
    "inactive_time": {
        "label_key": "inactive_time",
        "type": "slider",
        "flag": "-i",
        "min": 0,
        "max": 90,
        "step": 1,
        "hint_key": "inactive_time_hint"
    },
    "chatmix": {
        "label_key": "chatmix",
        "type": "slider",
        "flag": "-m",
        "min": 0,
        "max": 128,
        "step": 1,
        "hint_key": "chatmix_hint"
    },
    "voice_prompts": {
        "label_key": "voice_prompts",
        "type": "toggle",
        "flag": "-v"
    },
    "rotate_to_mute": {
        "label_key": "rotate_to_mute",
        "type": "toggle",
        "flag": "-r"
    },
    "equalizer_preset": {
        "label_key": "equalizer_preset",
        "type": "choice",
        "flag": "-p",
        "values": ["0", "1", "2", "3"]
    },
    "equalizer": {
        "label_key": "equalizer_curve",
        "type": "text",
        "flag": "-e",
        "multiline": False
    },
    "parametric_equalizer": {
        "label_key": "parametric_equalizer",
        "type": "text",
        "flag": "--parametric-equalizer",
        "multiline": True,
        "allow_newlines": True,
        "hint_key": "parametric_equalizer_hint"
    },
    "microphone_mute_led_brightness": {
        "label_key": "microphone_mute_led_brightness",
        "type": "slider",
        "flag": "--microphone-mute-led-brightness",
        "min": 0,
        "max": 3,
        "step": 1
    },
    "microphone_volume": {
        "label_key": "microphone_volume",
        "type": "slider",
        "flag": "--microphone-volume",
        "min": 0,
        "max": 128,
        "step": 1
    },
    "volume_limiter": {
        "label_key": "volume_limiter",
        "type": "toggle",
        "flag": "--volume-limiter"
    },
    "bluetooth_when_powered_on": {
        "label_key": "bluetooth_when_powered_on",
        "type": "toggle",
        "flag": "--bt-when-powered-on"
    },
    "bluetooth_call_volume": {
        "label_key": "bluetooth_call_volume",
        "type": "slider",
        "flag": "--bt-call-volume",
        "min": 0,
        "max": 2,
        "step": 1,
        "hint_key": "bluetooth_call_volume_hint"
    }
}

DEVICE_CAPABILITIES = {
    "Audeze Maxwell": [
        "sidetone",
        "battery",
        "inactive_time",
        "chatmix",
        "voice_prompts",
        "equalizer_preset",
        "volume_limiter"
    ],
    "Corsair Headset Device": [
        "sidetone",
        "battery",
        "notification_sound",
        "lights"
    ],
    "HyperX Cloud Alpha Wireless": [
        "sidetone",
        "battery",
        "inactive_time",
        "voice_prompts"
    ],
    "HyperX Cloud Flight Wireless": [
        "battery"
    ],
    "HyperX Cloud 3": [
        "sidetone"
    ],
    "Logitech G430": [
        "sidetone"
    ],
    "Logitech G432/G433": [
        "sidetone"
    ],
    "Logitech G533": [
        "sidetone",
        "battery",
        "inactive_time"
    ],
    "Logitech G535": [
        "sidetone",
        "battery",
        "inactive_time"
    ],
    "Logitech G930": [
        "sidetone",
        "battery"
    ],
    "Logitech G633/G635/G733/G933/G935": [
        "sidetone",
        "battery",
        "lights"
    ],
    "Logitech G PRO Series": [
        "sidetone",
        "battery",
        "inactive_time"
    ],
    "Logitech G PRO X 2": [
        "sidetone",
        "inactive_time"
    ],
    "Logitech Zone Wired/Zone 750": [
        "sidetone",
        "voice_prompts",
        "rotate_to_mute"
    ],
    "SteelSeries Arctis (1/7X/7P) Wireless": [
        "sidetone",
        "battery",
        "inactive_time"
    ],
    "SteelSeries Arctis (7/Pro)": [
        "sidetone",
        "battery",
        "lights",
        "inactive_time",
        "chatmix"
    ],
    "SteelSeries Arctis 9": [
        "sidetone",
        "battery",
        "inactive_time",
        "chatmix"
    ],
    "SteelSeries Arctis Pro Wireless": [
        "sidetone",
        "battery",
        "inactive_time"
    ],
    "ROCCAT Elo 7.1 Air": [
        "lights",
        "inactive_time"
    ],
    "ROCCAT Elo 7.1 USB": [
        "lights"
    ],
    "SteelSeries Arctis Nova 3": [
        "sidetone",
        "equalizer_preset",
        "equalizer",
        "microphone_mute_led_brightness",
        "microphone_volume"
    ],
    "SteelSeries Arctis Nova (5/5X)": [
        "sidetone",
        "battery",
        "inactive_time",
        "chatmix",
        "equalizer_preset",
        "equalizer",
        "parametric_equalizer",
        "microphone_mute_led_brightness",
        "microphone_volume",
        "volume_limiter"
    ],
    "SteelSeries Arctis Nova 7": [
        "sidetone",
        "battery",
        "inactive_time",
        "chatmix",
        "equalizer_preset",
        "equalizer",
        "microphone_mute_led_brightness",
        "microphone_volume",
        "volume_limiter",
        "bluetooth_when_powered_on",
        "bluetooth_call_volume"
    ],
    "SteelSeries Arctis 7+": [
        "sidetone",
        "battery",
        "inactive_time",
        "chatmix",
        "equalizer_preset",
        "equalizer"
    ],
    "SteelSeries Arctis Nova Pro Wireless": [
        "sidetone",
        "battery",
        "lights",
        "inactive_time",
        "equalizer_preset",
        "equalizer"
    ],
    "HeadsetControl Test device": [
        "sidetone",
        "battery",
        "notification_sound",
        "lights",
        "inactive_time",
        "chatmix",
        "voice_prompts",
        "rotate_to_mute",
        "equalizer_preset",
        "equalizer",
        "microphone_mute_led_brightness",
        "microphone_volume",
        "volume_limiter",
        "bluetooth_when_powered_on",
        "bluetooth_call_volume"
    ]
}


class ModernHeadsetControlGUI:
    def __init__(self):
        self.current_language = "pl"
        self._initialize_config_path()
        self.saved_feature_states = {}
        self._loading_feature_states = False
        self.load_config()

        # Główne okno
        self.root = ctk.CTk()
        try:
            # Ustaw klasę okna aby środowisko graficzne dopasowało ikonę z pliku .desktop
            self.root.wm_class("headsetcontrol-gui")
        except Exception:
            pass
        self.root.title(self.get_text("title"))
        self.root.geometry("900x800")
        self.root.minsize(900, 700)
        self.root.resizable(True, True)

        # Ikona okna (jeśli dostępna)
        self._icon_image = None
        self._set_window_icon()

        loaded_profile = getattr(self, "_loaded_profile_key", None)
        if loaded_profile not in DEVICE_CAPABILITIES:
            loaded_profile = None

        # Zmienne dla kontrolek
        self.device_var = ctk.StringVar()
        self.language_var = ctk.StringVar(value=self.current_language)
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        self.device_profile_var = ctk.StringVar()
        self.feature_states = {}
        self.profile_display_map = {}
        self.selected_profile_key = loaded_profile
        self.active_features = []
        self.battery_supported = True

        self.create_widgets()
        self.update_language()

    def get_text(self, key):
        return LANGUAGES[self.current_language].get(key, key)

    def load_config(self):
        try:
            self._loaded_profile_key = None
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_language = config.get('language', 'pl')
                    theme = config.get('theme', 'dark')
                    ctk.set_appearance_mode(theme)
                    self._loaded_profile_key = config.get('device_profile')
                    stored_states = config.get('feature_states', {})
                    if isinstance(stored_states, dict):
                        self.saved_feature_states = stored_states
            else:
                legacy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headsetcontrol_config.json")
                if os.path.exists(legacy_path):
                    with open(legacy_path, 'r') as f:
                        config = json.load(f)
                        self.current_language = config.get('language', 'pl')
                        theme = config.get('theme', 'dark')
                        ctk.set_appearance_mode(theme)
                        self._loaded_profile_key = config.get('device_profile')
                        stored_states = config.get('feature_states', {})
                        if isinstance(stored_states, dict):
                            self.saved_feature_states = stored_states
                    # przenieś konfigurację do nowej lokalizacji
                    try:
                        self.save_config()
                    except Exception:
                        pass
        except Exception as e:
            print(f"Błąd ładowania konfiguracji: {e}")

    def _initialize_config_path(self):
        if sys.platform.startswith("win"):
            base_dir = os.environ.get("APPDATA")
            if not base_dir:
                base_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
            config_dir = os.path.join(base_dir, "HeadsetControlGUI")
        else:
            xdg_dir = os.environ.get("XDG_CONFIG_HOME")
            if xdg_dir:
                config_dir = os.path.join(xdg_dir, "headsetcontrol-gui")
            else:
                config_dir = os.path.join(os.path.expanduser("~"), ".config", "headsetcontrol-gui")

        try:
            os.makedirs(config_dir, exist_ok=True)
        except Exception:
            fallback = os.path.join(os.path.expanduser("~"), ".headsetcontrol-gui")
            os.makedirs(fallback, exist_ok=True)
            config_dir = fallback

        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "headsetcontrol_config.json")

    def save_config(self):
        try:
            config = {
                'language': self.current_language,
                'theme': ctk.get_appearance_mode(),
                'device_profile': getattr(self, 'selected_profile_key', None),
                'feature_states': getattr(self, 'saved_feature_states', {})
            }
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Błąd zapisywania konfiguracji: {e}")

    def _set_window_icon(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ico_path = os.path.join(base_dir, "headsetcontrolGUI.ico")
        png_path = os.path.join(base_dir, "headsetcontrolGUI.png")

        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
                return
            except Exception:
                pass

        if os.path.exists(png_path):
            try:
                self._icon_image = tk.PhotoImage(file=png_path)
                self.root.iconphoto(False, self._icon_image)
            except Exception as e:
                print(f"Nie udało się ustawić ikony okna: {e}")

    def _textbox_set_state(self, textbox, state):
        if textbox is None:
            return
        try:
            textbox.configure(state=state)
        except Exception:
            internal = getattr(textbox, "_textbox", None)
            if internal is not None:
                try:
                    internal.configure(state=state)
                except Exception:
                    pass

    def _textbox_get_value(self, textbox):
        if textbox is None:
            return ""
        try:
            return textbox.get("1.0", "end").strip()
        except Exception:
            internal = getattr(textbox, "_textbox", None)
            if internal is not None:
                try:
                    return internal.get("1.0", "end").strip()
                except Exception:
                    pass
        return ""

    def _profile_state_key(self, profile_key=None):
        key = profile_key if profile_key else "__custom__"
        return key

    def _get_saved_feature_state(self, feature_name, profile_key=None):
        profile = self._profile_state_key(profile_key if profile_key is not None else self.selected_profile_key)
        return self.saved_feature_states.get(profile, {}).get(feature_name)

    def _set_saved_feature_state(self, feature_name, value, profile_key=None):
        profile = self._profile_state_key(profile_key if profile_key is not None else self.selected_profile_key)
        current_profile_states = self.saved_feature_states.setdefault(profile, {})

        if value is None:
            if feature_name in current_profile_states:
                del current_profile_states[feature_name]
                if not current_profile_states:
                    del self.saved_feature_states[profile]
                if not self._loading_feature_states:
                    self.save_config()
            return

        if current_profile_states.get(feature_name) == value:
            return

        current_profile_states[feature_name] = value

        if not self._loading_feature_states:
            self.save_config()

    def _persist_feature_state(self, feature_name):
        if self._loading_feature_states:
            return

        state = self.feature_states.get(feature_name)
        if not state:
            return

        config = state.get("config", {})
        control_type = config.get("type")
        data = None

        if control_type == "slider":
            data = {
                "include": bool(state["include_var"].get()),
                "value": int(state["value_var"].get())
            }
        elif control_type == "int":
            data = {
                "include": bool(state["include_var"].get()),
                "value": state["entry_var"].get()
            }
        elif control_type == "toggle":
            data = {
                "raw_value": state.get("raw_value", "none")
            }
        elif control_type == "choice":
            data = {
                "raw_value": state.get("raw_value", "__none__")
            }
        elif control_type == "text":
            include = bool(state["include_var"].get())
            textbox_widget = state.get("textbox")
            if textbox_widget is not None:
                value = self._textbox_get_value(textbox_widget)
            else:
                entry_var = state.get("entry_var")
                value = entry_var.get() if entry_var is not None else ""
            data = {
                "include": include,
                "value": value
            }

        if data is not None:
            self._set_saved_feature_state(feature_name, data)

    def _apply_saved_feature_state(self, feature_name, state):
        saved = self._get_saved_feature_state(feature_name)
        if saved is None:
            return

        config = state.get("config", {})
        control_type = config.get("type")

        if control_type == "slider":
            include = bool(saved.get("include", False))
            value = saved.get("value")
            if value is not None:
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    value = config.get("min", 0)
                state["value_var"].set(value)
                state["slider"].set(value)
                state["value_label"].configure(text=str(value))
            if include:
                state["include_switch"].select()
                state["slider"].configure(state="normal")
            else:
                state["include_switch"].deselect()
                state["slider"].configure(state="disabled")
        elif control_type == "int":
            include = bool(saved.get("include", False))
            value = saved.get("value", "")
            state["entry_var"].set(value)
            if include:
                state["include_switch"].select()
                state["entry"].configure(state="normal")
            else:
                state["include_switch"].deselect()
                state["entry"].configure(state="disabled")
        elif control_type == "toggle":
            raw_value = saved.get("raw_value", "none")
            state["raw_value"] = raw_value
            values = self._toggle_display_values()
            mapping = {
                "none": values[0],
                "on": values[1],
                "off": values[2]
            }
            state["display_var"].set(mapping.get(raw_value, values[0]))
        elif control_type == "choice":
            raw_value = saved.get("raw_value", "__none__")
            state["raw_value"] = raw_value
            display = self.get_text("no_change") if raw_value == "__none__" else str(raw_value)
            state["display_var"].set(display)
        elif control_type == "text":
            include = bool(saved.get("include", False))
            value = saved.get("value", "")
            textbox_widget = state.get("textbox")
            if textbox_widget is not None:
                self._textbox_set_state(textbox_widget, "normal")
                try:
                    textbox_widget.delete("1.0", "end")
                    if value:
                        textbox_widget.insert("1.0", value)
                finally:
                    self._textbox_set_state(textbox_widget, "normal" if include else "disabled")
            entry_widget = state.get("entry")
            if state.get("entry_var") is not None and entry_widget is not None:
                state["entry_var"].set(value)
                entry_widget.configure(state="normal" if include else "disabled")
            if include:
                state["include_switch"].select()
            else:
                state["include_switch"].deselect()

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

        # Sekcja profilu urządzenia
        profile_frame = ctk.CTkFrame(device_section)
        profile_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.device_profile_label = ctk.CTkLabel(
            profile_frame,
            text=self.get_text("device_profile"),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.device_profile_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

        self.device_profile_combo = ctk.CTkComboBox(
            profile_frame,
            values=[],
            variable=self.device_profile_var,
            command=self.on_device_profile_change,
            width=320
        )
        self.device_profile_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        profile_frame.grid_columnconfigure(1, weight=1)

        # Sekcja funkcji dynamicznych
        features_section = ctk.CTkFrame(control_frame, corner_radius=10)
        features_section.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.features_section_title = ctk.CTkLabel(
            features_section,
            text=self.get_text("feature_section_title"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.features_section_title.pack(anchor="w", padx=20, pady=(20, 10))

        self.feature_container = ctk.CTkFrame(features_section)
        self.feature_container.pack(fill="both", expand=True, padx=10, pady=(0, 20))

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

        self.refresh_device_profile_options()
        self.on_device_profile_change(self.device_profile_var.get())

    def refresh_device_profile_options(self):
        if not hasattr(self, "device_profile_combo"):
            return

        custom_display = self.get_text("custom_profile")
        device_names = list(DEVICE_CAPABILITIES.keys())
        values = [custom_display] + device_names

        current_display = self._profile_display_from_key(self.selected_profile_key)
        if current_display not in values:
            current_display = custom_display
            self.selected_profile_key = None

        self.profile_display_map = {custom_display: None}
        for name in device_names:
            self.profile_display_map[name] = name

        self.device_profile_combo.configure(values=values)
        self.device_profile_var.set(current_display)

    def _profile_display_from_key(self, profile_key):
        if profile_key and profile_key in DEVICE_CAPABILITIES:
            return profile_key
        return self.get_text("custom_profile")

    def on_device_profile_change(self, selection):
        if not hasattr(self, "device_profile_combo"):
            return

        previous_profile = getattr(self, "selected_profile_key", None)

        if not selection:
            selection = self.device_profile_var.get()

        profile_key = self.profile_display_map.get(selection) if selection in self.profile_display_map else None
        if profile_key not in DEVICE_CAPABILITIES:
            profile_key = None

        self.selected_profile_key = profile_key
        self.device_profile_var.set(self._profile_display_from_key(profile_key))
        self.build_feature_controls()

        if profile_key != previous_profile:
            self.save_config()

    def build_feature_controls(self):
        if not hasattr(self, "feature_container"):
            return

        for child in self.feature_container.winfo_children():
            child.destroy()

        if self.selected_profile_key is None:
            raw_features = ["battery"] + [feature for feature in FEATURE_ORDER if feature in FEATURE_DEFINITIONS]
        else:
            raw_features = DEVICE_CAPABILITIES.get(self.selected_profile_key, [])

        features_sorted = self._sort_features(raw_features)
        self.active_features = features_sorted

        self.battery_supported = "battery" in features_sorted
        if hasattr(self, "battery_button"):
            state = "normal" if self.battery_supported else "disabled"
            self.battery_button.configure(state=state)

        self.feature_states = {}
        self._loading_feature_states = True

        has_controls = False
        try:
            for feature in features_sorted:
                if feature == "battery":
                    continue
                config = FEATURE_DEFINITIONS.get(feature)
                if not config:
                    continue
                has_controls = True
                control_state = self._create_feature_control(feature, config)
                if control_state:
                    self.feature_states[feature] = control_state
                    self._apply_saved_feature_state(feature, control_state)
        finally:
            self._loading_feature_states = False

        if not has_controls:
            info_label = ctk.CTkLabel(
                self.feature_container,
                text=self.get_text("no_changes_selected"),
                font=ctk.CTkFont(size=12)
            )
            info_label.pack(anchor="w", padx=20, pady=10)
        else:
            for feature in self.feature_states:
                self._persist_feature_state(feature)

    def _sort_features(self, raw_features):
        ordered = []
        seen = set()
        if "battery" in raw_features:
            ordered.append("battery")
            seen.add("battery")
        for feature in FEATURE_ORDER:
            if feature in raw_features and feature not in seen:
                ordered.append(feature)
                seen.add(feature)
        for feature in raw_features:
            if feature not in seen:
                ordered.append(feature)
                seen.add(feature)
        return ordered

    def _create_feature_control(self, feature_name, config):
        control_type = config.get("type")
        if control_type == "slider":
            return self._create_slider_control(feature_name, config)
        if control_type == "int":
            return self._create_int_control(feature_name, config)
        if control_type == "toggle":
            return self._create_toggle_control(feature_name, config)
        if control_type == "choice":
            return self._create_choice_control(feature_name, config)
        if control_type == "text":
            return self._create_text_control(feature_name, config)
        return None

    def get_feature_label(self, feature_name):
        config = FEATURE_DEFINITIONS.get(feature_name, {})
        label_key = config.get("label_key", feature_name)
        return self.get_text(label_key)

    def _create_slider_control(self, feature_name, config):
        frame = ctk.CTkFrame(self.feature_container)
        frame.pack(fill="x", padx=20, pady=10)

        header = ctk.CTkFrame(frame)
        header.pack(fill="x")

        label = ctk.CTkLabel(header, text=self.get_feature_label(feature_name), font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(side="left", padx=(0, 10), pady=(10, 5))

        include_var = ctk.BooleanVar(value=False)
        include_switch = ctk.CTkSwitch(header, text=self.get_text("include_setting"), variable=include_var)
        include_switch.pack(side="right", padx=(10, 0), pady=(10, 5))

        min_value = config.get("min", 0)
        max_value = config.get("max", 100)
        step = max(1, config.get("step", 1))

        value_var = ctk.IntVar(value=min_value)
        slider = ctk.CTkSlider(frame, from_=min_value, to=max_value)
        slider.pack(fill="x", padx=10, pady=(5, 5))
        slider.set(min_value)
        slider.configure(state="disabled")

        value_label = ctk.CTkLabel(frame, text=str(min_value), font=ctk.CTkFont(size=12, weight="bold"))
        value_label.pack(anchor="e", padx=10, pady=(0, 5))

        def slider_command(value):
            rounded = int(round(float(value) / step) * step)
            rounded = max(min_value, min(max_value, rounded))
            if rounded != value_var.get():
                value_var.set(rounded)
            if abs(slider.get() - rounded) > 0.001:
                slider.set(rounded)
            value_label.configure(text=str(rounded))
            if not self._loading_feature_states:
                self._persist_feature_state(feature_name)

        slider.configure(command=slider_command)

        def toggle_slider():
            slider.configure(state="normal" if include_var.get() else "disabled")
            if not self._loading_feature_states:
                self._persist_feature_state(feature_name)

        include_switch.configure(command=toggle_slider)

        hint_label = None
        if config.get("hint_key"):
            hint_label = ctk.CTkLabel(
                frame,
                text=self.get_text(config["hint_key"]),
                font=ctk.CTkFont(size=11),
                text_color=("gray60", "gray80")
            )
            hint_label.pack(anchor="w", padx=10, pady=(0, 5))

        return {
            "type": "slider",
            "frame": frame,
            "label": label,
            "include_switch": include_switch,
            "include_var": include_var,
            "value_var": value_var,
            "slider": slider,
            "value_label": value_label,
            "hint_label": hint_label,
            "config": config
        }

    def _create_int_control(self, feature_name, config):
        frame = ctk.CTkFrame(self.feature_container)
        frame.pack(fill="x", padx=20, pady=10)

        header = ctk.CTkFrame(frame)
        header.pack(fill="x")

        label = ctk.CTkLabel(header, text=self.get_feature_label(feature_name), font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(side="left", padx=(0, 10), pady=(10, 5))

        include_var = ctk.BooleanVar(value=False)
        include_switch = ctk.CTkSwitch(header, text=self.get_text("include_setting"), variable=include_var)
        include_switch.pack(side="right", padx=(10, 0), pady=(10, 5))

        entry_var = ctk.StringVar()
        placeholder = self.get_text(config["hint_key"]) if config.get("hint_key") else None
        entry = ctk.CTkEntry(frame, textvariable=entry_var, placeholder_text=placeholder)
        entry.pack(fill="x", padx=10, pady=(5, 10))
        entry.configure(state="disabled")

        def toggle_entry():
            entry.configure(state="normal" if include_var.get() else "disabled")
            if not self._loading_feature_states:
                self._persist_feature_state(feature_name)

        include_switch.configure(command=toggle_entry)

        def on_entry_change(*_):
            if not self._loading_feature_states:
                self._persist_feature_state(feature_name)

        entry_var.trace_add("write", on_entry_change)

        return {
            "type": "int",
            "frame": frame,
            "label": label,
            "include_switch": include_switch,
            "include_var": include_var,
            "entry": entry,
            "entry_var": entry_var,
            "config": config
        }

    def _toggle_display_values(self):
        return [self.get_text("no_change"), self.get_text("on"), self.get_text("off")]

    def _handle_toggle_selection(self, feature_name, selection):
        state = self.feature_states.get(feature_name)
        if not state:
            return
        mapping = {
            self.get_text("no_change"): "none",
            self.get_text("on"): "on",
            self.get_text("off"): "off"
        }
        state["raw_value"] = mapping.get(selection, "none")
        if not self._loading_feature_states:
            self._persist_feature_state(feature_name)

    def _create_toggle_control(self, feature_name, config):
        frame = ctk.CTkFrame(self.feature_container)
        frame.pack(fill="x", padx=20, pady=10)

        label = ctk.CTkLabel(frame, text=self.get_feature_label(feature_name), font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=10, pady=(10, 5))

        values = self._toggle_display_values()
        display_var = ctk.StringVar(value=values[0])
        option_menu = ctk.CTkOptionMenu(
            frame,
            values=values,
            variable=display_var,
            command=lambda selection, feature=feature_name: self._handle_toggle_selection(feature, selection)
        )
        option_menu.pack(anchor="w", padx=10, pady=(5, 10))

        return {
            "type": "toggle",
            "frame": frame,
            "label": label,
            "menu": option_menu,
            "display_var": display_var,
            "raw_value": "none",
            "config": config
        }

    def _handle_choice_selection(self, feature_name, selection):
        state = self.feature_states.get(feature_name)
        if not state:
            return
        if selection == self.get_text("no_change"):
            state["raw_value"] = "__none__"
        else:
            state["raw_value"] = selection
        if not self._loading_feature_states:
            self._persist_feature_state(feature_name)

    def _create_choice_control(self, feature_name, config):
        frame = ctk.CTkFrame(self.feature_container)
        frame.pack(fill="x", padx=20, pady=10)

        label = ctk.CTkLabel(frame, text=self.get_feature_label(feature_name), font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=10, pady=(10, 5))

        values = [self.get_text("no_change")] + [str(v) for v in config.get("values", [])]
        display_var = ctk.StringVar(value=values[0])
        option_menu = ctk.CTkOptionMenu(
            frame,
            values=values,
            variable=display_var,
            command=lambda selection, feature=feature_name: self._handle_choice_selection(feature, selection)
        )
        option_menu.pack(anchor="w", padx=10, pady=(5, 10))

        return {
            "type": "choice",
            "frame": frame,
            "label": label,
            "menu": option_menu,
            "display_var": display_var,
            "raw_value": "__none__",
            "config": config
        }

    def _create_text_control(self, feature_name, config):
        frame = ctk.CTkFrame(self.feature_container)
        frame.pack(fill="x", padx=20, pady=10)

        header = ctk.CTkFrame(frame)
        header.pack(fill="x")

        label = ctk.CTkLabel(header, text=self.get_feature_label(feature_name), font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(side="left", padx=(0, 10), pady=(10, 5))

        include_var = ctk.BooleanVar(value=False)
        include_switch = ctk.CTkSwitch(header, text=self.get_text("include_setting"), variable=include_var)
        include_switch.pack(side="right", padx=(10, 0), pady=(10, 5))

        placeholder = self.get_text(config["hint_key"]) if config.get("hint_key") else None
        multiline = config.get("multiline", False)

        entry_var = None
        textbox = None
        entry = None
        hint_label = None

        if multiline:
            textbox = ctk.CTkTextbox(frame, height=120, wrap="word")
            textbox.pack(fill="both", expand=True, padx=10, pady=(5, 10))
            self._textbox_set_state(textbox, "disabled")
            if placeholder:
                hint_label = ctk.CTkLabel(
                    frame,
                    text=placeholder,
                    font=ctk.CTkFont(size=11),
                    text_color=("gray60", "gray80")
                )
                hint_label.pack(anchor="w", padx=10, pady=(0, 5))
        else:
            entry_var = ctk.StringVar()
            entry = ctk.CTkEntry(frame, textvariable=entry_var, placeholder_text=placeholder)
            entry.pack(fill="x", padx=10, pady=(5, 10))
            entry.configure(state="disabled")

        def toggle_text():
            state = "normal" if include_var.get() else "disabled"
            if textbox is not None:
                self._textbox_set_state(textbox, state)
            elif entry is not None:
                entry.configure(state=state)
            if not self._loading_feature_states:
                self._persist_feature_state(feature_name)

        include_switch.configure(command=toggle_text)

        if entry_var is not None:
            def on_entry_text_change(*_):
                if not self._loading_feature_states:
                    self._persist_feature_state(feature_name)

            entry_var.trace_add("write", on_entry_text_change)

        if textbox is not None:
            def on_textbox_change(event=None):
                if not self._loading_feature_states:
                    self._persist_feature_state(feature_name)

            textbox.bind("<KeyRelease>", on_textbox_change)
            textbox.bind("<FocusOut>", on_textbox_change)

        return {
            "type": "text",
            "frame": frame,
            "label": label,
            "include_switch": include_switch,
            "include_var": include_var,
            "entry_var": entry_var,
            "entry": entry if not multiline else None,
            "textbox": textbox,
            "hint_label": hint_label,
            "config": config
        }

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
        if hasattr(self, "device_profile_label"):
            self.device_profile_label.configure(text=self.get_text("device_profile"))
        if hasattr(self, "features_section_title"):
            self.features_section_title.configure(text=self.get_text("feature_section_title"))
        self.apply_button.configure(text=self.get_text("apply"))
        self.battery_button.configure(text=self.get_text("check_battery"))
        self.status_label.configure(text=f"{self.get_text('status')} {self.get_text('ready')}")
        if hasattr(self, 'output_label'):
            self.output_label.configure(text=self.get_text("result"))

        self.refresh_device_profile_options()
        self.on_device_profile_change(self.device_profile_var.get())

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
            cmd = " ".join(shlex.quote(str(arg)) for arg in command)
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

    def get_feature_value(self, feature_name, config):
        state = self.feature_states.get(feature_name)
        if not state:
            return None

        label = self.get_feature_label(feature_name)

        try:
            control_type = config.get("type")

            if control_type == "slider":
                if not state.get("include_var").get():
                    return None
                value = int(state.get("value_var").get())
                min_val = config.get("min")
                max_val = config.get("max")
                if min_val is not None and value < min_val or max_val is not None and value > max_val:
                    detail = f"{value}"
                    if min_val is not None and max_val is not None:
                        detail = f"{value} ({min_val}-{max_val})"
                    elif min_val is not None:
                        detail = f"{value} (min {min_val})"
                    elif max_val is not None:
                        detail = f"{value} (max {max_val})"
                    raise ValueError(self.get_text("invalid_value").format(feature=label, detail=detail))
                return value

            if control_type == "int":
                if not state.get("include_var").get():
                    return None
                raw_value = state.get("entry_var").get().strip()
                if not raw_value:
                    raise ValueError(self.get_text("value_required").format(feature=label))
                value = int(raw_value)
                min_val = config.get("min")
                max_val = config.get("max")
                if min_val is not None and value < min_val or max_val is not None and value > max_val:
                    detail = f"{value}"
                    if min_val is not None and max_val is not None:
                        detail = f"{value} ({min_val}-{max_val})"
                    elif min_val is not None:
                        detail = f"{value} (min {min_val})"
                    elif max_val is not None:
                        detail = f"{value} (max {max_val})"
                    raise ValueError(self.get_text("invalid_value").format(feature=label, detail=detail))
                return value

            if control_type == "toggle":
                raw_value = state.get("raw_value", "none")
                if raw_value == "none":
                    return None
                return "1" if raw_value == "on" else "0"

            if control_type == "choice":
                raw_value = state.get("raw_value", "__none__")
                if raw_value == "__none__":
                    return None
                return raw_value

            if control_type == "text":
                if not state.get("include_var").get():
                    return None
                if state.get("textbox") is not None:
                    text_value = state.get("textbox").get("1.0", "end").strip()
                else:
                    text_value = state.get("entry_var").get().strip()
                if not text_value:
                    raise ValueError(self.get_text("value_required").format(feature=label))
                if not config.get("allow_newlines", False):
                    text_value = " ".join(text_value.split())
                return text_value

        except ValueError as exc:
            raise exc
        except Exception as exc:
            raise ValueError(self.get_text("invalid_value").format(feature=label, detail=str(exc))) from exc

        return None

    def build_command_for_feature(self, feature_name, config, value):
        flag = config.get("flag")
        if not flag:
            return []

        if isinstance(value, (list, tuple)):
            return [flag] + [str(v) for v in value]
        return [flag, str(value)]

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
                    error_label = self.get_text("error")
                    message = self.get_text("headsetcontrol_missing")
                    self.display_output(f"{error_label}: {message}")
                    self.update_status(f"{error_label}: {message}", True)
                    return

                base_command = ["headsetcontrol"]
                device = self.device_var.get().strip()
                if device:
                    base_command.extend(["-d", device])

                all_args = base_command.copy()
                changes_made = False

                for feature in self.active_features:
                    if feature == "battery":
                        continue
                    config = FEATURE_DEFINITIONS.get(feature)
                    if not config:
                        continue
                    try:
                        value = self.get_feature_value(feature, config)
                    except ValueError as err:
                        message = str(err)
                        self.update_status(message, True)
                        self.display_output(f"✗ {message}")
                        return
                    if value is None:
                        continue
                    all_args.extend(self.build_command_for_feature(feature, config, value))
                    changes_made = True

                if not changes_made:
                    message = self.get_text("no_changes_selected")
                    self.update_status(message)
                    self.display_output(message)
                    return

                executing_label = self.get_text("executing_command")
                self.display_output(f"{executing_label}: {' '.join(shlex.quote(str(arg)) for arg in all_args)}")
                success, stdout, stderr = self.run_headsetcontrol_command(all_args)

                if success:
                    self.update_status(self.get_text("settings_applied"))
                    self.display_output(f"✓ {self.get_text('settings_applied')}")
                else:
                    error_msg = stderr.strip() if stderr else self.get_text("command_failed")
                    error_label = self.get_text("error")
                    self.update_status(f"{error_label}: {error_msg}", True)
                    self.display_output(f"✗ {error_label}: {error_msg}")

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
