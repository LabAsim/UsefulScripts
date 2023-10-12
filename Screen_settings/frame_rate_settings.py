"""
Install pypiwin32 for win32api and win32con
https://stackoverflow.com/questions/18907889/importerror-no-module-named-pywintypes
"""
import ctypes
import struct
import sys
import time
import win32con as c
import win32api  # pip install pywin32
from pywin32_system32 import *
import pywintypes


def set_res(width, height, bpp=32):
    """https://stackoverflow.com/questions/51987408/programmatically-change-windows-resolution"""
    DM_BITSPERPEL = 0x00040000
    DM_PELSWIDTH = 0x00080000
    DM_PELSHEIGHT = 0x00100000
    CDS_UPDATEREGISTRY = 0x00000001
    SIZEOF_DEVMODE = 148

    user32 = ctypes.WinDLL('user32.dll')
    DevModeData = struct.calcsize("32BHH") * bytes('\x00', 'utf')
    DevModeData += struct.pack("H", SIZEOF_DEVMODE)
    DevModeData += struct.calcsize("H") * bytes('\x00', 'utf')
    dwFields = (width and DM_PELSWIDTH or 0) | (height and DM_PELSHEIGHT or 0) | (bpp and DM_BITSPERPEL or 0)
    DevModeData += struct.pack("L", dwFields)
    DevModeData += struct.calcsize("l9h32BHL") * bytes('\x00', 'utf')
    DevModeData += struct.pack("LLL", bpp or 0, width or 0, height or 0)
    DevModeData += struct.calcsize("8L") * bytes('\x00', 'utf')
    result = user32.ChangeDisplaySettingsA(DevModeData, CDS_UPDATEREGISTRY)
    return result == 0  # success if zero, some failure otherwise


def printInfo(device):
    """https://stackoverflow.com/questions/1225057/how-can-i-determine-the-monitor-refresh-rate"""
    print((device.DeviceName, device.DeviceString))
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    for varName in ['Color', 'BitsPerPel', 'DisplayFrequency']:
        print("%s: %s" % (varName, getattr(settings, varName)))


def ttest():
    device = win32api.EnumDisplayDevices(None, 0, 0)

    devmode = win32api.EnumDisplaySettings(device.DeviceName, c.ENUM_CURRENT_SETTINGS)
    FlagForPrimary = c.CDS_SET_PRIMARY | c.CDS_UPDATEREGISTRY | c.CDS_NORESET
    FlagForSec = c.CDS_UPDATEREGISTRY | c.CDS_NORESET

    devmode.DisplayFrequency = 144
    win32api.ChangeDisplaySettingsEx(device.DeviceName, devmode, FlagForPrimary)
    # Update everything
    win32api.ChangeDisplaySettingsEx()

    time.sleep(2)

    devmode.DisplayFrequency = 60
    win32api.ChangeDisplaySettingsEx(device.DeviceName, devmode, FlagForPrimary)
    win32api.ChangeDisplaySettingsEx()
    printInfo(device)


def main():
    """
    # In python:
    # https://stackoverflow.com/questions/35814309/winapi-changedisplaysettingsex-does-not-work
    # In C:
    # https://stackoverflow.com/questions/63654012/programmatically-change-windows-laptops-refresh-rate
    # About ChangeDisplaySettingsEx
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-changedisplaysettingsexa
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-changedisplaysettingsa

    :return: None
    """
    device = win32api.EnumDisplayDevices(None, 0, 0)
    FlagForPrimary = c.CDS_SET_PRIMARY | c.CDS_UPDATEREGISTRY | c.CDS_NORESET

    while True:
        devmode = win32api.EnumDisplaySettings(device.DeviceName, c.ENUM_CURRENT_SETTINGS)
        if devmode.DisplayFrequency == 144:
            devmode.DisplayFrequency = 60
            win32api.ChangeDisplaySettingsEx(device.DeviceName, devmode, FlagForPrimary)
            win32api.ChangeDisplaySettingsEx()
            print(f"Display Frequency changed from 144 to 60 hz")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
