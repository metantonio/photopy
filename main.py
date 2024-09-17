import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from collections import deque
from functions.image_conversion import convert_image_format, load_image, open_folder
from functions.image_resize import resize_image

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

def convert_image_and_notify(image, target_format):
    try:
        converted_image_path = convert_image_format(image, target_format)
        return f"Image successfully converted and saved at: {converted_image_path}"
    except Exception as e:
        return str(e)
    
def resize_image_and_notify(image, width, height):
    try:
        resized_image = resize_image(image, width, height)
        return resized_image, f"Image successfully resized to {width}x{height} pixels."
    except Exception as e:
        return image, str(e)

def handle_open_folder():
    open_folder()

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

            """ with gr.Accordion("Herramienta de Pincel", open=False):
                brush_size = gr.Slider(1, 50, 10, label="Tamaño del Pincel")
                color_picker = gr.ColorPicker(label="Color del Pincel") """

            with gr.Accordion("Convertir Imagen", open=False):
                target_format = gr.Dropdown(["JPEG", "PNG", "BMP", "GIF"], label="Formato de Destino")
                convert_button = gr.Button("Convertir")
                conversion_message = gr.Textbox(label="Mensaje de Conversión", interactive=False)

            with gr.Accordion("Redimensionar Imagen", open=False):
                width = gr.Number(label="Ancho en píxeles", value=100)
                height = gr.Number(label="Alto en píxeles", value=100)
                resize_button = gr.Button("Redimensionar")
                resize_message = gr.Textbox(label="Mensaje de Redimensionamiento", interactive=False)

            #save_path = gr.Textbox(label="Save Path")
            open_folder_button = gr.Button("Open Folder")


        with gr.Column(scale=3):
            try:
                image_input = gr.Image(tool="sketch", type="numpy", label="Lienzo")
            except TypeError:
                image_input = gr.Image(type="numpy", label="Lienzo")
                #gr.Markdown("Nota: La herramienta de dibujo no está disponible en esta versión de Gradio.")
            gr.Markdown("Note: Tool created by Antonio Martínez @metantonio")
    
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

    convert_button.click(
        convert_image_and_notify,
        inputs=[image_input, target_format],
        outputs=conversion_message
    )

    resize_button.click(
        resize_image_and_notify,
        inputs=[image_input, width, height],
        outputs=[image_input, resize_message]
    )

    open_folder_button.click(
        handle_open_folder,
        inputs=[],
        outputs=None
    )

    if hasattr(image_input, 'tool') and image_input.tool == "sketch":
        image_input.edit(
            draw_on_image,
            inputs=[image_input, brush_size, color_picker],
            outputs=image_input
        )

if __name__ == "main":
    demo.launch()
