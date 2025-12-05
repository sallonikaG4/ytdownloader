# Quick Start Guide - macOS

## For End Users

### Installation
1. Download `YouTubeToMP3_macOS_v*.dmg`
2. Open the DMG and drag the app to Applications
3. Launch from Applications
4. Select your downloads folder when prompted
5. Start downloading!

## For Developers

### Quick Build
```bash
cd MACOS
pip3 install -r requirements.txt
./install_ffmpeg.sh  # If FFmpeg not installed
./build_macos.sh
open dist/YouTubeToMP3.app
```

### Create DMG
```bash
./create_dmg.sh
```

That's it! 🎉

## Requirements Checklist
- [ ] macOS 10.13+
- [ ] Python 3.8+
- [ ] FFmpeg (via `./install_ffmpeg.sh` or `brew install ffmpeg`)
- [ ] All Python packages (`pip3 install -r requirements.txt`)

## Common Issues

**"FFmpeg not found"**
→ Run `./install_ffmpeg.sh` or `brew install ffmpeg`

**"App won't open"**
→ System Preferences > Security & Privacy > Open Anyway

**"Build fails"**
→ Make sure all dependencies are installed: `pip3 install -r requirements.txt --upgrade`

