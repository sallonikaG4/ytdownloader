#!/bin/bash
# Build script for macOS YouTube to MP3 Downloader
# This script builds the macOS application using PyInstaller

# Don't exit on error immediately - we want to see what failed
set +e

echo "=========================================="
echo "Building YouTube to MP3 Downloader for macOS"
echo "=========================================="
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "ERROR: This script must be run on macOS"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    exit 1
fi

# Install/upgrade dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt --upgrade
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Check if icon exists
if [ ! -f "icon.icns" ]; then
    echo "WARNING: icon.icns not found. Creating from icon.ico if available..."
    if [ -f "icon.ico" ]; then
        echo "Converting icon.ico to icon.icns..."
        # Create temporary iconset directory
        mkdir -p icon.iconset
        # Convert ICO to PNG (requires ImageMagick or sips)
        if command -v sips &> /dev/null; then
            sips -s format png icon.ico --out icon.iconset/icon_512x512.png 2>/dev/null
            if [ $? -eq 0 ]; then
                # Create other sizes (macOS requires multiple sizes)
                sips -z 16 16 icon.iconset/icon_512x512.png --out icon.iconset/icon_16x16.png 2>/dev/null
                sips -z 32 32 icon.iconset/icon_512x512.png --out icon.iconset/icon_16x16@2x.png 2>/dev/null
                sips -z 32 32 icon.iconset/icon_512x512.png --out icon.iconset/icon_32x32.png 2>/dev/null
                sips -z 64 64 icon.iconset/icon_512x512.png --out icon.iconset/icon_32x32@2x.png 2>/dev/null
                sips -z 128 128 icon.iconset/icon_512x512.png --out icon.iconset/icon_128x128.png 2>/dev/null
                sips -z 256 256 icon.iconset/icon_512x512.png --out icon.iconset/icon_128x128@2x.png 2>/dev/null
                sips -z 256 256 icon.iconset/icon_512x512.png --out icon.iconset/icon_256x256.png 2>/dev/null
                sips -z 512 512 icon.iconset/icon_512x512.png --out icon.iconset/icon_256x256@2x.png 2>/dev/null
                sips -z 512 512 icon.iconset/icon_512x512.png --out icon.iconset/icon_512x512.png 2>/dev/null
                sips -z 1024 1024 icon.iconset/icon_512x512.png --out icon.iconset/icon_512x512@2x.png 2>/dev/null
                # Create ICNS
                iconutil -c icns icon.iconset -o icon.icns 2>/dev/null
                if [ -f "icon.icns" ]; then
                    rm -rf icon.iconset
                    echo "Icon created successfully!"
                else
                    echo "WARNING: Failed to create icon.icns. Building without icon..."
                    rm -rf icon.iconset
                fi
            else
                echo "WARNING: Failed to convert icon.ico. Building without icon..."
                rm -rf icon.iconset
            fi
        else
            echo "WARNING: sips not found. Building without icon..."
        fi
    else
        echo "WARNING: Neither icon.icns nor icon.ico found. Building without icon..."
    fi
fi

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf build dist *.app

# Build with PyInstaller
echo ""
echo "Building application with PyInstaller..."
pyinstaller youtube_downloader_macos.spec --clean
BUILD_EXIT_CODE=$?
if [ $BUILD_EXIT_CODE -ne 0 ]; then
    echo "ERROR: PyInstaller build failed with exit code $BUILD_EXIT_CODE"
    echo "Check the output above for details"
    exit 1
fi

# Check if build was successful
if [ -d "dist/YouTubeToMP3.app" ]; then
    echo ""
    echo "=========================================="
    echo "Build successful!"
    echo "=========================================="
    echo ""
    echo "Application bundle: dist/YouTubeToMP3.app"
    echo ""
    echo "To test the application:"
    echo "  open dist/YouTubeToMP3.app"
    echo ""
    echo "To create a DMG installer, run:"
    echo "  ./create_dmg.sh"
    echo ""
else
    echo ""
    echo "ERROR: Build failed. Application bundle not found."
    exit 1
fi

