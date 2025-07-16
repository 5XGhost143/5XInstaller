import os
import ctypes
import winreg
import traceback
import pythoncom
from win32com.client import Dispatch
from config import *

def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def remove_from_path(install_path):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_ALL_ACCESS
        )
        current_path, _ = winreg.QueryValueEx(key, "Path")
        path_parts = current_path.split(";")
        new_path_parts = [p for p in path_parts if p.lower() != install_path.lower()]

        if len(new_path_parts) != len(path_parts):
            new_path = ";".join(new_path_parts)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, "Environment")

        winreg.CloseKey(key)
        return True

    except Exception as e:
        return str(e)

def create_desktop_shortcut(install_path, app_name, output_exe):
    try:
        exe_path = os.path.join(os.path.normpath(install_path), output_exe)
        if not os.path.isfile(exe_path):
            return f"EXE not found: {exe_path}"

        pythoncom.CoInitialize()
        shell = Dispatch('WScript.Shell')

        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        shortcut_path = os.path.join(desktop_path, f"{app_name}.lnk")

        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = exe_path
        shortcut.WorkingDirectory = install_path
        shortcut.WindowStyle = 1
        shortcut.Description = f"Launch {app_name}"
        shortcut.IconLocation = exe_path
        shortcut.save()

        return True

    except Exception as e:
        return f"Error creating desktop shortcut: {str(e)}\n\n{traceback.format_exc()}"

def create_startmenu_shortcut(install_path, app_name, output_exe):
    try:
        install_path = os.path.normpath(install_path)
        exe_path = os.path.join(install_path, output_exe)

        if not os.path.isfile(exe_path):
            return f"EXE not found: {exe_path}"

        start_menu = os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs")
        shortcut_path = os.path.join(start_menu, f"{app_name}.lnk")

        pythoncom.CoInitialize()
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = exe_path
        shortcut.WorkingDirectory = install_path
        shortcut.WindowStyle = 1
        shortcut.Description = f"Launch {app_name}"
        shortcut.IconLocation = exe_path
        shortcut.save()

        return True

    except Exception as e:
        return f"Error creating Start Menu shortcut: {str(e)}\n\n{traceback.format_exc()}"
        
def create_autostart_entry(install_path, app_name, output_exe):
    try:
        exe_path = os.path.join(os.path.normpath(install_path), output_exe)
        if not os.path.isfile(exe_path):
            return f"EXE not found: {exe_path}"
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        return f"Error creating autostart entry: {str(e)}"

def remove_autostart_entry(app_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        return str(e)
