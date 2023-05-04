import tkinter as tk
from _tkinter import TclError
from tkinter import messagebox

import config
from PIL import ImageTk


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
        # self.tk.call("wm", "iconphoto", self._w, tk.PhotoImage(file="main_icon.png"))
        img = ImageTk.PhotoImage(file="src/main_icon.png")
        self.wm_iconphoto(False, img)
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.call('wm', 'attributes', '.', '-topmost', '1')
        x = (self.winfo_screenwidth() -
             self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() -
             self.winfo_reqheight()) / 2
        if self.__is_game_field:
            x = x - config.SIZE_OF_CELL * config.COLUMN
            y = y - config.SIZE_OF_CELL * config.ROW // 2
        self.wm_geometry("+%d+%d" % (x, y))
        self.resizable(width=False, height=False)  # don't work on linux ubuntu

    def destroy(self):
        if not self.__is_destroyed:
            super().destroy()
            self.__is_destroyed = True

    def __on_closing(self):
        try:
            self.grab_set()
            if messagebox.askokcancel(title="Выход из игры", message="Хотите выйти из игры?"):
                self.destroy()
        except TclError:
            pass

    def is_destroyed(self):
        return self.__is_destroyed
