import os
import struct
import zlib

EXTENSION = ".bin"
HEADER_FORMAT = '256sQ'  # filename padded to 256 bytes + 8 byte unsigned long long
HEADER_SIZE = 264
MAX_SIZE = 500 * 1024 * 1024

def pack_data_files(input_folder, status_callback=print):
    files_to_pack = []
    for root, dirs, files in os.walk(input_folder):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, input_folder)
            files_to_pack.append((full_path, rel_path))
    
    print(f"Found {len(files_to_pack)} files to pack.")
    
    if not files_to_pack:
        print("No files to pack! Check input folder.")
        return False
    
    file_index = 1
    current_size = 0
    output_file = None
    
    def get_output_filename(index):
        return f"data{index}.bin"
    
    def open_new_file(index):
        filename = get_output_filename(index)
        print(f"Creating new output file: {filename}")
        return open(filename, 'wb')
    
    try:
        output_file = open_new_file(file_index)
        
        for i, (full_path, rel_path) in enumerate(files_to_pack):
            print(f"Packing {rel_path}... ({i+1}/{len(files_to_pack)})")
            
            with open(full_path, 'rb') as f_in:
                raw_data = f_in.read()
            
            compressed_data = zlib.compress(raw_data)
            
            name_bytes = rel_path.encode('utf-8')
            if len(name_bytes) > 256:
                raise ValueError(f"Filename '{rel_path}' too long (max 256 bytes)")
            
            name_bytes_padded = name_bytes.ljust(256, b'\0')
            comp_size = len(compressed_data)
            
            header = struct.pack(HEADER_FORMAT, name_bytes_padded, comp_size)
            entry_size = len(header) + comp_size
            
            if current_size + entry_size > MAX_SIZE:
                output_file.close()
                file_index += 1
                output_file = open_new_file(file_index)
                current_size = 0
            
            output_file.write(header)
            output_file.write(compressed_data)
            current_size += entry_size
        
        output_file.close()
        print("✅ Packing complete.")
        return True
        
    except Exception as e:
        if output_file and not output_file.closed:
            output_file.close()
        print(f"❌ Error packing files: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        input_folder = sys.argv[1]
    else:
        input_folder = "files"

    pack_data_files(input_folder)