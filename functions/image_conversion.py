# image_conversion.py

from PIL import Image
import os
import numpy as np

def convert_image_format(image, target_format):
    """
    Converts the given image to the specified format.
    
    :param image: The image to be converted (PIL Image)
    :param target_format: The target format as a string (e.g., 'JPEG', 'PNG')
    :return: The converted image in the target format
    """
    if not target_format.lower() in ['jpeg', 'png', 'bmp', 'gif']:
        raise ValueError("Unsupported target format. Supported formats: JPEG, PNG, BMP, GIF")
    
    img = Image.fromarray(image)
    converted_image_path = f"converted_image.{target_format.lower()}"
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
