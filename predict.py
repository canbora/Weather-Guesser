#!/usr/bin/env python3
import keras
from imageresizer import get_single_image_data, weather_types
import numpy as np

def predict(filename=None, model=None):

    if model is None:
        model = keras.saving.load_model("trained_model.keras")
    if filename is None:
        filename = input("Enter file path: ")
    imdata = get_single_image_data(filename, 124)[np.newaxis]
    results = model(imdata)[0]
    category_results = list(zip(results, weather_types))
    category_results.sort(reverse=True)
    print("Possibilities for each category:")
    for result, category in category_results:
        print(f"{category}: {result:.3f}")
    return category_results


if __name__ == '__main__':
    predict()