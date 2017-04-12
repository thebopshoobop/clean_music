"""Quick script to clean up music directories"""

from setuptools import setup

setup(
    name='clean_music',
    version='0.1',
    py_modules=['clean_music'],
    install_requires=['click'],
    entry_points='''
        [console_scripts]
        clean_music=clean_music:clean
    '''
)
