from setuptools import setup, find_packages

setup(
    name='TimeDistancePlotBuilder', 
    version='0.7.3',
    packages=find_packages(include=['TimeDistancePlotBuilder*']),
    install_requires=open('requirements.txt').read().splitlines(),
    include_package_data=True,
    package_data={
        "TimeDistancePlotBuilder":["Resources/*"],
    },
    entry_points={
        'console_scripts': [
            'tdpb = TimeDistancePlotBuilder.app:main',
        ],
    },
)
