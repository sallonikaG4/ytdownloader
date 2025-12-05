# YouTube to MP3 Downloader - macOS Version

A modern, desktop application for downloading YouTube videos and playlists and converting them to MP3 at 172kbps quality.

## Features

- 🎵 Download single videos or entire playlists
- 🎯 Select specific videos from playlists
- 🎨 Modern, tech-savvy user interface
- 📁 Choose your downloads folder on startup
- ⚡ Real-time download progress
- 🚫 Automatically skips unavailable/blocked videos
- 🖥️ Native macOS application (no browser needed)

## Requirements

- macOS 10.13 (High Sierra) or later
- Python 3.8+ (for building from source)
- FFmpeg (will prompt to install if not found)

## Installation

### Option 1: Pre-built DMG (Recommended)

1. Download the latest `YouTubeToMP3_macOS_v*.dmg` file
2. Double-click the DMG to mount it
3. Drag `YouTubeToMP3.app` to your Applications folder
4. Open Applications and launch `YouTubeToMP3.app`
5. If you see a security warning:
   - Go to **System Preferences** > **Security & Privacy**
   - Click **"Open Anyway"** next to the warning message

### Option 2: Build from Source

1. **Clone or download this repository**
   ```bash
   cd MACOS
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Install FFmpeg** (if not already installed)
   ```bash
   ./install_ffmpeg.sh
   ```
   Or manually:
   ```bash
   brew install ffmpeg
   ```

4. **Create application icon** (optional)
   - Place `icon.icns` in the MACOS directory
   - Or the build script will attempt to convert `icon.ico` if available

5. **Build the application**
   ```bash
   chmod +x build_macos.sh
   ./build_macos.sh
   ```

6. **Test the application**
   ```bash
   open dist/YouTubeToMP3.app
   ```

7. **Create DMG installer** (optional)
   ```bash
   chmod +x create_dmg.sh
   ./create_dmg.sh
   ```

## Usage

1. **Launch the application**
   - Open `YouTubeToMP3.app` from Applications
   - On first launch, you'll be prompted to select a downloads folder

2. **Download a video**
   - Paste a YouTube video URL
   - Click "Get Info" to preview
   - Click "Download & Convert"

3. **Download a playlist**
   - Paste a YouTube playlist URL
   - Click "Get Info"
   - Select which videos you want to download
   - Use "Select All" or "Deselect All" for convenience
   - Click "Download & Convert"

4. **Access downloaded files**
   - Files are saved to your chosen downloads folder
   - The app shows all downloaded MP3 files in the "Downloaded Files" section
   - Click "Download" to save a file to your default Downloads folder

## Troubleshooting

### "FFmpeg not found" error

Install FFmpeg using Homebrew:
```bash
brew install ffmpeg
```

Or run the installation script:
```bash
./install_ffmpeg.sh
```

### Application won't open (Security Warning)

macOS may block the application if it's not signed. To allow it:

1. Go to **System Preferences** > **Security & Privacy**
2. Click **"Open Anyway"** next to the warning
3. Or right-click the app and select **Open**

### Build errors

- Make sure you're using Python 3.8 or later
- Ensure all dependencies are installed: `pip3 install -r requirements.txt`
- Check that PyInstaller is installed: `pip3 install pyinstaller`

### Downloads not appearing

- Check the downloads folder you selected on startup
- Make sure you have write permissions to that folder
- Try selecting a different folder (the app will remember your choice)

## Development

### Project Structure

```
MACOS/
├── youtube_downloader.py    # Core download logic
├── app.py                    # Flask web server
├── desktop_app.py           # PyQt5 desktop wrapper
├── templates/               # HTML templates
├── static/                  # CSS and JavaScript
├── requirements.txt         # Python dependencies
├── youtube_downloader_macos.spec  # PyInstaller spec
├── build_macos.sh           # Build script
├── install_ffmpeg.sh        # FFmpeg installer
└── create_dmg.sh            # DMG creator
```

### Running in Development Mode

```bash
# Terminal 1: Start Flask server
python3 app.py

# Terminal 2: Start desktop app (optional, or just use browser)
python3 desktop_app.py
```

Then open http://localhost:5000 in your browser.

## Code Signing (Optional)

For distribution outside the App Store, you may want to code sign the application:

```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/YouTubeToMP3.app
```

## Notarization (Optional)

For Gatekeeper compatibility, you can notarize the app:

```bash
# Create DMG first
./create_dmg.sh

# Notarize (requires Apple Developer account)
xcrun notarytool submit YouTubeToMP3_macOS_v*.dmg --apple-id your@email.com --team-id YOUR_TEAM_ID --password YOUR_APP_PASSWORD
```

## License

Copyright © 2025 WaLLe

## Support

For issues, questions, or contributions, please visit the project repository.

