import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance

# -------- ML FEATURES --------
def extract_features(image_path):
    img = cv2.imread(image_path)

    img = cv2.resize(img, (256, 256))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise
    noise = np.std(gray)

    # Edge density
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges) / (256 * 256)

    # Compression artifact
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, enc = cv2.imencode(".jpg", img, encode_param)
    dec = cv2.imdecode(enc, 1)
    compression_diff = np.mean(np.abs(img - dec))

    return [noise, edge_density, compression_diff]


# -------- ELA --------
def perform_ela(image_path, quality=90):
    original = Image.open(image_path).convert("RGB")

    temp_path = "static/uploads/temp_ela.jpg"
    original.save(temp_path, "JPEG", quality=quality)
    resaved = Image.open(temp_path)

    ela_image = ImageChops.difference(original, resaved)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1

    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    ela_save_path = image_path.replace(".jpg", "_ela.jpg")
    ela_image.save(ela_save_path)

    return ela_save_path


# -------- METADATA --------
def get_metadata(image_path):
    image = Image.open(image_path)
    exif = image._getexif()

    if not exif:
        return {}, "No EXIF metadata found"

    tags = {
        305: "Software",
        271: "Make",
        272: "Model",
        306: "DateTime"
    }

    metadata = {}
    software = "None Detected"

    for tag, value in exif.items():
        if tag in tags:
            metadata[tags[tag]] = value
            if tag == 305:
                software = value

    return metadata, software
