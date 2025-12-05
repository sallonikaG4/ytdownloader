# YouTube to MP3 Downloader

A modern, cross-platform desktop application for downloading YouTube videos and playlists and converting them to MP3 format at customizable quality (default: 172kbps). Available for **Windows** and **macOS**.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)

## 🎯 Purpose

This application was created to provide a **local, ad-free solution** for downloading YouTube content as MP3 files. Unlike browser-based solutions, this runs entirely on your computer with:

- ✅ **No ads or popups**
- ✅ **No browser required** (native desktop app)
- ✅ **No subscription fees**
- ✅ **Complete privacy** (all processing happens locally)
- ✅ **Playlist support** with selective downloading
- ✅ **Automatic handling** of unavailable/blocked videos

## ✨ Features

### Core Functionality
- 🎵 **Download Single Videos** - Convert any YouTube video to MP3
- 📁 **Download Entire Playlists** - Download complete playlists with automatic organization
- 🎯 **Selective Playlist Download** - Choose which videos to download from playlists
- 🚫 **Smart Filtering** - Automatically skips unavailable/blocked videos
- 🎚️ **Customizable Quality** - Choose from 128kbps to 320kbps (default: 172kbps)

### User Interface
- 🎨 **Modern, Tech-Savvy UI** - Beautiful dark theme with gradient accents
- 📊 **Real-time Progress** - Live download progress with speed and ETA
- 📂 **File Management** - Browse and access all downloaded files
- 🖥️ **Native Desktop App** - No browser needed (Windows & macOS)
- 📱 **Responsive Design** - Works on all screen sizes

### Technical Features
- 🚀 **Fast & Efficient** - Powered by yt-dlp and FFmpeg
- 🔒 **Privacy-First** - All processing happens locally
- 💾 **Persistent Settings** - Remembers your downloads folder preference
- 🔄 **Auto-Installation** - Windows installer includes FFmpeg setup
- 🎯 **Error Handling** - Graceful handling of unavailable content

## 📦 Installation

### Windows

