from setuptools import setup, find_packages

setup(
    name='check',
    version='0.1.2',
    packages=find_packages(where='.'),
    py_modules=['todo'],
    install_requires=[
        'click',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'check=todo:check',
        ],
    },
)