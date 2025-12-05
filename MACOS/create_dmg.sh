#!/bin/bash
# Create DMG installer for macOS

set -e

echo "=========================================="
echo "Creating DMG Installer"
echo "=========================================="
echo ""

# Check if app exists
if [ ! -d "dist/YouTubeToMP3.app" ]; then
    echo "ERROR: Application bundle not found. Please run build_macos.sh first."
    exit 1
fi

APP_NAME="YouTubeToMP3"
DMG_NAME="${APP_NAME}_macOS"
VERSION="2.0.0"
DMG_FILE="${DMG_NAME}_v${VERSION}.dmg"

# Clean previous DMG
rm -f "${DMG_FILE}" "${DMG_NAME}.dmg"

# Create temporary directory for DMG contents
TEMP_DMG="temp_dmg"
rm -rf "${TEMP_DMG}"
mkdir -p "${TEMP_DMG}"

# Copy app to temp directory
cp -R "dist/${APP_NAME}.app" "${TEMP_DMG}/"

# Create Applications symlink (optional, for easy drag-to-install)
ln -s /Applications "${TEMP_DMG}/Applications"

# Create README
cat > "${TEMP_DMG}/README.txt" << EOF
YouTube to MP3 Downloader for macOS
Version ${VERSION}

INSTALLATION:
1. Drag YouTubeToMP3.app to your Applications folder
2. Open Applications and double-click YouTubeToMP3.app
3. If you see a security warning, go to System Preferences > Security & Privacy
   and click "Open Anyway"

REQUIREMENTS:
- macOS 10.13 or later
- FFmpeg (will prompt to install if not found)

For more information, visit the project repository.
EOF

# Create DMG using hdiutil
echo "Creating DMG..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DMG}" -ov -format UDZO "${DMG_NAME}.dmg"

# Clean up
rm -rf "${TEMP_DMG}"

# Rename with version
mv "${DMG_NAME}.dmg" "${DMG_FILE}"

echo ""
echo "=========================================="
echo "DMG created successfully!"
echo "=========================================="
echo ""
echo "DMG file: ${DMG_FILE}"
echo ""
echo "To test the DMG:"
echo "  open ${DMG_FILE}"
echo ""

