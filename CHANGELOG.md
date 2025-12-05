# Changelog

## [2.0.0] - 2024-12-04

### Added
- **Windows Desktop Application**: Complete standalone Windows application with native window
- **Windows Installer**: Professional installer using Inno Setup
- **PyInstaller Integration**: Application packaged as single executable with all dependencies
- **Native WebView**: Uses PyQt5 WebEngine for native Windows experience (no browser needed)
- **Application Icon**: Custom icon for the executable
- **Exit Button**: Easy exit functionality in desktop mode
- **Silent Operation**: No localhost URL visible, runs as native application

### Technical Changes
- Added `desktop_app.py` - Desktop application wrapper using PyQt5
- Created PyInstaller spec file for building executable
- Created Inno Setup installer script
- Updated Flask app to work in bundled mode (PyInstaller)
- Added build automation script (`build.bat`)
- Icon creation script for application icon

### Installation
- Users can now install via Windows installer
- All Python dependencies bundled in executable
- FFmpeg must be installed separately (auto-detected)

## [1.1.0] - 2024-12-04

### Added
- **Playlist Selection Feature**: Select/deselect individual videos from playlists before downloading
- **Select All / Deselect All**: Quick selection controls for playlists
- **FFmpeg Auto-Detection**: Automatic detection of FFmpeg installation in common locations
- **Better FFmpeg Error Handling**: Clear error messages when FFmpeg is not found with helpful instructions
- **Unavailable Video Handling**: Automatically excludes unavailable/blocked videos from playlists
- **Visual Indicators**: Unavailable videos are shown with red badges and grayed out styling
- **Smart Selection**: Only available videos are selected by default

### Improved
- Enhanced playlist UI with checkbox selection interface
- Visual feedback for selected playlist items
- Selected count display showing how many videos are selected
- Better error messages for FFmpeg-related issues
- Download process continues even if some videos in a playlist are unavailable
- Unavailable videos are automatically skipped during download

### Technical Changes
- Added `find_ffmpeg()` function for automatic FFmpeg path detection
- Support for selective playlist downloads using yt-dlp's `playlist_items` option
- FFmpeg path configuration in yt-dlp options
- Playlist items now include index information for selection

## [1.0.0] - 2024-12-04

### Added
- YouTube video downloader with MP3 conversion at 172kbps (customizable)
- Support for downloading entire playlists with automatic folder organization
- Modern web-based user interface with real-time progress tracking
- Command-line interface for advanced users
- Real-time download progress with speed and ETA display
- Video/playlist information preview before downloading
- File browser to view and download converted MP3 files
- Customizable audio quality (128kbps to 320kbps)
- Customizable output directory
- Responsive design supporting desktop, tablet, and mobile devices
- Dark theme with modern, tech-savvy UI design

### Technical Details
- Backend: Flask web framework with RESTful API
- Frontend: Modern HTML5, CSS3, and JavaScript
- Download Engine: yt-dlp (latest version)
- Audio Conversion: FFmpeg integration
- Real-time Updates: WebSocket-like polling for progress updates
- Thread-safe download operations

### Dependencies
- Flask 3.1.2+
- Flask-CORS 6.0.1+
- yt-dlp 2025.11.12+
- FFmpeg (system dependency)

