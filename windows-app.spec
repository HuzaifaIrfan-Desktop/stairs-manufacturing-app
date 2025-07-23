# -*- mode: python ; coding: utf-8 -*-
import glob
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

import shutil
import os
import sys
import site

src = os.path.join('drawing_templates')
dst = os.path.join('dist', 'drawing_templates')
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)

# ocp_dir = r"C:\Users\admi\miniforge3\envs\stairs_app_env\Lib\site-packages\OCC"

# Find the site-packages directory of the current environment
site_packages = next(p for p in site.getsitepackages() if 'site-packages' in p)
ocp_dir = os.path.join(site_packages, 'OCC')

print("Collecting OCC binaries from:", ocp_dir)

ocp_binaries = [(f, os.path.join('OCC', os.path.basename(f))) for f in glob.glob(os.path.join(ocp_dir, "*.pyd"))]


a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[*ocp_binaries],
    datas=[('drawing_templates', 'drawing_templates')],
    hiddenimports=[*collect_submodules('OCP')],
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


