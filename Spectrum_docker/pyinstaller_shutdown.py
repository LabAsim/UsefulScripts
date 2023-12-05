"""A pyinstaller script to convert the main ton a executable"""
import os
import PyInstaller.__main__

name = 'shutdown.py'
dir_path = os.path.dirname(__file__)

PyInstaller.__main__.run([
    f'{name}',
    '--onefile',
    '--console',
    '-y'
])

