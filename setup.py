from setuptools import setup, find_packages

setup(
    name='TimeDistancePlotBuilder', 
    version='0.1',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'gui_scripts': [
            'runn2 = TimeDistancePlotBuilder.app:main',
        ],
    },
)
