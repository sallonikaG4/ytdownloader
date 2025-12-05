# Build Instructions - YouTube to MP3 Downloader

Complete guide to building the Windows desktop application and installer.

## Prerequisites

1. **Python 3.7+** - Already installed ✓
2. **All Python Dependencies** - Will be installed automatically
3. **Inno Setup** (Optional) - For creating the installer
   - Download from: https://jrsoftware.org/isinfo.php
   - Free and open-source

## Quick Build

Simply run:
```bash
build.bat
```

This automated script will:
1. ✅ Install all Python dependencies
2. ✅ Create the application icon
3. ✅ Build the executable using PyInstaller
4. ✅ Create the installer (if Inno Setup is installed)

## Manual Build Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask & Flask-CORS (web framework)
- yt-dlp (YouTube downloader)
- PyQt5 & PyQtWebEngine (desktop app framework)
- PyInstaller (packaging tool)
- Pillow (icon creation)

### Step 2: Create Icon

```bash
python create_icon.py
```

This creates `icon.ico` with multiple sizes. You can replace this with your own icon file if desired.

### Step 3: Build Executable

```bash
pyinstaller youtube_downloader.spec
```

This creates:
- `dist/YouTubeToMP3.exe` - Standalone executable (all dependencies included)

**Note:** The first build may take several minutes as PyInstaller bundles Python and all libraries.

### Step 4: Create Installer (Optional)

If you have Inno Setup installed:

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
```

This creates:
- `dist/YouTubeToMP3_Setup.exe` - Windows installer

## Testing the Application

### Test Desktop App (Before Building)

```bash
python desktop_app.py
```

This should:
- Open a native window (not browser)
- Show the YouTube downloader interface
- Have an Exit button in the top-right

### Test Executable (After Building)

1. Navigate to `dist` folder
2. Double-click `YouTubeToMP3.exe`
3. The application should launch in a native window

## Output Files

After building:

```
dist/
├── YouTubeToMP3.exe              # Standalone executable
└── YouTubeToMP3_Setup.exe        # Windows installer (if Inno Setup used)
```

## Distribution

### For End Users

Distribute `YouTubeToMP3_Setup.exe`. Users simply:
1. Run the installer
2. Follow the wizard
3. Launch from Start Menu

### Standalone Executable

You can also distribute `YouTubeToMP3.exe` directly:
- No installation needed
- Just double-click to run
- All dependencies included

## Troubleshooting

### PyInstaller Errors

**Error: "Module not found"**
- Solution: Add missing module to `hiddenimports` in `youtube_downloader.spec`

**Error: "Template/static files not found"**
- Solution: Check that `datas` in spec file includes templates and static folders

**Large executable size**
- Normal: PyInstaller bundles Python runtime (~50-100MB)
- Can be reduced with UPX compression (already enabled)

### Inno Setup Errors

**Error: "ISCC.exe not found"**
- Solution: Install Inno Setup or update path in `build.bat`

**Error: "Icon file not found"**
- Solution: Make sure `icon.ico` exists in project root

### Application Won't Start

**Error: "FFmpeg not found"**
- Solution: Application will show error message
- Users need to install FFmpeg separately

**Error: "Port 5000 already in use"**
- Solution: Close other instances of the app
- Or modify port in `desktop_app.py`

## Advanced Configuration

### Custom Icon

Replace `icon.ico` with your own:
- Format: ICO file
- Sizes: 16x16, 32x32, 48x48, 256x256 (recommended)
- Tools: Use online ICO converters or GIMP

### Custom Installer

Edit `build_installer.iss` to:
- Change application name/version
- Add custom installation steps
- Include additional files
- Modify registry entries

### Bundle FFmpeg

To include FFmpeg in the installer:
1. Download FFmpeg static build
2. Extract to `ffmpeg` folder
3. Update `build_installer.iss` to include FFmpeg files
4. Update `youtube_downloader.py` to check bundled FFmpeg first

## File Sizes

Expected sizes:
- **Executable**: ~80-120 MB (includes Python + all libraries)
- **Installer**: ~90-130 MB (executable + installer overhead)

## Build Time

- First build: 5-10 minutes (downloads dependencies)
- Subsequent builds: 2-5 minutes (incremental)

## Next Steps

1. ✅ Build the application
2. ✅ Test the executable
3. ✅ Create installer
4. ✅ Distribute to users

For more details, see:
- `INSTALLER_GUIDE.md` - Detailed installer information
- `README_DESKTOP.md` - End-user documentation
- `README.md` - General project information

---

**Happy Building! 🚀**


