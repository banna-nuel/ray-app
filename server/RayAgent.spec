# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\unipaz\\tic\\ray-app\\.env', '.'), ('C:\\unipaz\\tic\\ray-app\\server\\agent.py', '.'), ('C:\\unipaz\\tic\\ray-app\\server\\db.py', '.'), ('C:\\unipaz\\tic\\ray-app\\server\\ai_interpreter.py', '.'), ('C:\\unipaz\\tic\\ray-app\\server\\executor.py', '.')]
binaries = []
hiddenimports = ['pystray._win32', 'PIL._tkinter_finder', 'pyperclip', 'pycaw', 'pycaw.pycaw', 'comtypes', 'comtypes.client', 'dotenv', 'openai', 'httpx', 'httpx._transports', 'httpcore', 'pyautogui', 'pygetwindow', 'supabase', 'gotrue', 'postgrest', 'realtime', 'storage3', 'supafunc']
tmp_ret = collect_all('pystray')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('supabase')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('gotrue')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('postgrest')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('realtime')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('storage3')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('supafunc')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['tray.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorflow', 'torch', 'numpy', 'pandas', 'scipy', 'matplotlib', 'sklearn', 'cv2', 'transformers', 'torchaudio', 'torchvision', 'tensorboard', 'keras', 'jax', 'IPython', 'notebook', 'jupyterlab', 'pytest', 'unittest'],
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
    name='RayAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
