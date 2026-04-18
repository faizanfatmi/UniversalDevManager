#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
DIST="$ROOT/dist"
BUILD="$ROOT/build/appimage"
APPDIR="$BUILD/UniversalDevManager.AppDir"

echo "=== Building Linux AppImage ==="

# Step 1: PyInstaller one-directory build
python3 -m PyInstaller \
    --onedir \
    --name UniversalDevManager \
    --add-data "$ROOT/tools.json:." \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtWidgets \
    --distpath "$BUILD/pyinstaller-dist" \
    --workpath "$BUILD/pyinstaller-work" \
    --specpath "$BUILD" \
    "$ROOT/main.py"

# Step 2: Create AppDir structure
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp -r "$BUILD/pyinstaller-dist/UniversalDevManager/"* "$APPDIR/usr/bin/"

# Desktop entry
cat > "$APPDIR/usr/share/applications/UniversalDevManager.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=Universal Dev Manager
Comment=Cross-platform developer tool installer
Exec=UniversalDevManager
Icon=UniversalDevManager
Categories=Development;
Terminal=false
EOF

cp "$APPDIR/usr/share/applications/UniversalDevManager.desktop" "$APPDIR/UniversalDevManager.desktop"

# Create a simple icon (placeholder SVG converted to PNG would go here)
# For now, create a minimal placeholder
convert -size 256x256 xc:"#1a1d23" -fill "#4ade80" -gravity center \
    -pointsize 120 -annotate 0 "U" \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps/UniversalDevManager.png" 2>/dev/null || \
    echo "ImageMagick not available, skipping icon generation"

# Copy icon to AppDir root
cp "$APPDIR/usr/share/icons/hicolor/256x256/apps/UniversalDevManager.png" \
   "$APPDIR/UniversalDevManager.png" 2>/dev/null || true

# AppRun
cat > "$APPDIR/AppRun" << 'APPRUN'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
exec "${HERE}/usr/bin/UniversalDevManager" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

# Step 3: Build AppImage
mkdir -p "$DIST"

if ! command -v appimagetool &>/dev/null; then
    echo "Downloading appimagetool..."
    ARCH="$(uname -m)"
    wget -q "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-${ARCH}.AppImage" \
        -O "$BUILD/appimagetool"
    chmod +x "$BUILD/appimagetool"
    APPIMAGETOOL="$BUILD/appimagetool"
else
    APPIMAGETOOL="appimagetool"
fi

ARCH="$(uname -m)" "$APPIMAGETOOL" "$APPDIR" "$DIST/UniversalDevManager-${ARCH}.AppImage"

echo "=== AppImage created at $DIST/ ==="
