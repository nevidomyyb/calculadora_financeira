# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Coleta apenas arquivos de dados e libs nativas do Kivy,
# sem varrer kivy.garden (que causa o erro do collect_all).
kivy_datas    = collect_data_files('kivy', includes=['**/*'])
kivy_binaries = collect_dynamic_libs('kivy')

# Inclui SDL2/GLEW se kivy_deps estiver instalado no ambiente
try:
    from kivy_deps import sdl2, glew
    kivy_deps_bins = [(b, '.') for b in sdl2.dep_bins + glew.dep_bins]
except ImportError:
    kivy_deps_bins = []

a = Analysis(
    ['calculadora_financeira.py'],
    pathex=[],
    binaries=kivy_binaries + kivy_deps_bins,
    datas=kivy_datas,
    hiddenimports=[
        'kivy',
        'kivy._event',
        'kivy.properties',
        'kivy.core.text.markup',
        'kivy.core.window.window_sdl2',
        'kivy.core.image.img_sdl2',
        'kivy.core.audio.audio_sdl2',
        'kivy.graphics.cgl_backend.cgl_glew',
        'kivy.graphics.cgl_backend.cgl_angle',
        'kivy.uix.recycleview',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['kivy.garden'],
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
    name='CalculadoraFinanceira',
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
)
