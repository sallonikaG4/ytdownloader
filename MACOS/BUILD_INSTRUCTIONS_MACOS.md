# Build Instructions for macOS

This guide explains how to build the YouTube to MP3 Downloader application for macOS.

## Prerequisites

1. **macOS 10.13 or later**
2. **Python 3.8+** - Install from [python.org](https://www.python.org/downloads/) or via Homebrew:
   ```bash
   brew install python3
   ```
3. **Xcode Command Line Tools** (usually installed with Python):
   ```bash
   xcode-select --install
   ```

## Step 1: Install Dependencies

```bash
cd MACOS
pip3 install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (CORS support)
- yt-dlp (YouTube downloader)
- PyQt5 (GUI framework)
- PyQtWebEngine (web view)
- PyInstaller (app bundler)
- Pillow (image processing)

## Step 2: Install FFmpeg

FFmpeg is required for audio conversion. Install it via Homebrew:

```bash
./install_ffmpeg.sh
```

Or manually:
```bash
brew install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

## Step 3: Prepare Icon (Optional)

The application needs an `icon.icns` file. If you have `icon.ico`, the build script will attempt to convert it. Otherwise:

1. Create an icon in PNG format (512x512 or larger)
2. Use `iconutil` to create the ICNS:
   ```bash
   mkdir icon.iconset
   # Copy your PNG files to icon.iconset with proper naming
   # icon_16x16.png, icon_16x16@2x.png, etc.
   iconutil -c icns icon.iconset
   ```

Or use an online converter to convert ICO to ICNS.

## Step 4: Build the Application

Make the build script executable and run it:

```bash
chmod +x build_macos.sh
./build_macos.sh
```

This will:
1. Install/upgrade Python dependencies
2. Convert icon if needed
3. Clean previous builds
4. Build the application with PyInstaller
5. Create `dist/YouTubeToMP3.app`

## Step 5: Test the Application

```bash
open dist/YouTubeToMP3.app
```

If you see a security warning:
1. Go to **System Preferences** > **Security & Privacy**
2. Click **"Open Anyway"**

## Step 6: Create DMG Installer (Optional)

To create a distributable DMG file:

```bash
chmod +x create_dmg.sh
./create_dmg.sh
```

This creates `YouTubeToMP3_macOS_v2.0.0.dmg` in the current directory.

## Manual Build (Alternative)

If you prefer to build manually:

```bash
# Clean previous builds
rm -rf build dist *.app

# Build with PyInstaller
pyinstaller youtube_downloader_macos.spec --clean

# Test
open dist/YouTubeToMP3.app
```

## Troubleshooting

### Build Fails with "Module not found"

Make sure all dependencies are installed:
```bash
pip3 install -r requirements.txt --upgrade
```

### PyInstaller Errors

Try cleaning and rebuilding:
```bash
rm -rf build dist __pycache__
pyinstaller youtube_downloader_macos.spec --clean
```

### Icon Not Found

The build will work without an icon, but the app won't have a custom icon. Create `icon.icns` or the build script will attempt to convert `icon.ico`.

### FFmpeg Not Found

Install FFmpeg:
```bash
brew install ffmpeg
```

Or use the installation script:
```bash
./install_ffmpeg.sh
```

### App Won't Open

1. Check Console.app for error messages
2. Try running from terminal:
   ```bash
   dist/YouTubeToMP3.app/Contents/MacOS/YouTubeToMP3
   ```
3. Check System Preferences > Security & Privacy

## Code Signing (For Distribution)

If you have an Apple Developer account, you can code sign the app:

```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/YouTubeToMP3.app
```

## Notarization (For Gatekeeper)

For distribution, you may want to notarize the DMG:

1. Create DMG: `./create_dmg.sh`
2. Notarize with `xcrun notarytool` (requires Apple Developer account)
3. Staple the notarization: `xcrun stapler staple YouTubeToMP3_macOS_v*.dmg`

## File Sizes

After building, expect:
- `dist/YouTubeToMP3.app`: ~150-200 MB (includes Python, PyQt5, and all dependencies)
- DMG file: ~100-150 MB (compressed)

## Next Steps

- Test the application thoroughly
- Create a DMG for distribution
- Consider code signing and notarization for wider distribution
- Update version numbers in `youtube_downloader_macos.spec` and `create_dmg.sh`

