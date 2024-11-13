from setuptools import setup, find_packages

setup(
    name='TimeDistancePlotBuilder', 
    version='0.6',
    packages=find_packages(include=['TimeDistancePlotBuilder*']),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'gui_scripts': [
            'tdpb = TimeDistancePlotBuilder.app:main',
        ],
    },
)
