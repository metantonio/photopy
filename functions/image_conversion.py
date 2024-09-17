# image_conversion.py

from PIL import Image
import os
import numpy as np
from datetime import datetime

def convert_image_format(image, target_format, save_path):
    """
    Converts the given image to the specified format and saves it to the specified path.
    
    :param image: The image to be converted (PIL Image)
    :param target_format: The target format as a string (e.g., 'JPEG', 'PNG')
    :param save_path: The path where the converted image should be saved
    :return: The path of the converted image
    """
    if not target_format.lower() in ['jpeg', 'png', 'bmp', 'gif']:
        raise ValueError("Unsupported target format. Supported formats: JPEG, PNG, BMP, GIF")
    
    # Get the current date and time
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

    img = Image.fromarray(image)

    converted_image_path = os.path.join('./flagged/output', f"converted_image_{current_date}.{target_format.lower()}")
    img.save(converted_image_path, format=target_format.upper())
    return converted_image_path

def load_image(image_path):
    """
    Loads an image from a given path and converts it to a numpy array.
    
    :param image_path: The path to the image
    :return: The image as a numpy array
    """
    img = Image.open(image_path)
    return np.array(img)