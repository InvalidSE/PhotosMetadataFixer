# Google Photos Metadata Re-attacher
# Created by InvalidSE - https://github.com/InvalidSE

# ========= Example JSON =========
# {
#   "title": "0A9A2458.JPG",
#   "description": "",
#   "creationTime": {
#     "timestamp": "1690353213",
#     "formatted": "26 Jul 2023, 06:33:33 UTC"
#   },
#   "photoTakenTime": {
#     "timestamp": "1690274164",
#     "formatted": "25 Jul 2023, 08:36:04 UTC"
#   },
#   "geoData": {
#     "latitude": 0.0,
#     "longitude": 0.0,
#     "altitude": 0.0,
#     "latitudeSpan": 0.0,
#     "longitudeSpan": 0.0
#   },
#   "geoDataExif": {
#     "latitude": 0.0,
#     "longitude": 0.0,
#     "altitude": 0.0,
#     "latitudeSpan": 0.0,
#     "longitudeSpan": 0.0
#   },
#   "favorited": true
# }

# ========= Imports =========
import os
import json
from PIL import Image
from pillow_heif import register_heif_opener
import re
from PIL.ExifTags import TAGS, GPSTAGS

register_heif_opener()

# ========= Settings =========
takeout_dir = "D:\Photos\Photos Takeout\Takeout\Google Photos"
save_dir = "D:\Photos\Photos Takeout\Takeout\Google Photos Edited"
temp_dir = "D:\Photos\Photos Takeout\Takeout\Google Photos Temp"
supported_file_formats = ['png', 'jpg', 'jpeg', 'webp', 'arw', 'heic', 'heif']

# ========= Functions =========

# Get all supported files in a directory and its subdirectories.
def get_supported_files(path):
    supported_files = []
    file_count = 0
    extensions = []

    for r, d, f in os.walk(path):
        for file in f: 
            if file.split(".")[-1].lower() == 'json':
                continue

            file_count += 1
            if file.split(".")[-1].lower() in supported_file_formats:
                supported_files.append(os.path.join(r, file))

            if file.split(".")[-1].lower() not in extensions:
                extensions.append(file.split(".")[-1].lower())

    print("Supported: {}".format(supported_file_formats))

    unsupported_formats = []
    for extension in extensions:
        if extension not in supported_file_formats:
            unsupported_formats.append(extension)

    print("Unsupported: {}".format(unsupported_formats))
            
    return supported_files, file_count

# Metadata is stored in a JSON file with the same name as the image file.
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

# ========== GPS Data ==========
def get_gps_data(gps):
    # GPS Metadata
    GPSMetadata = {}

    # Latitude
    latitude = gps["latitude"]

    # Longitude
    longitude = gps["longitude"]

    # Altitude
    altitude = gps["altitude"]

    # Latitude Span
    latitudeSpan = gps["latitudeSpan"]

    # Longitude Span
    longitudeSpan = gps["longitudeSpan"]

    # GPS Version ID
    GPSMetadata[0] = 2

    # Latitude Reference
    if latitude < 0:
        GPSMetadata[1] = 'S'
    else:
        GPSMetadata[1] = 'N'

    # Latitude
    latitude = abs(latitude)
    GPSMetadata[2] = ((int(latitude), 1), (1, 1), (0, 1))

    # Longitude Reference
    if longitude < 0:
        GPSMetadata[3] = 'W'
    else:
        GPSMetadata[3] = 'E'

    # Longitude
    longitude = abs(longitude)
    GPSMetadata[4] = ((int(longitude), 1), (1, 1), (0, 1))

    # Altitude Reference
    if altitude < 0:
        GPSMetadata[5] = 1
    else:
        GPSMetadata[5] = 0

    # Altitude
    altitude = abs(altitude)
    GPSMetadata[6] = (int(altitude), 1)

    # Time Stamp
    GPSMetadata[7] = ((0, 1), (0, 1), (0, 1))

    # Latitude Span
    GPSMetadata[16] = ((int(latitudeSpan), 1), (1, 1))

    # Longitude Span
    GPSMetadata[17] = ((int(longitudeSpan), 1), (1, 1))

    return GPSMetadata



# ========== Attach GPS, Photo Taken Time and Favourited Status ==========
def attach_jpg(file, metadata):
    # Open the image file.
    im = Image.open(file)

    # Get the EXIF data.
    exif = im.getexif()

    # Get the GPS data.
    gps = metadata["geoDataExif"]
    if gps is not None:
        exif["GPSInfo"] = get_gps_data(gps)

    # Get the photo taken time.
    photo_taken_time = metadata["photoTakenTime"]["timestamp"]
    if photo_taken_time is not None:
        exif[36867] = photo_taken_time

    # Get the favourited status.
    if "favorited" in metadata.keys():
        exif[42036] = '1'

    # Create file
    new_file = file.replace(takeout_dir, save_dir)
    if not os.path.exists(os.path.dirname(new_file)):
        os.makedirs(os.path.dirname(new_file))

    # Save the image file.
    im.save(new_file, "jpeg", exif=exif)

    # Close the image file.
    im.close()



# ========= Main =========
if __name__ == "__main__":
    files, total = get_supported_files(takeout_dir)
    # print(files)
    print("Found {} supported files of {} ({}%)".format(len(files), total, round(len(files) / total * 100, 2)))
    print("Starting metadata re-attachment...")

    success = 0

    for file in files:
        metadata = get_metadata(file)

        if metadata is not None:
            try: 

                if(file.split(".")[-1].lower() == 'heic'):

                    # convert heic to jpg
                    im = Image.open(file)

                    # Create file
                    new_file = file.replace(takeout_dir, temp_dir)
                    if not os.path.exists(os.path.dirname(new_file)):
                        os.makedirs(os.path.dirname(new_file))

                    im.save(new_file.replace(".heic", ".jpg"), "jpeg")

                    # Close the image file.
                    im.close()

                    # attach metadata
                    attach_jpg(new_file.replace(".heic", ".jpg"), metadata)

                if(file.split(".")[-1].lower() == 'jpeg' or file.split(".")[-1].lower() == 'jpg'):
                    attach_jpg(file, metadata)
                    
                success += 1
            except Exception as e:
                print("Error with {}: {}".format(file, e))
                
        else:
            print("No metadata for {}".format(file))

    print("Successfully re-attached metadata for {}/{} photos ({}%)".format(success, len(files), round(success / len(files) * 100, 2)))
    