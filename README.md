# HeadsetControl GUI - Nowoczesny Panel Sterowania

Graficzny interfejs użytkownika dla HeadsetControl - narzędzia do kontroli bezprzewodowych słuchawek gamingowych.

![HeadsetControl GUI](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎧 Obsługiwane Funkcje

- **Profile słuchawek** – wybierz model z listy, a aplikacja wyświetli tylko te ustawienia, które są obsługiwane przez dane urządzenie (wykorzystuje oficjalną tabelę HeadsetControl) i zapamiętuje ostatnio wybrany profil między uruchomieniami.
- **Pamięć ustawień** – dla każdego profilu zapisywane są ostatnio użyte wartości suwaków, przełączników i pól tekstowych, dzięki czemu po ponownym uruchomieniu aplikacji lub zmianie profilu wracasz do swoich preferencji.
- **Sidetone** – płynna regulacja słyszalności własnego głosu (0–128) z opcją włączenia tylko wtedy, gdy chcesz zastosować zmianę.
- **Equalizer** – presety (0–3), pełna krzywa equalizera oraz equalizer parametryczny (częstotliwość, zysk, Q, typ filtra).
- **Światła i komunikaty** – sterowanie podświetleniem, komunikatami głosowymi, dźwiękiem powiadomień oraz funkcją „rotate to mute”.
- **ChatMix oraz czas bezczynności** – szybka korekta balansu pomiędzy grą a czatem oraz ustawienie automatycznego wyłączania słuchawek.
- **Mikrofon** – zmiana głośności mikrofonu oraz jasności diody LED informującej o wyciszeniu.
- **Limiter głośności i Bluetooth** – aktywacja ogranicznika głośności, włączanie Bluetooth po starcie oraz regulacja głośności połączeń Bluetooth.
- **Poziom baterii** – przycisk baterii jest automatycznie włączony tylko dla urządzeń, które udostępniają tę informację.
- **Opcjonalny identyfikator urządzenia** – możliwość wskazania konkretnego dongla (vendor:product ID) bez utraty prostoty obsługi.

## 🖥️ Interfejs

- **Nowoczesny design** - Ciemny/jasny motyw z zaokrąglonymi elementami
- **Wielojęzyczność** - Polski i angielski
- **Przewijanie kółkiem myszy** - Stabilne przewijanie na Linux/Windows/Mac
- **Logi operacji** - Podgląd wykonywanych komend w czasie rzeczywistym
- **Progress bar** - Wizualizacja postępu operacji
- **Automatyczne czyszczenie** - Pole wyników czyści się przed każdą operacją

## 📋 Wymagania

### Wymagania systemowe
- **Python 3.8+**
- **HeadsetControl** - [Zainstaluj z GitHub](https://github.com/Sapd/HeadsetControl)
- **Tkinter** - Zazwyczaj preinstalowane z Pythonem

### Obsługiwane słuchawki
Aplikacja działa ze wszystkimi słuchawkami obsługiwanymi przez HeadsetControl:
- SteelSeries (Arctis seria)
- Logitech (seria G)
- Corsair (seria VOID)
- HyperX
- Razer
- ROCCAT
- Sennheiser
- I wiele innych...

Pełna lista: [HeadsetControl README](https://github.com/Sapd/HeadsetControl#supported-headsets)

## 🚀 Instalacja

### 1. Pobierz kod źródłowy
```bash
git clone https://github.com/user/headsetcontrol-gui.git
cd headsetcontrol-gui
```

### 2. Uruchom aplikację
```bash
# Automatyczna instalacja i uruchomienie
./run.sh

# Lub ręcznie:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python headsetcontrolGUI.py
```

### 3. Zainstaluj HeadsetControl (jeśli nie masz)
```bash
# Ubuntu/Debian
sudo apt install headsetcontrol

# Arch Linux
yay -S headsetcontrol

# Z kodu źródłowego
git clone https://github.com/Sapd/HeadsetControl
cd HeadsetControl
mkdir build && cd build
cmake ..
make
sudo make install
```

## 🔧 Konfiguracja Autostartu

### Opcja 1: Desktop Entry (zalecane)
```bash
# Skopiuj plik .desktop do autostartu
cp headsetcontrol-gui.desktop ~/.config/autostart/

# WAŻNE: Edytuj ścieżkę w pliku .desktop
nano ~/.config/autostart/headsetcontrol-gui.desktop
# Zmień Exec= na swoją pełną ścieżkę
```

### Opcja 2: Bezpośredni skrypt
```bash
# Nadaj uprawnienia wykonywania
chmod +x start_gui.sh

# Dodaj do autostartu przez GUI menedżera sesji lub:
echo "/pełna/ścieżka/do/start_gui.sh --autostart" >> ~/.xprofile
```

### Opcja 3: Systemd User Service
```bash
# Utwórz service
nano ~/.config/systemd/user/headsetcontrol-gui.service

[Unit]
Description=HeadsetControl GUI
After=graphical-session.target

[Service]
Type=forking
ExecStart=/pełna/ścieżka/do/start_gui.sh --autostart
Restart=on-failure
Environment=DISPLAY=:0

[Install]
WantedBy=default.target

# Aktywuj service
systemctl --user enable headsetcontrol-gui.service
systemctl --user start headsetcontrol-gui.service
```

## 📁 Struktura Projektu

```
headsetcontrol-gui/
├── headsetcontrolGUI.py          # Główny plik aplikacji
├── requirements.txt              # Zależności Python
├── run.sh                       # Prosty skrypt uruchamiający
├── start_gui.sh                 # Skrypt autostartu z logowaniem
├── headsetcontrol-gui.desktop   # Plik desktop entry
├── headsetcontrol_config.json   # Konfiguracja (auto-generowany)
└── README.md                    # Ta dokumentacja
```

## 🎮 Użytkowanie

1. **Podłącz słuchawki** i upewnij się, że są wykryte przez system
2. **Uruchom aplikację** przez `./run.sh` lub `./start_gui.sh`
3. **Opcjonalnie podaj Device ID** (vendor:product) jeśli masz wiele urządzeń
4. **Dostosuj ustawienia** przy pomocy suwaków i przełączników
5. **Kliknij "Zastosuj ustawienia"** aby aplikować zmiany
6. **Sprawdź logi** w sekcji "Wynik" na dole okna

### Znajdowanie Device ID
```bash
# Lista urządzeń HeadsetControl
headsetcontrol -l

# Przykład wyniku:
# Found SteelSeries Arctis 7 (1038:12ad)
# Użyj: 1038:12ad w polu Device ID
```

## 🛠️ Rozwiązywanie Problemów

### Aplikacja nie uruchamia się
```bash
# Sprawdź czy CustomTkinter jest zainstalowany
python3 -c "import customtkinter; print('OK')"

# Sprawdź logi
tail -f ~/.headsetcontrol-gui.log

# Sprawdź czy Python ma dostęp do GUI
echo $DISPLAY
```

### HeadsetControl nie wykrywa słuchawek
```bash
# Sprawdź czy urządzenie jest podłączone
lsusb | grep -i headset

# Uruchom HeadsetControl z debug
headsetcontrol -b --debug

# Sprawdź uprawnienia (może wymagać sudo)
sudo headsetcontrol -b
```

### Przewijanie kółkiem myszy nie działa
- Upewnij się, że kursor jest nad zawartością okna
- Zmień rozmiar okna jeśli jest za małe
- Problem może występować w niektórych środowiskach Wayland

### Błędy uprawnień
```bash
# Dodaj użytkownika do grupy audio
sudo usermod -a -G audio $USER

# Logout/login po zmianie grup
```

## 🧰 Rozwój

### Uruchomienie w trybie debug
```bash
# Włącz verbose mode w HeadsetControl
export HEADSETCONTROL_DEBUG=1
python headsetcontrolGUI.py
```

### Dodawanie tłumaczeń
Edytuj słownik `LANGUAGES` w `headsetcontrolGUI.py`:
```python
LANGUAGES = {
    "pl": { ... },
    "en": { ... },
    "de": { ... }  # Nowy język
}
```

## 📝 Licencja

MIT License - zobacz plik `LICENSE` dla szczegółów.

## 🤝 Wkład w projekt

1. Fork repository
2. Utwórz branch funkcjonalności (`git checkout -b feature/AmazingFeature`)
3. Commit zmian (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 🔗 Linki

- [HeadsetControl](https://github.com/Sapd/HeadsetControl) - Podstawowe narzędzie CLI
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Nowoczesna biblioteka GUI
- [Lista obsługiwanych słuchawek](https://github.com/Sapd/HeadsetControl#supported-headsets)

## 📞 Wsparcie

Jeśli masz problemy:
1. Sprawdź sekcję "Rozwiązywanie problemów" powyżej
2. Sprawdź logi w `~/.headsetcontrol-gui.log`
3. Otwórz issue na GitHub z logami i opisem problemu
4. Dołącz informacje o systemie: `uname -a` i `python3 --version`

---
**HeadsetControl GUI v2.0** - Nowoczesny interfejs 2025 ✨
