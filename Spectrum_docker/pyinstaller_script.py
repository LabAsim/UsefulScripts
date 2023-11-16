import os

import PyInstaller.__main__

name = 'main.py'
dir_path = os.path.dirname(__file__)

PyInstaller.__main__.run([
    f'{name}',
    '--onefile',
    '--console',
    '--nowindowed',
    '--noconsole',
    '-y'
])

try:
    os.remove(os.path.join(dir_path + '\\dist', 'spectrum_docker.exe'))
except:
    pass
os.rename(os.path.join(dir_path + '\\dist', 'main.exe'), os.path.join(dir_path + '\\dist', 'spectrum_docker.exe'))