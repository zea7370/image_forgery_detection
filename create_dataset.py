import cv2
import os
import numpy as np
import random
import shutil

SOURCE_DIR = "dataset/source_images"
ORIGINAL_DIR = "dataset/original"
TAMPERED_DIR = "dataset/tampered"

os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(TAMPERED_DIR, exist_ok=True)

def copy_move_tamper(img):
    h, w, _ = img.shape
    x1, y1 = random.randint(0, w//2), random.randint(0, h//2)
    x2, y2 = x1 + 50, y1 + 50
    patch = img[y1:y2, x1:x2]
    img[y1+30:y2+30, x1+30:x2+30] = patch
    return img

def blur_tamper(img):
    return cv2.GaussianBlur(img, (15, 15), 0)

def noise_tamper(img):
    noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
    return cv2.add(img, noise)

tamper_functions = [copy_move_tamper, blur_tamper, noise_tamper]

for file in os.listdir(SOURCE_DIR):
    img_path = os.path.join(SOURCE_DIR, file)
    img = cv2.imread(img_path)

    if img is None:
        continue

    # Save original
    shutil.copy(img_path, os.path.join(ORIGINAL_DIR, file))

    # Create tampered version
    tampered = random.choice(tamper_functions)(img.copy())
    cv2.imwrite(os.path.join(TAMPERED_DIR, file), tampered)

print("✅ Dataset created successfully!")
