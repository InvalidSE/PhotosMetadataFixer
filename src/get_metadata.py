# ========== Imports ==========
import os
import json
import re

# ========== Functions ==========
def get_metadata(file):

    # Attempt Default JSON
    metadata_path = file + ".json"
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            return metadata

    # If the file name is too long, the JSON is cut shorter
    if len(file.split('\\')[-1]) > 46:
        new_file = file.split('\\')[-1][:46]
        new_file = file.replace(file.split('\\')[-1], new_file)

        # Check if the JSON exists
        metadata_path = new_file + ".json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                return metadata
            
    if "-edited" in file:
        # Check if the JSON exists without the "-edited" in the file name.
        metadata_path = file.replace("-edited", "") + ".json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                return metadata

    # If the file is a duplicate (eg img(1).jpg), it is possible the JSON has the number after the image file extension. (eg img.jpg(1).json)
    if("(" in file and ")" in file):

        # Take out the number in the file name. (n)
        file = move_number_to_end(file)
        
        if file is None:
            return None
        
        # Check if the JSON exists with the number at the end.
        metadata_path = file + ".json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                return metadata
            
    return None
                
def move_number_to_end(filename):
    # Get the number in the file name.
    match = re.search(r'\((.*?)\)', filename)
    if match:
        number = match.group(1)
    else:
        return None

    # Remove the number from the file name.
    filename = filename.replace(f"({number})", "")

    # Add the number to the end of the file name.
    filename = filename + f"({number})"

    return filename