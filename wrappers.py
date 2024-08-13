import tkinter as tk
from _tkinter import TclError
from tkinter import messagebox

import os
import sys

import config
from PIL import ImageTk


def resource_path(relative_path):
    # Получаем абсолютный путь к ресурсам
    try:
        # PyInstaller создает временную папку в _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Window(tk.Tk):
    __is_game_field = False
    __is_destroyed = False

    def __init__(self, is_game_field=False):
        self.__is_game_field = is_game_field
        super().__init__()
        self.__tune_window()
        self.update()

    def __tune_window(self):
        self.title("Морской Бой")
        self.tk.call("wm", "iconphoto", self._w, tk.PhotoImage(file=resource_path("src/main_icon.png")))
        img = ImageTk.PhotoImage(file=resource_path("src/main_icon.png"))
        self.wm_iconphoto(False, img)
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.call("wm", "attributes", ".", "-topmost", "1")
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        if self.__is_game_field:
            x = x - config.SIZE_OF_CELL * config.COLUMN
            y = y - config.SIZE_OF_CELL * config.ROW // 2
        self.wm_geometry("+%d+%d" % (x, y))
        self.resizable(width=False, height=False)  # don"t work on linux ubuntu

    def destroy(self):
        if not self.__is_destroyed:
            self.__is_destroyed = True
            super().destroy()

    def __on_closing(self):
        try:
            self.grab_set()
            if messagebox.askokcancel(title="Выход из игры", message="Хотите выйти из игры?"):
                self.destroy()
        except TclError:
            pass

    def is_destroyed(self):
        return self.__is_destroyed


if sys.platform.startswith("darwin"):
    constant_unnecessary_pixels = 6
    from tkmacosx import Button as OriginalButton
elif sys.platform.startswith("win"):
    constant_unnecessary_pixels = 4
    OriginalButton = tk.Button
else:
    constant_unnecessary_pixels = 2
    OriginalButton = tk.Button
    # tkinter displays slightly differently on different OS ))


class Button(OriginalButton):
    bindings = {
        "<Enter>": {"state": "active"},  # for Mouse focus
        "<Leave>": {"state": "normal"},
        "<Configure>": {"highlightbackground": "snow"}
    }
    if sys.platform.startswith("darwin"):
        bindings.update({"<Configure>": {"borderless": 1}})
    else:
        bindings.update({"<FocusIn>": {"default": "active"},  # for Keyboard focus
                         "<FocusOut>": {"default": "normal"}})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_responsive_button()

    def custom_responsive_button(self):
        # Set the bindings for the button instance
        for key, value in self.bindings.items():
            self.bind(key, lambda el, kwarg=value: el.widget.config(**kwarg))


class Canvas(tk.Canvas):
    def __init__(self, window, small_canvas):
        if small_canvas:
            width = config.COLUMN * config.SIZE_OF_CELL - 2
            height = config.ROW * config.SIZE_OF_CELL - 2
        else:
            width = (config.COLUMN * 2 + 1) * config.SIZE_OF_CELL - constant_unnecessary_pixels
            height = (config.ROW + 1) * config.SIZE_OF_CELL - constant_unnecessary_pixels

        super().__init__(window,
                         width=width,
                         height=height)
