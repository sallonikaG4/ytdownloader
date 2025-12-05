# FFmpeg Installation Guide

FFmpeg is required for converting YouTube videos to MP3 format. Follow these instructions to install it on Windows.

## Option 1: Using Chocolatey (Recommended)

If you have Chocolatey package manager installed:

```powershell
choco install ffmpeg
```

After installation, restart your terminal/PowerShell.

## Option 2: Manual Installation

1. **Download FFmpeg:**
   - Visit: https://www.gyan.dev/ffmpeg/builds/
   - Download the "ffmpeg-release-essentials.zip" file

2. **Extract the files:**
   - Extract the ZIP file to a location like `C:\ffmpeg`

3. **Add to PATH:**
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin` (or wherever you extracted FFmpeg)
   - Click "OK" on all dialogs

4. **Verify installation:**
   - Open a new PowerShell/Command Prompt window
   - Run: `ffmpeg -version`
   - You should see version information

## Option 3: Using winget (Windows 10/11)

```powershell
winget install ffmpeg
```

## Verify Installation

After installation, verify FFmpeg is working:

```bash
ffmpeg -version
```

You should see output showing the FFmpeg version and build information.

## Troubleshooting

- **"ffmpeg is not recognized"**: Make sure you've added FFmpeg to your PATH and restarted your terminal
- **Permission errors**: Run your terminal as Administrator if needed
- **Still not working**: Try restarting your computer after adding to PATH

Once FFmpeg is installed, you can use the YouTube to MP3 downloader!


