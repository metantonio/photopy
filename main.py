import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def adjust_brightness(image, brightness):
    enhancer = ImageEnhance.Brightness(Image.fromarray(image))
    return np.array(enhancer.enhance(brightness))

def adjust_contrast(image, contrast):
    enhancer = ImageEnhance.Contrast(Image.fromarray(image))
    return np.array(enhancer.enhance(contrast))

def apply_blur(image, blur_strength):
    img = Image.fromarray(image)
    return np.array(img.filter(ImageFilter.GaussianBlur(blur_strength)))

def apply_sharpen(image):
    img = Image.fromarray(image)
    return np.array(img.filter(ImageFilter.SHARPEN))

def grayscale(image):
    img = Image.fromarray(image).convert('L')
    return np.array(img)

def edit_image(image, brightness, contrast, blur, sharpen, gray):
    if image is None:
        return None
    
    result = adjust_brightness(image, brightness)
    result = adjust_contrast(result, contrast)
    
    if blur > 0:
        result = apply_blur(result, blur)
    
    if sharpen:
        result = apply_sharpen(result)
    
    if gray:
        result = grayscale(result)
    
    return result

iface = gr.Interface(
    fn=edit_image,
    inputs=[
        gr.Image(),
        gr.Slider(0.1, 2.0, 1.0, label="Brillo"),
        gr.Slider(0.1, 2.0, 1.0, label="Contraste"),
        gr.Slider(0, 10, 0, label="Desenfoque"),
        gr.Checkbox(label="Enfocar"),
        gr.Checkbox(label="Escala de grises")
    ],
    outputs="image",
    title="Editor de Imágenes Simple",
    description="Sube una imagen y ajusta los parámetros para editarla."
)

iface.launch()