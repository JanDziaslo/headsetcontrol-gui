import tkinter as tk
from tkinter import ttk
import subprocess
import json
import os

# Configuration file path
CONFIG_FILE = 'headsetcontrol_config.json'

# Language dictionaries
LANGUAGES = {
    'en': {
        'title': 'HeadsetControl GUI',
        'settings': 'Settings',
        'actions': 'Actions',
        'device': 'Device (vendorid:productid):',
        'sidetone': 'Sidetone:',
        'equalizer_preset': 'Equalizer preset:',
        'lights': 'Lights:',
        'voice_prompt': 'Voice prompt:',
        'mic_mute': 'Mic mute:',
        'check_battery': 'Check Battery',
        'apply_settings': 'Apply Settings',
        'result': 'Result:',
        'on': 'On',
        'off': 'Off',
        'language': 'Language:',
        'theme': 'Theme:',
        'light_theme': 'Light',
        'dark_theme': 'Dark'
    },
    'pl': {
        'title': 'HeadsetControl GUI',
        'settings': 'Ustawienia',
        'actions': 'Akcje',
        'device': 'Urządzenie (vendorid:productid):',
        'sidetone': 'Poziom słyszalności:',
        'equalizer_preset': 'Preset equalizera:',
        'lights': 'Światła:',
        'voice_prompt': 'Komunikaty głosowe:',
        'mic_mute': 'Wyciszenie mikrofonu:',
        'check_battery': 'Sprawdź baterię',
        'apply_settings': 'Zastosuj ustawienia',
        'result': 'Wynik:',
        'on': 'Włącz',
        'off': 'Wyłącz',
        'language': 'Język:',
        'theme': 'Motyw:',
        'light_theme': 'Jasny',
        'dark_theme': 'Ciemny'
    }
}

def load_config():
    """Load configuration from file"""
    default_config = {
        'language': 'en',
        'theme': 'dark'
    }

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
        except:
            return default_config
    return default_config

def save_config():
    """Save configuration to file"""
    config = {
        'language': current_language.get(),
        'theme': current_theme.get()
    }

    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

def get_text(key):
    """Get text in current language"""
    return LANGUAGES[current_language.get()].get(key, key)

def theme_display_to_value(display_text):
    """Convert display text to theme value"""
    if display_text == get_text('dark_theme'):
        return 'dark'
    elif display_text == get_text('light_theme'):
        return 'light'
    return 'dark'

def theme_value_to_display(value):
    """Convert theme value to display text"""
    if value == 'dark':
        return get_text('dark_theme')
    else:
        return get_text('light_theme')

def apply_theme():
    """Apply the selected theme"""
    theme = current_theme.get()

    if theme == 'dark':
        # Dark theme colors - improved
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        entry_bg = '#3c3c3c'
        entry_fg = '#ffffff'
        button_bg = '#404040'
        button_fg = '#ffffff'
        frame_bg = '#2d2d2d'

        style.theme_use('clam')
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11, 'bold'), background=button_bg, foreground=button_fg)
        style.configure('TFrame', background=bg_color)
        style.configure('TLabelFrame', background=frame_bg, foreground=fg_color, borderwidth=1, relief='solid')
        style.configure('TLabelFrame.Label', background=frame_bg, foreground=fg_color, font=('Segoe UI', 10, 'bold'))
        style.configure('TCombobox', fieldbackground=entry_bg, foreground=entry_fg, background=button_bg, borderwidth=1)
        style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg, borderwidth=1)

        style.map('TButton',
                 background=[('active', '#505050'), ('pressed', '#606060')])
        style.map('TCombobox',
                 fieldbackground=[('readonly', entry_bg), ('focus', entry_bg)],
                 selectbackground=[('readonly', '#505050')])

        root.configure(bg=bg_color)
        output_text.configure(bg=entry_bg, fg=entry_fg, insertbackground=fg_color, selectbackground='#505050')

        # Style the sidetone scale for dark theme
        sidetone_scale.configure(bg=bg_color, fg=fg_color, troughcolor=entry_bg,
                               highlightbackground=bg_color, activebackground='#505050')

    else:
        # Light theme - improved
        bg_color = '#f0f0f0'
        fg_color = '#000000'

        style.theme_use('clam')
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11, 'bold'))
        style.configure('TFrame', background=bg_color)
        style.configure('TLabelFrame', background=bg_color, foreground=fg_color)
        style.configure('TLabelFrame.Label', background=bg_color, foreground=fg_color, font=('Segoe UI', 10, 'bold'))
        style.configure('TCombobox')
        style.configure('TEntry')

        # Reset button and combobox mappings
        style.map('TButton')
        style.map('TCombobox')

        root.configure(bg=bg_color)
        output_text.configure(bg='white', fg='black', insertbackground='black', selectbackground='#0078d4')

        # Reset sidetone scale to default light theme
        sidetone_scale.configure(bg=bg_color, fg=fg_color, troughcolor='white',
                               highlightbackground=bg_color, activebackground='lightblue')

