# Google Photos Metadata Re-attacher
# Created by InvalidSE - https://github.com/InvalidSE

# ========== Imports ==========
import os
import json

import get_metadata
import attach_metadata

# ========== Settings ==========
takeout_dir = "D:\Photos\Photos Takeout\Takeout\Google Photos"
save_dir = "D:\Photos\Photos Takeout\Takeout\Google Photos Edited"
temp_dir = "D:\Photos\Photos Takeout\Takeout\Google Photos Temp"
# supported_file_formats = ['jpg', 'mp4', 'gif', 'mov', 'heic', 'jpeg', 'webp', 'arw', 'png']
supported_file_formats = ['jpg', 'jpeg']

# ========== Functions ==========

# Get all supported files in a directory and its subdirectories.
def get_supported_files(path):
    file_count = 0
    supported_files = []
    extensions = []

    for r, d, f in os.walk(path):
        for file in f: 
            if file.split(".")[-1].lower() == 'json':
                continue
            if file.split(".")[-1].lower() in supported_file_formats:
                supported_files.append(os.path.join(r, file))
            file_count += 1
            if file.split(".")[-1].lower() not in extensions:
                extensions.append(file.split(".")[-1].lower())
    
    return supported_files, file_count, extensions

# ========== Main ==========


# Get all supported files in the takeout directory.
supported_files, file_count, extensions = get_supported_files(takeout_dir)

unsupported_formats = []
for extension in extensions:
    if extension not in supported_file_formats:
        unsupported_formats.append(extension)

# Start the metadata re-attachment process.
i = 0
success = 0
for file in supported_files:
    i += 1
    print("[INFO] Processing {}/{}: {}".format(i, len(supported_files), file.replace(takeout_dir, "")))
    metadata = get_metadata.get_metadata(file)

    if metadata is None:
        print("[ERROR] No Metadata Found.")
        continue

    result = attach_metadata.attach_metadata(file, metadata, save_dir, temp_dir, takeout_dir)

    if result:
        success += 1

print("[INFO] Done!")
print("[INFO] {}/{} ({})% Success".format(success, len(supported_files), round(success/len(supported_files)*100, 2)))
print("[INFO] Supported Files: {}/{} ({}%)".format(len(supported_files), file_count, round(len(supported_files)/file_count*100, 2)))
print("[INFO] Supported Formats: {}".format(supported_file_formats))
print("[INFO] Unsupported Formats: {}".format(unsupported_formats))
