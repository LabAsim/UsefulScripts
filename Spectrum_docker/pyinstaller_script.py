import PyInstaller.__main__

name = 'main.py'

PyInstaller.__main__.run([
    f'{name}',
    '--onefile',
    '--console',
    '--nowindowed',
    '--noconsole',
    '-y'
])
