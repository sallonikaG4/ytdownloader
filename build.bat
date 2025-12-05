@echo off
echo ========================================
echo Building YouTube to MP3 Downloader
echo ========================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Step 2: Creating icon...
python create_icon.py
if errorlevel 1 (
    echo Warning: Icon creation failed, continuing anyway...
)

echo.
echo Step 3: Building executable with PyInstaller...
pyinstaller youtube_downloader.spec
if errorlevel 1 (
    echo Failed to build executable!
    pause
    exit /b 1
)

echo.
echo Step 4: Building installer (if Inno Setup is installed)...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
    if errorlevel 1 (
        echo Warning: Installer creation failed. Executable is in dist\ folder.
    ) else (
        echo Installer created successfully in dist\ folder!
    )
) else (
    echo Inno Setup not found. Skipping installer creation.
    echo Executable is available in dist\ folder.
    echo To create installer, install Inno Setup from: https://jrsoftware.org/isinfo.php
)

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Executable: dist\YouTubeToMP3.exe
if exist "dist\YouTubeToMP3_Setup.exe" (
    echo Installer: dist\YouTubeToMP3_Setup.exe
)
echo.
pause


