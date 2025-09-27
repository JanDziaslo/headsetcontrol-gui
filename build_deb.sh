#!/bin/bash
set -euo pipefail

DEFAULT_VERSION="1.1.0"
VERSION="${DEB_VERSION:-$DEFAULT_VERSION}"

function usage() {
  cat <<'EOS'
Usage: ./build_deb.sh [--version <version>]

Options:
  -v, --version <version>   Override the Debian package version (e.g. 2.0-1).
  -h, --help                Show this help message and exit.

Environment variables:
  DEB_VERSION               Alternate way to override the package version.
EOS
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--version)
      if [[ $# -lt 2 ]]; then
        echo "Error: --version requires a value" >&2
        usage
        exit 1
      fi
      VERSION="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

APP_NAME="headsetcontrol-gui"
PACKAGE_NAME="headsetcontrolgui"
ARCH="all"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build/${PACKAGE_NAME}_${VERSION}"
PKG_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
DEBIAN_DIR="$PKG_ROOT/DEBIAN"
APP_DIR="$PKG_ROOT/opt/$APP_NAME"
BIN_DIR="$PKG_ROOT/usr/bin"
DESKTOP_DIR="$PKG_ROOT/usr/share/applications"
ICON_DIR="$PKG_ROOT/usr/share/icons/hicolor/256x256/apps"
DOC_DIR="$PKG_ROOT/usr/share/doc/$PACKAGE_NAME"
OUTPUT_DIR="$SCRIPT_DIR/deb"

function cleanup() {
  rm -rf "$BUILD_DIR"
}
trap cleanup EXIT

mkdir -p "$DEBIAN_DIR" "$APP_DIR" "$BIN_DIR" "$DESKTOP_DIR" "$ICON_DIR" "$DOC_DIR" "$OUTPUT_DIR"

install -m 755 "$SCRIPT_DIR/start_gui.sh" "$APP_DIR/start_gui.sh"
install -m 644 "$SCRIPT_DIR/headsetcontrolGUI.py" "$APP_DIR/headsetcontrolGUI.py"
install -m 644 "$SCRIPT_DIR/requirements.txt" "$APP_DIR/requirements.txt"
install -m 644 "$SCRIPT_DIR/headsetcontrolGUI.png" "$APP_DIR/headsetcontrolGUI.png"
install -m 644 "$SCRIPT_DIR/LICENSE" "$DOC_DIR/copyright"

if [[ -f "$SCRIPT_DIR/README.md" ]]; then
  gzip -cn "$SCRIPT_DIR/README.md" > "$DOC_DIR/README.md.gz"
fi

echo "Package built on $(date -u +%Y-%m-%dT%H:%M:%SZ)" | gzip -cn > "$DOC_DIR/changelog.gz"

cat <<'EOF' > "$BIN_DIR/$APP_NAME"
#!/bin/bash
exec /opt/headsetcontrol-gui/start_gui.sh "$@"
EOF
chmod 755 "$BIN_DIR/$APP_NAME"

cat <<'EOF' > "$BIN_DIR/headsetcontrolgui"
#!/bin/bash
exec /opt/headsetcontrol-gui/start_gui.sh "$@"
EOF
chmod 755 "$BIN_DIR/headsetcontrolgui"

cat <<'EOF' > "$DESKTOP_DIR/headsetcontrol-gui.desktop"
[Desktop Entry]
Type=Application
Name=HeadsetControl GUI
Comment=Nowoczesny panel sterowania słuchawkami
Exec=headsetcontrol-gui
Icon=headsetcontrol-gui
Terminal=false
Categories=AudioVideo;Audio;Settings;
StartupNotify=false
StartupWMClass=headsetcontrol-gui
EOF

install -m 644 "$SCRIPT_DIR/headsetcontrolGUI.png" "$ICON_DIR/headsetcontrol-gui.png"

cat <<EOF > "$DEBIAN_DIR/control"
Package: $PACKAGE_NAME
Version: $VERSION
Section: sound
Priority: optional
Architecture: $ARCH
Maintainer: Jan Dziasło <contact@example.com>
Depends: python3 (>= 3.8), python3-venv, python3-pip, python3-tk, libgl1
Description: HeadsetControl GUI - modern control panel for wireless headsets
 HeadsetControl GUI provides ready-made profiles, dynamic controls, and
 persistence for settings when using the headsetcontrol CLI utility.
EOF

cat <<'EOF' > "$DEBIAN_DIR/postinst"
#!/bin/bash
set -e

APP_DIR="/opt/headsetcontrol-gui"
VENV_DIR="$APP_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"

if [ -d "/etc/headsetcontrolgui" ]; then
  rm -rf /etc/headsetcontrolgui || true
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -q -f /usr/share/icons/hicolor || true
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database >/dev/null 2>&1 || true
fi

exit 0
EOF
chmod 755 "$DEBIAN_DIR/postinst"

cat <<'EOF' > "$DEBIAN_DIR/postrm"
#!/bin/bash
set -e

if [ "$1" = "purge" ]; then
  rm -rf /opt/headsetcontrol-gui/venv
  rm -rf /etc/headsetcontrolgui
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -q -f /usr/share/icons/hicolor || true
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database >/dev/null 2>&1 || true
fi

exit 0
EOF
chmod 755 "$DEBIAN_DIR/postrm"

convert_command=$(command -v convert || true)
for size in 128 64 48 32 24 16; do
  target_dir="$PKG_ROOT/usr/share/icons/hicolor/${size}x${size}/apps"
  mkdir -p "$target_dir"
  if [[ -n "$convert_command" ]]; then
    "$convert_command" "$SCRIPT_DIR/headsetcontrolGUI.png" -resize ${size}x${size} "$target_dir/headsetcontrol-gui.png"
  else
    install -m 644 "$SCRIPT_DIR/headsetcontrolGUI.png" "$target_dir/headsetcontrol-gui.png"
  fi
done

dpkg-deb --build --root-owner-group "$PKG_ROOT" "$OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo "\nCreated Debian package: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo "If the installation reports missing dependencies, run: sudo apt install -f"
