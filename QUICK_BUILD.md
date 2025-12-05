# Quick Build Guide

## The Problem

The Inno Setup installer is looking for `dist\YouTubeToMP3.exe`, but it doesn't exist yet because PyInstaller hasn't built it.

## Solution: Build in Order

You must build the executable **BEFORE** creating the installer.

### Step 1: Build the Executable

```bash
pyinstaller youtube_downloader.spec
```

**This will take 5-10 minutes** (especially the first time). Be patient!

The build process will:
- Analyze all dependencies
- Bundle Python runtime
- Include templates and static files
- Create the executable

**Output:** `dist\YouTubeToMP3.exe`

### Step 2: Create the Installer

Once the executable exists, you can create the installer:

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
```

**Output:** `dist\YouTubeToMP3_Setup.exe`

## Automated Build

Or use the automated script (does everything in order):

```bash
build.bat
```

This script:
1. Installs dependencies
2. Creates icon
3. Builds executable (Step 1)
4. Creates installer (Step 2)

## Troubleshooting

### "Executable not found" Error

**Cause:** You tried to create the installer before building the executable.

**Solution:** Run `pyinstaller youtube_downloader.spec` first, wait for it to complete.

### Build Takes Too Long

**Normal!** PyInstaller needs to:
- Bundle Python (~50MB)
- Include all libraries (PyQt5, Flask, yt-dlp, etc.)
- Process all files

**First build:** 5-10 minutes
**Subsequent builds:** 2-5 minutes

### Build Fails

Common issues:
- Missing dependencies: `pip install -r requirements.txt`
- PyQt5 not found: `pip install PyQt5 PyQtWebEngine`
- Icon missing: `python create_icon.py`

## Expected File Sizes

- **Executable:** ~80-120 MB (includes everything)
- **Installer:** ~90-130 MB (executable + installer overhead)

## Verification

After building, check:

```bash
# Check if executable exists
Test-Path "dist\YouTubeToMP3.exe"

# Should return: True
```

Then you can create the installer!


