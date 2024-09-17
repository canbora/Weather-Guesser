#!/usr/bin/env python3
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from predict import predict
from trainer import train_model
import threading

class ButtonsFrame(ttk.Frame):

    def __init__(self, parent, button_infos):
        super().__init__(parent)
        self.buttons = []

        for (name, func) in button_infos:
            button = ttk.Button(self, text=name, padding=10)
            def callback(button=button, func=func):
                def altered_func():
                    button.state(["disabled"])
                    func()
                    button.state(["!disabled"])
                thread = threading.Thread(target=altered_func)
                thread.start()
            button.config(command=callback)
            self.buttons.append(button)
            button.pack(side=tk.LEFT, padx=10, pady=10)

class ResultsFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.frame_image = ttk.Frame(self, width=250, height=250)
        self.frame_image.pack_propagate(0)
        self.frame_image.pack(side=tk.LEFT, padx=20, pady=20)
        self.label_image = ttk.Label(self.frame_image)
        self.label_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.table_results = ttk.Treeview(self, show="headings", columns=("category", "probability"), height=11)
        self.table_results.column("category", width=100)
        self.table_results.column("probability", width=100)
        self.table_results.heading("category", text="Weather")
        self.table_results.heading("probability", text="Probability")
        self.table_results.pack(side=tk.RIGHT, padx=20, pady=20)

    def update(self, image_filename, results):
        image = Image.open(image_filename)
        image.thumbnail((250, 250))
        self.tk_image = ImageTk.PhotoImage(image)
        self.table_results.delete(*self.table_results.get_children())
        for (result, category) in results:
            self.table_results.insert("", "end", values=(category, f"{result:.3f}"))
        self.label_image.config(image=self.tk_image)


class Window(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title("Weather Guesser")

        # Top buttons
        buttons = [
            ("Test an Image", self.load_image),
            ("Tune and train model", lambda: train_model(tune_again=True)),
            ("Retrain model with current hyperparams", lambda: train_model(tune_again=False))
        ]
        self.buttons_frame = ButtonsFrame(self, buttons)
        self.buttons_frame.pack(padx=10, pady=10)

        self.results_frame = ResultsFrame(self)
        self.results_frame.pack()

        ## Center window
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        offset_x = (self.winfo_screenwidth()-width)//2
        offset_y = (self.winfo_screenheight()-height)//2
        self.geometry(f"{width}x{height}+{offset_x}+{offset_y}")

    def load_image(self):
        image_filename = filedialog.askopenfilename(multiple=False)
        results = predict(image_filename)
        self.results_frame.update(image_filename, results)


window = Window()
window.mainloop()