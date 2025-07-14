import os
import shutil
import struct
import zlib
import winreg
import ctypes
from config import EXTENSION, HEADER_FORMAT, HEADER_SIZE
from utils import remove_from_path

def unpack_data_files(output_folder, status_callback=print):
    data_files = sorted([f for f in os.listdir('.') if f.startswith("data") and f.endswith(EXTENSION)])
    
    if not data_files:
        status_callback(f"No {EXTENSION} files found in the current directory")
        return False
    
    os.makedirs(output_folder, exist_ok=True)
    status_callback(f"Unpacking {len(data_files)} data package(s)...")
    
    try:
        for i, data_file_name in enumerate(data_files):
            status_callback(f"Processing {data_file_name}... ({i+1}/{len(data_files)})")
            
            with open(data_file_name, 'rb') as data_file:
                while True:
                    header_bytes = data_file.read(HEADER_SIZE)
                    if not header_bytes or len(header_bytes) < HEADER_SIZE:
                        break
                    
                    name_bytes, comp_size = struct.unpack(HEADER_FORMAT, header_bytes)
                    filename = name_bytes.rstrip(b'\0').decode('utf-8')
                    
                    compressed_data = data_file.read(comp_size)
                    if len(compressed_data) < comp_size:
                        raise ValueError(f"Incomplete data in {data_file_name} for file {filename}")
                    
                    raw_data = zlib.decompress(compressed_data)
                    
                    target_path = os.path.join(output_folder, filename)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    
                    with open(target_path, 'wb') as f_out:
                        f_out.write(raw_data)
        
        status_callback("✅ Unpacking complete.")
        return True
        
    except Exception as e:
        status_callback(f"❌ Error unpacking files: {e}")
        return False

def add_to_path(install_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                             0, winreg.KEY_ALL_ACCESS)
        
        current_path, _ = winreg.QueryValueEx(key, "Path")
        
        if install_path.lower() not in [p.lower() for p in current_path.split(";")]:
            new_path = current_path + ";" + install_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, "Environment")
        
        winreg.CloseKey(key)
        return True
        
    except Exception as e:
        return str(e)