from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='fluedit',
    version=open(join(dirname(__file__), './fluedit/version.txt')).read(),
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'gui_scripts': ['fluedit = fluedit.__main__:main']
    },
)
