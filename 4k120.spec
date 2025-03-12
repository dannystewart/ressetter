from __future__ import annotations

import sys

a = Analysis(
    ["src/py4k120/main.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=["psutil"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

# Check if --background or -b is in sys.argv
background_mode = any(arg in sys.argv for arg in ["--background", "-b"])

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="4K120",
    icon="4K120.ico",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=background_mode,
    onefile=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
