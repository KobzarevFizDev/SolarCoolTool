from PyInstaller.utils.hooks import exec_statement

qt_binding = 'PyQt5'  

if qt_binding == 'PyQt5':
    excludedimports = ['PySide2', 'PySide6']
else:
    excludedimports = ['PyQt5', 'PyQt6']