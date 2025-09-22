#!/usr/bin/env bash
set -euo pipefail

# Automatyczna instalacja zależności i uruchomienie GUI
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Tworzenie wirtualnego środowiska, jeśli brak
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Aktywacja venv i instalacja zależności
# shellcheck source=/dev/null
source venv/bin/activate
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Uruchomienie aplikacji
exec python headsetcontrolGUI.py "$@"

