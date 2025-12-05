# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for macOS

import os

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
    ] + ([] if not os.path.exists('icon.icns') else [('icon.icns', '.')]),
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
        'flask',
        'flask_cors',
        'yt_dlp',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubeToMP3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.icns' if os.path.exists('icon.icns') else None,  # macOS uses .icns format
)

app = BUNDLE(
    exe,
    name='YouTubeToMP3.app',
    icon='icon.icns' if os.path.exists('icon.icns') else None,
    bundle_identifier='com.techsolutions.youtubetomp3',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '2.0.0',
        'CFBundleVersion': '2.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025 WaLLe',
    },
)

