# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules


a = Analysis(
    ['TimeDistancePlotBuilder\\app.py'],
    pathex=['D:\\Python\\SolarCoolTool'],
    binaries=[],
    datas=[(r'D:\\Python\\SolarCoolTool\\TimeDistancePlotBuilder\\Resources\\*.png', 'TimeDistancePlotBuilder/Resources'),
           (r'D:\\Python\\SolarCoolTool\\TimeDistancePlotBuilder\\Resources\\*.jpg', 'TimeDistancePlotBuilder/Resources'),
           (r'D:\\Python\\SolarCoolTool\\venv\\Lib\\site-packages\\aiapy\\CITATION.rst', 'aiapy'),
           (r'D:\\Python\\SolarCoolTool\\venv\\Lib\\site-packages\\drms\\CITATION.rst', 'drms'),
           (r'D:\\Python\\SolarCoolTool\\venv\\Lib\\site-packages\\astropy\\CITATION', 'astropy'),
           (r'D:\\Python\\SolarCoolTool\\venv\\Lib\site-packages\\asdf\\_jsonschema\schemas\\*.json', 'asdf/_jsonschema/schemas'),
            *collect_data_files('astropy'),
            *collect_data_files('drms'),
            *collect_data_files('asdf'),
           (r'D:\\Python\\SolarCoolTool\\venv\\Lib\\site-packages\\astropy\\units\\format\\*.py', 'astropy/units/format'),
           (r'D:\\Python\\SolarCoolTool\\venv\\Lib\site-packages\\Pillow-*.dist-info\\*', 'Pillow.dist-info')],
     hiddenimports=[
        'h5netcdf',
        'sunpy.timeseries',
        'sunpy.visualization',
        'sunpy.image',
        'sunpy.net',
        'drms',
        'importlib_resources.trees',
        'importlib_resources.readers',
        'importlib_resources.abc',
        'importlib_resources._legacy',
        'cdflib',
        'aiapy.calibrate',
        'asdf',
        'asdf._jsonschema',
        *collect_submodules('astropy'),
        *collect_submodules('drms'),
        *collect_submodules('asdf'),
        'PIL',
        'Pillow',
        'importlib.metadata',
        *collect_submodules('PIL')
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['imageio_ffmpeg',
              'ffmpeg',
              'imageio.plugins.ffmpeg',
              'opencv_videoio_ffmpeg*',
              'cv2',
              'pytest',
              '_pytest' 
              'astropy.tests', 
              'skimage.tests', 
              'matplotlib.tests',
              'PySide2'
              ],
    noarchive=False,
    optimize=0,
)

a.binaries = [
    x for x in a.binaries 
    if not (
        x[0].endswith('opengl32sw.dll') or
        x[0].startswith('libopenblas64_')
    )
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