def update_language():
    """Update all text elements with current language"""
    root.title(get_text('title'))
    header.configure(text=get_text('title'))
    settings_frame.configure(text=get_text('settings'))
    actions_frame.configure(text=get_text('actions'))

    device_label.configure(text=get_text('device'))
    sidetone_label.configure(text=get_text('sidetone'))
    preset_label.configure(text=get_text('equalizer_preset'))
    lights_label.configure(text=get_text('lights'))
    voice_label.configure(text=get_text('voice_prompt'))
    mute_label.configure(text=get_text('mic_mute'))

    battery_btn.configure(text=get_text('check_battery'))
    apply_btn.configure(text=get_text('apply_settings'))
    output_label.configure(text=get_text('result'))

    language_label.configure(text=get_text('language'))
    theme_label.configure(text=get_text('theme'))

    # Update combobox values
    on_off_values = ['', get_text('on'), get_text('off')]
    lights_combo.configure(values=on_off_values)
    voice_combo.configure(values=on_off_values)
    mute_combo.configure(values=on_off_values)

    # Update theme combobox values and current selection
    theme_values = [get_text('light_theme'), get_text('dark_theme')]
    theme_combo.configure(values=theme_values)

    # Set current theme display value
    current_display = theme_value_to_display(current_theme.get())
    theme_display_var.set(current_display)

def on_language_change(*args):
    """Handle language change"""
    update_language()
    save_config()

def on_theme_display_change(*args):
    """Handle theme display change"""
    display_value = theme_display_var.get()
    theme_value = theme_display_to_value(display_value)
    current_theme.set(theme_value)

def on_theme_change(*args):
    """Handle theme change"""
    apply_theme()
    save_config()

def run_headsetcontrol(args):
    try:
        result = subprocess.run(['headsetcontrol'] + args, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def gui_to_flag(val):
    if val == get_text('on'):
        return '1'
    elif val == get_text('off'):
        return '0'
    return ''

def apply_settings():
    args = []
    device = device_var.get().strip()
    if device:
        args += ['-d', device]
    sidetone = sidetone_var.get()
    if sidetone != '':
        args += ['-s', str(sidetone)]
    eqpreset = eqpreset_var.get()
    if eqpreset != '':
        args += ['-p', eqpreset]
    light_flag = gui_to_flag(light_var.get())
    if light_flag:
        args += ['-l', light_flag]
    voice_flag = gui_to_flag(voice_var.get())
    if voice_flag:
        args += ['-v', voice_flag]
    mute_flag = gui_to_flag(mute_var.get())
    if mute_flag:
        args += ['-r', mute_flag]
    output = run_headsetcontrol(args)
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state='disabled')

def check_battery():
    args = []
    device = device_var.get().strip()
    if device:
        args += ['-d', device]
    args += ['-b']
    output = run_headsetcontrol(args)
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state='disabled')

# Load configuration
config = load_config()

root = tk.Tk()
root.resizable(False, False)

style = ttk.Style()

mainframe = ttk.Frame(root, padding=20)
mainframe.grid(row=0, column=0, sticky='nsew')

# Configuration variables
current_language = tk.StringVar(value=config['language'])
current_theme = tk.StringVar(value=config['theme'])
theme_display_var = tk.StringVar()

# GUI variables
device_var = tk.StringVar()
sidetone_var = tk.IntVar(value=64)
eqpreset_var = tk.StringVar(value='0')
light_var = tk.StringVar(value='')
voice_var = tk.StringVar(value='')
mute_var = tk.StringVar(value='')

