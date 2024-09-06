#!/usr/bin/env python3
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from predict import predict

# Functions

def load_image():
    global selected_image
    image_filename = filedialog.askopenfilename(multiple=False)
    results = predict(image_filename)
    image = Image.open(image_filename)
    image.thumbnail((250, 250))
    selected_image = ImageTk.PhotoImage(image)
    formatted_results = "\n".join(f"    {category}: {result:.3f}" for result, category in results)
    label_image.config(text=formatted_results, image=selected_image)


# Window creation and geometry

window = tk.Tk()
window.title("Weather Guesser")

## Center window
width = 500
height = 360
offset_x = (window.winfo_screenwidth()-width)//2
offset_y = (window.winfo_screenheight()-height)//2
window.geometry(f"{width}x{height}+{offset_x}+{offset_y}")

# Widgets

button_load_image = ttk.Button(window, text="Test an Image", command=load_image, padding=10)
button_load_image.pack(padx=10, pady=10)
selected_image = None
label_image = ttk.Label(window, text="", compound="left", font=("Cambria", 12), padding=10)
label_image.pack(padx=10, pady=10)

window.mainloop()