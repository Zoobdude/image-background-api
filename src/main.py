from fastapi import FastAPI
from typing import Union, Annotated
from enum import Enum

class Tags(Enum):
    blur_hash = "Blur Hash"
    colour_palette = "Colour palette"
    image_processing = "Image Processing"

app = FastAPI(docs_url="/")

class ColourPaletteFormats(str, Enum):
    rgb = "rgb"
    hls = "hls"
    hsv = "hsv"


@app.get("/blurhash/encode", tags=[Tags.blur_hash])
def encode_image_into_blurhash(img_url: str):
    pass

@app.get("/blurhash/decode", tags=[Tags.blur_hash])
def decode_blurhash_into_PNG(hash: str):
    pass

@app.get("/colour-palette", tags=[Tags.colour_palette])
def get_image_colour_palette(img_url: str, num_colours: int, format: ColourPaletteFormats):
    pass

@app.get("/colour-palette/image", tags=[Tags.colour_palette])
def get_colour_palette_as_image(img_url: str, num_colours: int, width: int, height: int):
    pass

