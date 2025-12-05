# Windows Installer Guide

This guide explains how to create a complete Windows installer for the YouTube to MP3 Downloader application.

## Prerequisites

1. **Python 3.7+** - Already installed
2. **PyInstaller** - Will be installed automatically
3. **Inno Setup** (Optional, for creating installer) - Download from [jrsoftware.org](https://jrsoftware.org/isinfo.php)

## Building the Application

### Quick Build

Simply run:
```bash
build.bat
```

This will:
1. Install all dependencies
2. Create the application icon
3. Build the executable using PyInstaller
4. Create an installer (if Inno Setup is installed)

### Manual Build Steps

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Icon:**
   ```bash
   python create_icon.py
   ```
   (Or replace `icon.ico` with your own icon file)

3. **Build Executable:**
   ```bash
   pyinstaller youtube_downloader.spec
   ```

4. **Create Installer (Optional):**
   - Install Inno Setup from https://jrsoftware.org/isinfo.php
   - Run: `"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss`
   - Or use the Inno Setup Compiler GUI

## What Gets Installed

The installer includes:
- ✅ The application executable (bundled with Python runtime)
- ✅ Application icon
- ✅ All required Python libraries
- ⚠️ **FFmpeg** - Must be installed separately (see below)

## FFmpeg Installation

FFmpeg is not bundled with the installer. Users need to install it separately:

### Option 1: Automatic (Recommended)
The application will try to detect FFmpeg automatically. If not found, users can:
- Install via Chocolatey: `choco install ffmpeg`
- Install via winget: `winget install Gyan.FFmpeg`
- Download from: https://www.gyan.dev/ffmpeg/builds/

### Option 2: Bundle FFmpeg (Advanced)
To bundle FFmpeg with the installer:
1. Download FFmpeg static build
2. Extract to a `ffmpeg` folder
3. Update `build_installer.iss` to include FFmpeg files
4. Update the application to use bundled FFmpeg path

## Output Files

After building:
- **Executable**: `dist\YouTubeToMP3.exe` - Standalone executable
- **Installer**: `dist\YouTubeToMP3_Setup.exe` - Windows installer (if Inno Setup is used)

## Distribution

The installer (`YouTubeToMP3_Setup.exe`) can be distributed to users. They simply:
1. Run the installer
2. Follow the installation wizard
3. Launch the application from Start Menu or Desktop shortcut

## Troubleshooting

### PyInstaller Issues
- Make sure all dependencies are installed
- Try: `pip install --upgrade pyinstaller`

### Icon Not Showing
- Ensure `icon.ico` exists in the project root
- Icon should be in ICO format with multiple sizes (16x16, 32x32, 48x48, 256x256)

### Inno Setup Not Found
- Install Inno Setup from https://jrsoftware.org/isinfo.php
- Or manually compile the installer using the GUI

### Application Won't Start
- Check if FFmpeg is installed and in PATH
- Run from command line to see error messages
- Check Windows Event Viewer for errors

## Advanced: Custom Installer

To customize the installer:
1. Edit `build_installer.iss`
2. Add custom installation steps
3. Include additional files
4. Modify registry entries if needed

For more information, see Inno Setup documentation: https://jrsoftware.org/ishelp/


