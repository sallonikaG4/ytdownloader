# YouTube to MP3 Downloader - Desktop Application

A complete Windows desktop application for downloading YouTube videos and playlists as MP3 files.

## 🚀 Quick Start

### For End Users

1. **Download the Installer**
   - Get `YouTubeToMP3_Setup.exe` from the releases

2. **Run the Installer**
   - Double-click the installer
   - Follow the installation wizard
   - The application will be installed to `C:\Program Files\YouTube to MP3 Downloader`

3. **Install FFmpeg** (Required)
   - The installer will guide you, or install manually:
   - **Option 1**: `winget install Gyan.FFmpeg`
   - **Option 2**: `choco install ffmpeg`
   - **Option 3**: Download from https://www.gyan.dev/ffmpeg/builds/

4. **Launch the Application**
   - Find "YouTube to MP3 Downloader" in Start Menu
   - Or use the Desktop shortcut
   - The application opens in a native window (no browser needed!)

## ✨ Features

- 🖥️ **Native Windows Application** - No browser required
- 🎵 **Download Single Videos** - Convert any YouTube video to MP3
- 📁 **Download Playlists** - Download entire playlists with automatic organization
- ✅ **Select Videos** - Choose which videos to download from playlists
- 🎚️ **Customizable Quality** - Choose from 128kbps to 320kbps (default: 172kbps)
- 📊 **Real-time Progress** - Live download progress with speed and ETA
- 🚫 **Auto-Skip Unavailable** - Automatically skips blocked/unavailable videos
- 🎨 **Modern UI** - Beautiful, responsive interface

## 📋 System Requirements

- **Windows 10/11** (64-bit)
- **FFmpeg** (installed separately - see above)
- **Internet Connection**

## 🛠️ For Developers

### Building from Source

1. **Install Prerequisites:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Icon:**
   ```bash
   python create_icon.py
   ```

3. **Build Executable:**
   ```bash
   pyinstaller youtube_downloader.spec
   ```

4. **Create Installer** (requires Inno Setup):
   ```bash
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
   ```

Or simply run:
```bash
build.bat
```

### Project Structure

```
.
├── desktop_app.py          # Desktop application wrapper (PyQt5)
├── app.py                  # Flask web application
├── youtube_downloader.py    # Core downloader logic
├── templates/              # HTML templates
├── static/                 # CSS and JavaScript
├── icon.ico                # Application icon
├── youtube_downloader.spec # PyInstaller configuration
├── build_installer.iss     # Inno Setup installer script
└── build.bat               # Automated build script
```

## 🎯 Usage

1. **Launch the Application**
   - The app opens in a native window
   - No browser or localhost URL needed

2. **Download a Video:**
   - Paste a YouTube URL
   - Click "Get Info" to preview
   - Click "Download & Convert"
   - Watch the progress in real-time

3. **Download a Playlist:**
   - Paste a playlist URL
   - Select which videos you want
   - Use "Select All" or "Deselect All" for quick selection
   - Click "Download & Convert"

4. **Access Downloads:**
   - View all downloaded files in the "Downloaded Files" section
   - Click "Download" to save files to your computer

5. **Exit:**
   - Click the "Exit" button in the top-right corner
   - Or close the window normally

## 🔧 Troubleshooting

### Application Won't Start
- Make sure FFmpeg is installed: `ffmpeg -version`
- Check Windows Event Viewer for error messages
- Try running from command line to see errors

### Downloads Fail
- Verify FFmpeg is in your system PATH
- Check your internet connection
- Some videos may be region-restricted

### Icon Not Showing
- The icon should appear automatically
- If not, it's a cosmetic issue and doesn't affect functionality

## 📝 Notes

- The application runs a local web server (Flask) internally
- All processing happens locally on your computer
- No data is sent to external servers (except YouTube for downloading)
- Downloads are saved to the `downloads` folder by default

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main README.md
3. Check INSTALLER_GUIDE.md for build issues

## 📄 License

This project is provided as-is for personal use.

---

**Enjoy your music! 🎵**


