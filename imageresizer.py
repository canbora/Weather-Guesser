#!/usr/bin/env python3
from PIL import Image
import os
import numpy as np
import random

weather_types = ["dew", "fogsmog", "frost", "glaze", "hail", "lightning", "rain", "rainbow", "rime", "sandstorm", "snow"]


def get_single_image_data(path, side):
    im = Image.open(path)

    # Crop the longer side
    width, height = im.size
    if width <= height:
        im = im.crop((0, (height - width)//2, width, (height + width)//2))
    else:
        im = im.crop(((width - height)//2, 0, (width + height)//2, height))

    im = im.resize((side, side))
    im = im.convert("RGB")
    imdata = np.asarray(im)
    return imdata

"""
Resizes all images in the database to a side x side square by cropping the ends of the longer side and scaling.
Formats the resulting images, and the corresponding weathers, as two numpy arrays.
Saves them in images.npz.
"""
def resize_images(side):
    file_path = os.path.dirname(os.path.realpath(__file__))
    # Each element is of the form (image, weather_index)
    images = []
    for weather_index, weather_name in enumerate(weather_types):
        for file in os.scandir(f"{file_path}/dataset/{weather_name}"):
            imdata = get_single_image_data(file.path, side)
            images.append((imdata, weather_index))
    random.shuffle(images)
    np.savez("images.npz", images=np.array([item[0] for item in images]), weather=np.array([item[1] for item in images]))


if __name__ == "__main__":
    side = "None"
    while not side.isdigit():
        side = input("Resim kenarı kaç pixel olsun? : ")
    resize_images(int(side))