# Header
header = ttk.Label(mainframe, font=('Segoe UI', 16, 'bold'))
header.grid(row=0, column=0, columnspan=2, pady=(0, 15))

# Language and theme selection
config_frame = ttk.Frame(mainframe)
config_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))

language_label = ttk.Label(config_frame)
language_label.grid(row=0, column=0, padx=(0, 5))
language_combo = ttk.Combobox(config_frame, textvariable=current_language, values=['en', 'pl'], width=5, state='readonly')
language_combo.grid(row=0, column=1, padx=(0, 20))

theme_label = ttk.Label(config_frame)
theme_label.grid(row=0, column=2, padx=(0, 5))
theme_combo = ttk.Combobox(config_frame, textvariable=theme_display_var, values=[], width=10, state='readonly')
theme_combo.grid(row=0, column=3)

# Settings frame
settings_frame = ttk.LabelFrame(mainframe, padding=12)
settings_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 10))
settings_frame.columnconfigure(1, weight=1)

# Device
device_label = ttk.Label(settings_frame)
device_label.grid(row=0, column=0, sticky='e', pady=2, padx=2)
ttk.Entry(settings_frame, textvariable=device_var, width=20).grid(row=0, column=1, sticky='w', pady=2, padx=2)

# Sidetone
sidetone_subframe = ttk.Frame(settings_frame)
sidetone_subframe.grid(row=1, column=0, columnspan=2, sticky='ew', pady=4)
sidetone_label = ttk.Label(sidetone_subframe)
sidetone_label.pack(side='left', padx=(0, 8))
sidetone_scale = tk.Scale(sidetone_subframe, from_=0, to=128, orient='horizontal', variable=sidetone_var, length=160, showvalue=True, resolution=1)
sidetone_scale.pack(side='left')

# Equalizer preset
preset_label = ttk.Label(settings_frame)
preset_label.grid(row=2, column=0, sticky='e', pady=2, padx=2)
ttk.Combobox(settings_frame, textvariable=eqpreset_var, values=['0', '1', '2', '3'], width=7, state='readonly').grid(row=2, column=1, sticky='w', pady=2, padx=2)

# Lights
lights_label = ttk.Label(settings_frame)
lights_label.grid(row=3, column=0, sticky='e', pady=2, padx=2)
lights_combo = ttk.Combobox(settings_frame, textvariable=light_var, values=[], width=7, state='readonly')
lights_combo.grid(row=3, column=1, sticky='w', pady=2, padx=2)

# Voice prompt
voice_label = ttk.Label(settings_frame)
voice_label.grid(row=4, column=0, sticky='e', pady=2, padx=2)
voice_combo = ttk.Combobox(settings_frame, textvariable=voice_var, values=[], width=7, state='readonly')
voice_combo.grid(row=4, column=1, sticky='w', pady=2, padx=2)

# Mic mute
mute_label = ttk.Label(settings_frame)
mute_label.grid(row=5, column=0, sticky='e', pady=2, padx=2)
mute_combo = ttk.Combobox(settings_frame, textvariable=mute_var, values=[], width=7, state='readonly')
mute_combo.grid(row=5, column=1, sticky='w', pady=2, padx=2)

# Actions frame
actions_frame = ttk.LabelFrame(mainframe, padding=12)
actions_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 10))

battery_btn = ttk.Button(actions_frame, command=check_battery)
battery_btn.grid(row=0, column=0, padx=5, pady=2)
apply_btn = ttk.Button(actions_frame, command=apply_settings)
apply_btn.grid(row=0, column=1, padx=5, pady=2)

# Output
output_label = ttk.Label(mainframe, font=('Segoe UI', 10, 'bold'))
output_label.grid(row=4, column=0, columnspan=2, sticky='w', pady=(0, 2))
output_text = tk.Text(mainframe, height=7, width=60, state='disabled', font=('Consolas', 10))
output_text.grid(row=5, column=0, columnspan=2, padx=2, pady=(0, 10))

# Bind events
current_language.trace('w', on_language_change)
current_theme.trace('w', on_theme_change)
theme_display_var.trace('w', on_theme_display_change)

# Initialize
update_language()
apply_theme()

root.mainloop()
