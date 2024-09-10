#!/usr/bin/env python3
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from predict import predict

class ResultsFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.label_image = ttk.Label(self, font=("Cambria", 12))
        self.label_image.pack(side=tk.LEFT, padx=20, pady=20, expand=True)

        self.table_results = ttk.Treeview(self, show="", columns=("category", "probability"), height=11)
        self.table_results.heading("category", text="Weather")
        self.table_results.heading("probability", text="Probability")
        self.table_results.pack(side=tk.LEFT, padx=20, pady=20, expand=True)

    def update(self, image_filename, results):
        image = Image.open(image_filename)
        image.thumbnail((250, 250))
        self.tk_image = ImageTk.PhotoImage(image)
        self.table_results.config(show="headings")
        self.table_results.delete(*self.table_results.get_children())
        for (result, category) in results:
            self.table_results.insert("", "end", values=(category, f"{result:.3f}"))
        self.label_image.config(image=self.tk_image)


class Window(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title("Weather Guesser")

        ## Center window
        width = 540
        height = 360
        offset_x = (self.winfo_screenwidth()-width)//2
        offset_y = (self.winfo_screenheight()-height)//2
        self.geometry(f"{width}x{height}+{offset_x}+{offset_y}")

        # Widgets
        self.button_load_image = ttk.Button(self, text="Test an Image", command=self.load_image, padding=10)
        self.button_load_image.pack(padx=10, pady=10)

        self.results_frame = ResultsFrame(self)
        self.results_frame.pack()

    def load_image(self):
        image_filename = filedialog.askopenfilename(multiple=False)
        results = predict(image_filename)
        self.results_frame.update(image_filename, results)


window = Window()
window.mainloop()