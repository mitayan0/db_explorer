import os
import sys

block_cipher = None

# Set project root to current working directory
project_root = os.getcwd()

# List all data files to be included with absolute source paths
# But keep destination paths relative (they are relative to the app bundle)
added_files = [
    (os.path.join(project_root, 'databases'), 'databases'),
    (os.path.join(project_root, 'assets'), 'assets'),
]

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'psycopg2',
        'sqlparse',
        'oracledb',
        'pandas',
        'qtawesome',
        'openpyxl',
        'cdata.servicenow',
        'cdata.csv'
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
    [],  # binaries go to COLLECT, not embedded
    exclude_binaries=True,  # required for one-folder mode
    name='DB_Explorer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=os.path.join(project_root, 'file_version_info.txt'),
    icon=os.path.join(project_root, 'assets', 'app_icon.ico') if os.path.exists(os.path.join(project_root, 'assets', 'app_icon.ico')) else None,
)

# One-folder layout: all DLLs live next to the .exe, not in %TEMP%
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DB_Explorer',
)
