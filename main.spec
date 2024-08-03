# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
options = [('W ignore', None, 'OPTION')]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/main_icon.png', 'src'), ('src/cross.png', 'src'), ('src/water.png', 'src'), ('src/hit.png', 'src'), ('src/dot.png', 'src'), ('src/pixel.png', 'src')],
    hiddenimports=['PIL', 'PIL._tkinter_finder'],
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
    name='sea-battle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/main_icon.png'],
)
