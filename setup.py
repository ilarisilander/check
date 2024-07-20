from setuptools import setup, find_packages
from src.constants import APP_VERSION


setup(
    name='check',
    version=APP_VERSION,
    packages=find_packages(where='.'),
    py_modules=['cli'],
    install_requires=[
        'click',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'check=cli:check',
        ],
    },
)