#### Option 1: Installer (Recommended)
1. Download `YouTubeToMP3_Setup.exe` from the [Releases](https://github.com/sallonikaG4/ytdownloader/releases) page
2. Run the installer
3. Follow the installation wizard
4. The installer will automatically set up FFmpeg if needed
5. Launch from Start Menu or desktop shortcut

#### Option 2: Build from Source
See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed instructions.

### macOS

#### Option 1: DMG Installer (Recommended)
1. Download `YouTubeToMP3_macOS_v*.dmg` from the [Releases](https://github.com/sallonikaG4/ytdownloader/releases) page
2. Open the DMG file
3. Drag `YouTubeToMP3.app` to your Applications folder
4. Launch from Applications
5. If you see a security warning, go to **System Preferences** > **Security & Privacy** > **Open Anyway**

#### Option 2: Build from Source
See [MACOS/BUILD_INSTRUCTIONS_MACOS.md](MACOS/BUILD_INSTRUCTIONS_MACOS.md) for detailed instructions.

### Prerequisites (For Building from Source)

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **FFmpeg** - Required for audio conversion
  - **Windows**: Included in installer, or download from [FFmpeg.org](https://ffmpeg.org/download.html)
  - **macOS**: `brew install ffmpeg` or use `MACOS/install_ffmpeg.sh`
  - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)

## 🚀 Usage

### Desktop Application (Windows & macOS)

1. **Launch the application**
   - **Windows**: From Start Menu or desktop shortcut
   - **macOS**: From Applications folder

2. **Select Downloads Folder** (First Launch)
   - Choose where you want downloaded files saved
   - Your choice will be remembered for future sessions

3. **Download a Video**
   - Paste a YouTube video URL in the input field
   - Click **"Get Info"** to preview the video
   - Adjust quality settings if needed (default: 172kbps)
   - Click **"Download & Convert"**
   - Watch real-time progress

4. **Download a Playlist**
   - Paste a YouTube playlist URL
   - Click **"Get Info"** to see all videos
   - **Select which videos** you want to download (use "Select All" or "Deselect All")
   - Unavailable/blocked videos are automatically excluded
   - Click **"Download & Convert"**

5. **Access Downloaded Files**
   - All downloaded MP3 files appear in the "Downloaded Files" section
   - Click "Download" to save a file to your default Downloads folder
   - Files are organized by playlist name (for playlists)

### Command Line Interface (Advanced)

For command-line usage:

```bash
# Download a single video
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Download a playlist
python youtube_downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Custom output directory
python youtube_downloader.py "URL" --output "my_music"

# Custom bitrate
python youtube_downloader.py "URL" --bitrate "192k"
```

## 📁 Output Structure

- **Single Videos**: Saved directly to your chosen downloads folder
- **Playlists**: Organized in subfolders by playlist name, with tracks numbered:
  ```
  Downloads/YouTube Downloads/
  ├── My Playlist Name/
  │   ├── 1 - Song Title.mp3
  │   ├── 2 - Another Song.mp3
  │   └── ...
  └── Single Video Title.mp3
  ```

## ⚙️ Configuration

### Default Settings
- **Bitrate**: 172kbps
- **Output Directory**: 
  - Windows: `Documents/YouTube Downloads`
  - macOS: `Downloads/YouTube Downloads`
- **Format**: MP3

### Available Bitrates
- 128kbps
- 172kbps (default)
- 192kbps
- 256kbps
- 320kbps

## 🎨 Features in Detail

### Playlist Selection
- View all videos in a playlist before downloading
- Select individual videos with checkboxes
- "Select All" / "Deselect All" buttons for convenience
- Unavailable videos are marked and automatically excluded
- See how many videos are selected

### Progress Tracking
- Real-time download percentage
- Current download speed (KB/s or MB/s)
- Estimated time remaining (ETA)
- Status updates (downloading, converting, etc.)

### File Management
- Browse all downloaded MP3 files
- See file paths and organization
- Download files directly from the app
- Files sorted by modification date (newest first)

## 🔧 Troubleshooting

### FFmpeg Not Found (Windows)
- The installer should set up FFmpeg automatically
- If not, download from [FFmpeg.org](https://ffmpeg.org/download.html)
- Add FFmpeg to your system PATH
- Restart the application

### FFmpeg Not Found (macOS)
```bash
brew install ffmpeg
```
Or use the installation script:
```bash
cd MACOS
./install_ffmpeg.sh
```

### Application Won't Open (macOS)
1. Go to **System Preferences** > **Security & Privacy**
2. Click **"Open Anyway"** next to the warning message
3. Or right-click the app and select **Open**

### Download Fails
- Check your internet connection
- Verify the YouTube URL is correct
- Some videos may be region-restricted or unavailable (these are automatically skipped)

### Conversion Issues
- Ensure FFmpeg is properly installed
- Check that you have write permissions in the downloads folder
- Try selecting a different downloads folder

### Build Errors
- Make sure Python 3.8+ is installed
- Install all dependencies: `pip install -r requirements.txt`
- Check platform-specific build instructions

## 🏗️ Project Structure

```
.
├── youtube_downloader.py      # Core download logic
├── app.py                      # Flask web server
├── desktop_app.py             # Desktop application wrapper
├── templates/                 # HTML templates
├── static/                    # CSS and JavaScript
├── MACOS/                     # macOS-specific files
│   ├── youtube_downloader.py  # macOS version
│   ├── build_macos.sh         # macOS build script
│   └── ...
├── requirements.txt           # Python dependencies
├── BUILD_INSTRUCTIONS.md      # Windows build guide
└── README.md                  # This file
```

## 🛠️ Development

### Running in Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py

# Or run desktop app
python desktop_app.py
```

Then open http://localhost:5000 in your browser (if using Flask directly).

### Building for Distribution

- **Windows**: See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
- **macOS**: See [MACOS/BUILD_INSTRUCTIONS_MACOS.md](MACOS/BUILD_INSTRUCTIONS_MACOS.md)

## 📝 Technical Details

### Technologies Used
- **Python 3.8+** - Core language
- **yt-dlp** - YouTube downloading engine
- **FFmpeg** - Audio conversion
- **Flask** - Web framework (for UI)
- **PyQt5** - Desktop application framework
- **PyInstaller** - Application bundling

### Architecture
- **Backend**: Flask REST API serving the web UI
- **Frontend**: Modern HTML/CSS/JavaScript
- **Desktop Wrapper**: PyQt5 WebEngine (embeds web UI in native window)
- **Download Engine**: yt-dlp with FFmpeg post-processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🛡️ Legal Notice

This tool is for **personal use only**. Please respect:
- YouTube's Terms of Service
- Copyright laws
- Content creators' rights

**Only download content you have permission to download.**

## 📄 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **yt-dlp** - [GitHub](https://github.com/yt-dlp/yt-dlp) - YouTube downloading engine
- **FFmpeg** - [FFmpeg.org](https://ffmpeg.org/) - Audio/video processing
- **Flask** - [Flask.palletsprojects.com](https://flask.palletsprojects.com/) - Web framework
- **PyQt5** - [Riverbank Computing](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- **Inter Font** - [Google Fonts](https://fonts.google.com/specimen/Inter) - Typography

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sallonikaG4/ytdownloader/issues)
- **Releases**: [GitHub Releases](https://github.com/sallonikaG4/ytdownloader/releases)

## 🎉 Acknowledgments

Special thanks to all the open-source projects that make this application possible.

---

**Made with ❤️ for music lovers who want a simple, ad-free way to enjoy YouTube content offline.**

**Enjoy your music! 🎵**
