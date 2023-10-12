import PyInstaller.__main__

name = 'frame_rate_settings.py'

PyInstaller.__main__.run([
    f'{name}',
    '--onefile',
    '--console',
    '--nowindowed',
    '--noconsole',
    '-y'
])