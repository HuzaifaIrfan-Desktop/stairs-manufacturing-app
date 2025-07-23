# -*- mode: python ; coding: utf-8 -*-
import glob

import shutil
import os

src = os.path.join('drawing_templates')
dst = os.path.join('dist', 'drawing_templates')
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('drawing_templates', 'drawing_templates')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Stairs App',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='favicon.ico'  
)


