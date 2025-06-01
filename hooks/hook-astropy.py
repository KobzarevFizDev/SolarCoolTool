# from PyInstaller.utils.hooks import collect_submodules


# hiddenimports = [
#     'astropy.tests.helper',
#     'astropy.tests.runner',
#     *collect_submodules('astropy.tests')

# ]

from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('astropy')