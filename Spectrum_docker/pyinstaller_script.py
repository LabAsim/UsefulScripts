"""A pyinstaller script to convert the main ton a executable"""
import os
import PyInstaller.__main__
import constants

# To render colors properly in the terminal
constants.COLORAMA_TERMINAL_COLORS = True

name = 'main.py'
dir_path = os.path.dirname(__file__)

PyInstaller.__main__.run([
    f'{name}',
    '--onefile',
    '--console',
    '-y'
])

try:
    os.remove(os.path.join(dir_path + '\\dist', 'spectrum_docker.exe'))
except:
    pass
os.rename(os.path.join(dir_path + '\\dist', 'main.exe'), os.path.join(dir_path + '\\dist', 'spectrum_docker.exe'))