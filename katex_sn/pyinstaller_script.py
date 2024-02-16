"""A pyinstaller script to convert the main ton a executable"""
import os
import PyInstaller.__main__

name = 'main.py'
dir_path = os.path.dirname(__file__)

PyInstaller.__main__.run([
    f'{name}',
    '--onefile',
    '--console',
    '-y'
])

try:
    os.remove(os.path.join(dir_path + '\\dist', 'katex_sn.exe'))
except:
    pass
os.rename(os.path.join(dir_path + '\\dist', 'main.exe'), os.path.join(dir_path + '\\dist', 'katex_sn.exe'))