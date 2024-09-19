#!/usr/bin/env python3
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from predict import predict
from trainer import train_model
import threading

class ButtonsFrame(ttk.Frame):

    def __init__(self, parent, button_infos, lang="TR"):
        super().__init__(parent)
        self.buttons = []
        self.button_infos = button_infos

        for (names, func) in button_infos:
            button = ttk.Button(self, text=names[lang], padding=10)
            def callback(button=button, func=func):
                def altered_func():
                    button.state(["disabled"])
                    func()
                    button.state(["!disabled"])
                thread = threading.Thread(target=altered_func)
                thread.start()
            button["command"] = callback
            self.buttons.append(button)
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def change_lang(self, lang):
        self.lang = lang
        for i, info in enumerate(self.button_infos):
            self.buttons[i]["text"] = info[0][lang]


class ResultsFrame(ttk.Frame):

    labels = {
        "EN": {
            "dew": "Dew",
            "fogsmog": "Fog/smog",
            "frost": "Frost",
            "glaze": "Glaze",
            "hail": "Hail",
            "lightning": "Lightning",
            "rain": "Rain",
            "rainbow": "Rainbow",
            "rime": "Rime",
            "sandstorm": "Sandstorm",
            "snow": "Snow",
            "category": "Weather",
            "probability": "Probability"
        }, "TR": {
            "dew": "Çiy",
            "fogsmog": "Sis/pus",
            "frost": "Kırağı",
            "glaze": "Buzlu",
            "hail": "Dolu",
            "lightning": "Şimşek",
            "rain": "Yağmur",
            "rainbow": "Gökkuşağı",
            "rime": "Don",
            "sandstorm": "Kum fırtınası",
            "snow": "Kar",
            "category": "Hava Durumu",
            "probability": "İhtimal"
        }
    }

    def __init__(self, parent, lang="TR"):
        super().__init__(parent)
        self.lang = lang

        self.frame_image = ttk.Frame(self, width=250, height=250)
        self.frame_image.pack_propagate(0)
        self.frame_image.pack(side=tk.LEFT, padx=20, pady=20)
        self.label_image = ttk.Label(self.frame_image)
        self.label_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.table_results = ttk.Treeview(self, show="headings", columns=("category", "probability"), height=11)
        self.table_results.column("category", width=100)
        self.table_results.column("probability", width=100)
        self.table_results.heading("category", text=self.labels[self.lang]["category"])
        self.table_results.heading("probability", text=self.labels[self.lang]["probability"])
        self.table_results.pack(side=tk.RIGHT, padx=20, pady=20)
        self.results = []

    def update(self, image_filename=None, results=None):
        if image_filename is not None:
            image = Image.open(image_filename)
            image.thumbnail((250, 250))
            self.tk_image = ImageTk.PhotoImage(image)
            self.label_image.config(image=self.tk_image)
        if results is not None:
            self.results = results
        self.table_results.delete(*self.table_results.get_children())
        for (result, category) in self.results:
            self.table_results.insert("", "end", values=(self.labels[self.lang][category], f"{result:.3f}"))

    def change_lang(self, lang):
        self.lang = lang
        self.table_results.heading("category", text=self.labels[self.lang]["category"])
        self.table_results.heading("probability", text=self.labels[self.lang]["probability"])
        self.update()



class Window(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title("Weather Guesser")

        self.lang = "TR"

        self.invert_lang = {"TR": "EN", "EN": "TR"}

        self.buttons = [
            [{"TR": "English", "EN": "Türkçe"}, self.change_lang],
            [{"TR": "Resim yükle", "EN": "Test an Image"}, self.load_image],
            [{"TR": "Modeli eğit ve ayarla", "EN": "Tune and train model"}, lambda: train_model(tune_again=True)],
            [{"TR": "Modeli eğit", "EN": "Train model"}, lambda: train_model(tune_again=False)]
        ]

        self.buttons_frame = ButtonsFrame(self, self.buttons)
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

    def change_lang(self):
        self.lang = self.invert_lang[self.lang]
        self.buttons_frame.change_lang(self.lang)
        self.results_frame.change_lang(self.lang)



window = Window()
window.mainloop()