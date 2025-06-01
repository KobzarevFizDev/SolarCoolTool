# from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# datas = collect_data_files('sunpy')
# hiddenimports = collect_submodules('sunpy')


from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('sunpy')