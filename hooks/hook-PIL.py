from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('PIL')
hiddenimports = ['PIL._imaging', 'PIL.Image']