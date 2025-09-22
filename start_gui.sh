#!/bin/bash

# HeadsetControl GUI - Autostart Script
# Skrypt uruchamiający dla autostartu aplikacji

# Nazwa aplikacji
APP_NAME="HeadsetControl GUI"

# Ścieżka do katalogu projektu (zmień na swoją ścieżkę)
PROJECT_DIR="$(dirname "$(realpath "$0")")"

# Funkcja logowania
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [HeadsetControl-GUI] $1" | tee -a "$HOME/.headsetcontrol-gui.log"
}

# Sprawdź czy jest sesja graficzna
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    log "ERROR: Brak sesji graficznej. Aplikacja wymaga środowiska graficznego."
    exit 1
fi

# Przejdź do katalogu projektu
cd "$PROJECT_DIR" || {
    log "ERROR: Nie można przejść do katalogu projektu: $PROJECT_DIR"
    exit 1
}

log "Uruchamianie $APP_NAME..."

# Sprawdź czy środowisko wirtualne istnieje
if [ ! -d "venv" ]; then
    log "Środowisko wirtualne nie istnieje. Tworzenie..."
    python3 -m venv venv || {
        log "ERROR: Nie można utworzyć środowiska wirtualnego"
        exit 1
    }
fi

# Aktywuj środowisko wirtualne
source venv/bin/activate || {
    log "ERROR: Nie można aktywować środowiska wirtualnego"
    exit 1
}

# Sprawdź czy zależności są zainstalowane
if ! python -c "import customtkinter" 2>/dev/null; then
    log "Instalowanie zależności..."
    pip install -r requirements.txt || {
        log "ERROR: Nie można zainstalować zależności"
        exit 1
    }
fi

# Sprawdź czy headsetcontrol jest dostępny
if ! command -v headsetcontrol >/dev/null 2>&1; then
    log "WARNING: headsetcontrol nie jest zainstalowany w systemie"
    log "Aplikacja będzie działać, ale funkcje sterowania słuchawkami nie będą dostępne"
fi

# Dodaj opóźnienie dla autostartu (daj czas na załadowanie się pulpitu)
if [ "$1" = "--autostart" ]; then
    log "Opóźnienie autostartu - czekam 10 sekund..."
    sleep 10
fi

# Uruchom aplikację
log "Uruchamianie aplikacji..."
python headsetcontrolGUI.py &

# Zapisz PID
APP_PID=$!
echo $APP_PID > "$HOME/.headsetcontrol-gui.pid"

log "$APP_NAME uruchomiony z PID: $APP_PID"

# Czekaj na zakończenie aplikacji
wait $APP_PID
EXIT_CODE=$?

log "$APP_NAME zakończony z kodem: $EXIT_CODE"

# Usuń plik PID
rm -f "$HOME/.headsetcontrol-gui.pid"

exit $EXIT_CODE
