# ========== Imports ==========
import os
import json
import PIL, PIL.Image
import datetime

# ========== Each File Type ==========
def attach_png(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] PNG not yet implemented.")
    return False

def attach_jpg(file, metadata, save_dir, temp_dir, takeout_dir):
    img = PIL.Image.open(file)
    exif_data = img.getexif()

    print(exif_data)
    
    # add geo data
    # if metadata.get("lat") is not None:
    #     exif_data[34853] = [
    #         (2, 1),
    #         (metadata.get("lat"), 1),
    #         (0, 1),
    #         (metadata.get("lon"), 1),
    #         (0, 1),
    #         (metadata.get("alt"), 1)
    #     ]
    #     exif_data[34853] = exif_data[34853] + [
    #         (2, 2),
    #         (metadata.get("latSpan"), 1),
    #         (0, 1),
    #         (metadata.get("lonSpan"), 1),
    #         (0, 1),
    #         (0, 1)
    #     ]
    
    # add photo taken time
    if metadata.get("photoTakenTime") is not None:
        exif_data[306] = datetime.datetime.fromtimestamp(int(metadata.get("photoTakenTime"))).strftime("%Y:%m:%d %H:%M:%S") # Does this need time zone?
        exif_data[36867] = datetime.datetime.fromtimestamp(int(metadata.get("photoTakenTime"))).strftime("%Y:%m:%d %H:%M:%S") # Does this need time zone?

    # add favorited
    if metadata.get("favorited") is not None:
        exif_data[42036] = metadata.get("favorited")

    # save the image to the temp directory
    new_file = file.replace(takeout_dir, temp_dir)
    if not os.path.exists(os.path.dirname(new_file)):
        os.makedirs(os.path.dirname(new_file))

    img.save(new_file, "jpeg", exif=exif_data)

    img.close()

    return True

def attach_jpeg(file, metadata, save_dir, temp_dir, takeout_dir):
    return attach_jpg(file, metadata, save_dir, temp_dir, takeout_dir)

def attach_webp(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] WEBP not yet implemented.")
    return False

def attach_arw(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] ARW not yet implemented.")
    return False

def attach_heic(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] HEIC not yet implemented.")
    return False

def attach_mp4(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] MP4 not yet implemented.")
    return False

def attach_gif(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] GIF not yet implemented.")
    return False

def attach_mov(file, metadata, save_dir, temp_dir, takeout_dir):
    print("[WARN] MOV not yet implemented.")
    return False


# ========== Main ==========
def attach_metadata(file, metadata, save_dir, temp_dir, takeout_dir):

    # Check if metadata has anything worth saving.

    # Useful metadata:
    #   "photoTakenTime": {
    #     "timestamp": "1690274164",
    #     "formatted": "25 Jul 2023, 08:36:04 UTC"
    #   },
    #   "geoDataExif": {
    #     "latitude": 0.0,
    #     "longitude": 0.0,
    #     "altitude": 0.0,
    #     "latitudeSpan": 0.0,
    #     "longitudeSpan": 0.0
    #   },
    #   "favorited": true

    metadata_python = {}

    if metadata.get("photoTakenTime") is not None:
        metadata_python["photoTakenTime"] = metadata.get("photoTakenTime").get("timestamp")

    if metadata.get("geoDataExif") is not None:
        metadata_python["lat"] = metadata.get("geoDataExif").get("latitude")
        metadata_python["lon"] = metadata.get("geoDataExif").get("longitude")
        metadata_python["alt"] = metadata.get("geoDataExif").get("altitude")
        metadata_python["latSpan"] = metadata.get("geoDataExif").get("latitudeSpan")
        metadata_python["lonSpan"] = metadata.get("geoDataExif").get("longitudeSpan")

        if metadata_python["lat"] == 0 and metadata_python["lon"] == 0 and metadata_python["alt"] == 0 and metadata_python["latSpan"] == 0 and metadata_python["lonSpan"] == 0:
            metadata_python.pop("lat")
            metadata_python.pop("lon")
            metadata_python.pop("alt")
            metadata_python.pop("latSpan")
            metadata_python.pop("lonSpan")

    if metadata.get("favorited") is not None:
        metadata_python["favorited"] = True

    # print(str(metadata_python))

    # Get the file name and extension.
    file_name = file.split('\\')[-1]
    extension = file_name.split(".")[-1].lower()

    try:
        if extension == "png":
            result = attach_png(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "jpg":
            result = attach_jpg(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "jpeg":
            result = attach_jpeg(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "webp":
            result = attach_webp(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "arw":
            result = attach_arw(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "heic":
            result = attach_heic(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "mp4":
            result = attach_mp4(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "gif":
            result = attach_gif(file, metadata_python, save_dir, temp_dir, takeout_dir)
        elif extension == "mov":
            result = attach_mov(file, metadata_python, save_dir, temp_dir, takeout_dir)
        else:
            print("[ERROR] Unsupported file format: {}".format(extension))
            return False
    except Exception as e:
        print("[ERROR] Exception: {}".format(e) + "\n" + "[ERROR] Failed to attach metadata to {}".format(file_name))
        return False
    
    if result:
        print("[SUCCESS] Metadata attached to {}".format(file_name))

    return result