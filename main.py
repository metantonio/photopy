import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from collections import deque

# Funciones de edición de imagen (sin cambios)
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
    return np.array(img.convert('RGB'))

def draw_on_image(image, x, y, brush_size, color):
    if image is None:
        return None
    img = Image.fromarray(image).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.ellipse([x-brush_size, y-brush_size, x+brush_size, y+brush_size], fill=tuple(color))
    return np.array(img)

# Historial de imágenes
image_history = deque(maxlen=10)

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

def update_image(image, brightness, contrast, blur, sharpen, gray):
    if image is not None:
        image_history.append(np.copy(image))
    return edit_image(image, brightness, contrast, blur, sharpen, gray)

def undo_changes():
    if len(image_history) > 0:
        return image_history.pop()
    else:
        return None

with gr.Blocks() as demo:
    gr.Markdown("# Editor de Imágenes Avanzado")
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Accordion("Ajustes de Imagen", open=False):
                brightness = gr.Slider(0.1, 2.0, 1.0, label="Brillo")
                contrast = gr.Slider(0.1, 2.0, 1.0, label="Contraste")
                blur = gr.Slider(0, 10, 0, label="Desenfoque")
                sharpen = gr.Checkbox(label="Enfocar")
                gray = gr.Checkbox(label="Escala de grises")
                apply_button = gr.Button("Aplicar Ajustes")
                undo_button = gr.Button("Deshacer")

            with gr.Accordion("Herramienta de Pincel", open=False):
                brush_size = gr.Slider(1, 50, 10, label="Tamaño del Pincel")
                color_picker = gr.ColorPicker(label="Color del Pincel")

        with gr.Column(scale=3):
            try:
                image_input = gr.Image(tool="sketch", type="numpy", label="Lienzo")
            except TypeError:
                image_input = gr.Image(type="numpy", label="Lienzo")
                gr.Markdown("Nota: La herramienta de dibujo no está disponible en esta versión de Gradio.")
    
    apply_button.click(
        update_image,
        inputs=[image_input, brightness, contrast, blur, sharpen, gray],
        outputs=image_input
    )

    undo_button.click(
        undo_changes,
        inputs=[],
        outputs=image_input
    )

    if hasattr(image_input, 'tool') and image_input.tool == "sketch":
        image_input.edit(
            draw_on_image,
            inputs=[image_input, brush_size, color_picker],
            outputs=image_input
        )

demo.launch()