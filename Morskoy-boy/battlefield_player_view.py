import tkinter as tk
import config
from PIL import ImageTk
from battlefield import Battlefield


class BattlefieldPlayer(Battlefield):
    # what the opponent sees
    __canvas = ["tk.Canvas()"]
    __labels = []
    __image_cross = "image.png"
    __image_dot = "image.png"

    def __init__(self, real_field, canvas):
        super().__init__(real_field)
        self.__canvas = canvas
        for i in range(config.row):
            temp = [tk.Label(self.__canvas,
                             width=config.size_of_cell,
                             height=config.size_of_cell,
                             relief="flat",
                             bg="light gray")]
            for j in range(config.column):
                lbl = tk.Label(self.__canvas,
                               width=config.size_of_cell,
                               height=config.size_of_cell,
                               relief="groove",
                               bg="slateblue" if real_field[i][j] != 0 else "aqua")
                temp.append(lbl)
            self.__labels.append(temp)
        self.__image_cross = ImageTk.PhotoImage(file="cross.png")
        self.__image_dot = ImageTk.PhotoImage(file="dot.png")

    def __create_labels(self):
        for i in range(config.row):
            for j in range(config.column + 1):
                self.__labels[i][j].pack(expand=False, side="top")
                self.__canvas.create_window(
                    (j * config.size_of_cell + config.column *
                     config.size_of_cell, i * config.size_of_cell),
                    anchor="nw",
                    window=self.__labels[i][j])

    def view(self):
        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.column + 1) * config.size_of_cell // 3,
                               height=config.size_of_cell,
                               bg="white")
        label_frame.pack_propagate(False)
        lbl = tk.Label(label_frame,
                       relief="solid",
                       font=("Comic Sans MS", 13, "bold"),
                       text="Ваше поле",
                       justify="center",
                       borderwidth=1)
        lbl.pack(fill="both", expand=True)
        self.__canvas.create_window(((2 * config.column + 1) * config.size_of_cell -
                                     ((2 * config.column + 1) * config.size_of_cell // 3),
                                     config.row * config.size_of_cell),
                                    anchor="nw",
                                    window=label_frame)
        self.__create_labels()

    def update(self, x, y):
        self._existence_of_raw_shot = False
        self._shot(x, y)
        for x in range(config.row):
            for y in range(config.column):
                if self._field[x][y] == "hit" and self.__labels[x][y + 1]["image"] == "":
                    self.__labels[x][y + 1].config(image=self.__image_cross,
                                                   relief="flat")

                if self._field[x][y] == "miss" and self.__labels[x][y + 1]["image"] == "":
                    self.__labels[x][y + 1].config(image=self.__image_dot)
