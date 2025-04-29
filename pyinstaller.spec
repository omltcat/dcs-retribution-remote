# -*- mode: python ; coding: utf-8 -*-

import shutil
from pathlib import Path

NAME = 'retribution_remote'

dist_dir = Path('dist')
if dist_dir.exists():
    shutil.rmtree(dist_dir)

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name=NAME,
    icon='resources/icon.ico',
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
)

copy = {
    'app/static': 'app/static',
    'app/templates': 'app/templates',
    'resources': 'resources',
    'resources/config.default.yaml': 'config.yaml',
}

for src, dst in copy.items():
    src_path = Path(src)
    dst_path = dist_dir / dst
    if src_path.is_dir():
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    else:
        shutil.copy(src_path, dst_path)

# Zip for distribution and save to current directory
zip_path = Path(f'{NAME}.zip')
shutil.make_archive(NAME, 'zip', dist_dir)
shutil.move(zip_path, dist_dir)
