# -*- mode: python ; coding: utf-8 -*-
import glob
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

import shutil
import os
import sys
import site



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
    [],
    exclude_binaries=True,
    name='stairs_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='favicon.ico',
    version='version.txt',
)


dir_name='stairs_app-v_0_1_2'

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=dir_name,
)


src = os.path.join('assets')
dst = os.path.join('dist',dir_name, 'assets')
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)


src = os.path.join('drawing_templates')
dst = os.path.join('dist',dir_name, 'drawing_templates')
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)

print("Copied required folders to:", dst)