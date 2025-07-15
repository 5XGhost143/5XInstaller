import os
import shutil
import sys
from datetime import datetime
from InstallerV2.config import App_Name

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(folder_path)

def main():
    bin_folder = 'Bin Creator'
    installer_dist_folder = os.path.join('InstallerV2', 'dist')
    today = datetime.now().strftime('%Y-%m-%d')
    build_folder = f'build-{today}'

    try:
        files_in_bin = os.listdir(bin_folder)
    except FileNotFoundError:
        print(f"Source folder '{bin_folder}' does not exist. ❌")
        sys.exit(1)

    data_files = [f for f in files_in_bin if f.startswith('data') and f.endswith('.bin')]

    if not data_files:
        print("No Data was found")
        sys.exit(0)

    clear_folder(build_folder)
    print(f"Cleaned or created target folder: {build_folder} ✅")

    for filename in data_files:
        src_path = os.path.join(bin_folder, filename)
        dst_path = os.path.join(build_folder, filename)
        shutil.copy2(src_path, dst_path)
        print(f"Copied {filename} to {build_folder}")

    main_exe_path = os.path.join(installer_dist_folder, 'main.exe')
    if os.path.exists(installer_dist_folder) and os.path.isdir(installer_dist_folder):
        if os.path.isfile(main_exe_path):
            target_name = f"{App_Name}-Installer-Windows-x64.exe"
            target_path = os.path.join(build_folder, target_name)
            shutil.copy2(main_exe_path, target_path)
            print(f"Copied main.exe to {build_folder}")
        else:
            print(f"No main.exe found in {installer_dist_folder}")

        ico_src = os.path.join(installer_dist_folder, 'ico')
        ico_dst = os.path.join(build_folder, 'ico')
        if os.path.exists(ico_src) and os.path.isdir(ico_src):
            shutil.copytree(ico_src, ico_dst)
            print(f"Copied 'ico' folder to {build_folder}")
        else:
            print(f"No 'ico' folder found in {installer_dist_folder}")
    else:
        print(f"Folder {installer_dist_folder} does not exist ❌")

    print("All files copied successfully. ✅")

if __name__ == "__main__":
    main()
