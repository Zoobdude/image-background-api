import blurhash
from PIL import Image, ImageDraw
from Pylette import extract_colors, Palette
import numpy as np
from io import BytesIO
import requests

def download_image(url: str):
    response = requests.get(url)
    response.raise_for_status()
    
    image_data = response.content
    return image_data

def image_data_to_PIL_imagefile(image_data):
    return Image.open(BytesIO(image_data))


# Blur Hash Functions
def img_to_hash(image, x_components=4, y_components=3) -> str:
    hash: str =  blurhash.encode(image=image, x_components=x_components, y_components=y_components)

    return hash

def hash_to_img(hash: str, width=32, height=32) -> Image:
    image = blurhash.decode(hash, width, height)

    return image


# Colour palette Functions
def get_colour_palette(image_data, num_colours=10) -> Palette:
    palette = extract_colors(image_data, num_colours)
    return palette

def colour_palette_to_list(palette: Palette, format="rgb") -> list:
    match format:
        case "rgb":
            values_list = [c.rgb for c in palette.colors]
        
        case "hls":
            values_list = [c.hls for c in palette.colors]

        case "hsv":
            values_list = [c.hsv for c in palette.colors]

    return values_list  

def palette_to_image(palette: Palette, width=50, height=50) -> Image.Image:
    img = Image.new("RGB", size=(width * palette.number_of_colors, height))
    arr = np.asarray(img).copy()
    for i in range(palette.number_of_colors):
        c = palette.colors[i]
        arr[:, i * height : (i + 1) * height, :] = c.rgb
    img = Image.fromarray(arr, "RGB")
    return img


# Image resizing and background applying functions
def round_corners(image, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
    alpha = Image.new('L', image.size, 255)
    w, h = image.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    image.putalpha(alpha)
    return image

image_download = download_image("https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg")

image = round_corners(image_data_to_PIL_imagefile(image_download), 50)

image.save("image.png")