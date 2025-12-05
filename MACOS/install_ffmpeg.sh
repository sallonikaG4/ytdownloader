#!/bin/bash
# Install FFmpeg on macOS

set -e

echo "=========================================="
echo "FFmpeg Installation for macOS"
echo "=========================================="
echo ""

# Check if FFmpeg is already installed
if command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is already installed:"
    ffmpeg -version | head -n 1
    echo ""
    read -p "Do you want to reinstall? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed."
    echo ""
    echo "Homebrew is the recommended way to install FFmpeg on macOS."
    echo ""
    read -p "Do you want to install Homebrew now? (Y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo ""
        echo "You can install FFmpeg manually:"
        echo "1. Download from: https://ffmpeg.org/download.html"
        echo "2. Or install Homebrew and run: brew install ffmpeg"
        exit 1
    fi
    
    echo ""
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH (for Apple Silicon Macs)
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

echo ""
echo "Installing FFmpeg via Homebrew..."
brew install ffmpeg

echo ""
echo "=========================================="
echo "FFmpeg installation complete!"
echo "=========================================="
echo ""
echo "FFmpeg version:"
ffmpeg -version | head -n 1
echo ""
echo "FFmpeg is now available in your PATH."

