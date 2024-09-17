# image_resize.py

from PIL import Image
import numpy as np

def resize_image(image, width, height):
    """
    Resizes the given image to the specified width and height.
    
    :param image: The image to be resized (numpy array)
    :param width: The target width in pixels
    :param height: The target height in pixels
    :return: The resized image as a numpy array
    """
    img = Image.fromarray(image)
    resized_img = img.resize((width, height), Image.LANCZOS)
    return np.array(resized_img)
