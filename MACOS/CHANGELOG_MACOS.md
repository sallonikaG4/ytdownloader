# Changelog - macOS Version

## Version 2.0.0 (Initial macOS Release)

### Features
- ✅ Full macOS compatibility
- ✅ Native .app bundle with proper macOS structure
- ✅ macOS-specific FFmpeg detection (Homebrew paths, /usr/local/bin, etc.)
- ✅ Default downloads folder: ~/Downloads/YouTube Downloads
- ✅ Folder selection dialog on startup (persisted with QSettings)
- ✅ Playlist selection with select/deselect all
- ✅ Automatic skipping of unavailable/blocked videos
- ✅ Modern, tech-savvy UI
- ✅ Real-time download progress
- ✅ DMG installer creation script

### Technical Changes
- Updated `find_ffmpeg()` to check macOS-specific paths:
  - `/usr/local/bin/ffmpeg` (Homebrew Intel)
  - `/opt/homebrew/bin/ffmpeg` (Homebrew Apple Silicon)
  - `/usr/bin/ffmpeg` (system)
  - `~/ffmpeg/bin/ffmpeg` (user installation)
- Updated `get_default_downloads_dir()` to use `~/Downloads/YouTube Downloads` on macOS
- Updated `desktop_app.py` to handle `.icns` icon format
- Created macOS-specific PyInstaller spec with proper .app bundle structure
- Added build scripts for macOS (`build_macos.sh`)
- Added FFmpeg installation script (`install_ffmpeg.sh`)
- Added DMG creation script (`create_dmg.sh`)

### Build System
- PyInstaller spec configured for macOS .app bundle
- Icon support for .icns format
- Proper Info.plist configuration
- Bundle identifier: `com.techsolutions.youtubetomp3`

### Documentation
- Created `README_MACOS.md` with installation and usage instructions
- Created `BUILD_INSTRUCTIONS_MACOS.md` with detailed build steps
- Created this changelog

### Known Issues
- None at this time

### Future Enhancements
- Code signing support
- Notarization support for Gatekeeper
- Universal binary (Intel + Apple Silicon)
- Auto-update mechanism

