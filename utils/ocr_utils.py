from PIL import Image, ImageOps, ImageEnhance
from pyautogui import screenshot as pyautogui_screenshot
import logging
logging.getLogger('easyocr').setLevel(logging.ERROR)
print("Loading OCR...")
from easyocr import Reader
print("OCR loaded!")
import numpy as np

reader = Reader(['en'])

def extract_text_from_roi(extract_x, extract_y, extract_width, extract_height, resolution):
    _, x, y, _, _ = resolution
    screenshot = pyautogui_screenshot(region=(x + extract_x, y + extract_y, extract_width, extract_height))
    resized_image = screenshot.resize((extract_width * 4, extract_height * 4), Image.Resampling.LANCZOS)
    image_np = np.array(resized_image)
    white_threshold = 200
    black_threshold = 50
    mask = ((image_np[:, :, 0] > white_threshold) & (image_np[:, :, 1] > white_threshold) & (image_np[:, :, 2] > white_threshold)) | \
           ((image_np[:, :, 0] < black_threshold) & (image_np[:, :, 1] < black_threshold) & (image_np[:, :, 2] < black_threshold))
    filtered_image_np = np.zeros_like(image_np)
    filtered_image_np[mask] = image_np[mask]
    filtered_image = Image.fromarray(filtered_image_np)
    gray_image = ImageOps.grayscale(filtered_image)
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2)
    binarized_image = enhanced_image.point(lambda p: 255 if p > 160 else 0)
    image_np = np.array(binarized_image)
    result = reader.readtext(image_np)
    return " ".join([text for (_, text, _) in result])