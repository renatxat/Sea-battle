import tkinter as tk
from PIL import ImageTk

import config
from battlefield import Battlefield
from wrappers import resource_path


class BattlefieldPlayer(Battlefield):
    # what the player sees from the right
    __canvas = ["tk.Canvas()"]
    __labels = []
    __image_cross = "image.png"
    __image_dot = "image.png"

    def __init__(self, real_field, canvas):
        super().__init__(real_field)
        self.__canvas = canvas
        for i in range(config.ROW):
            temp = [tk.Label(self.__canvas,
                             width=config.SIZE_OF_CELL,
                             height=config.SIZE_OF_CELL,
                             relief="flat",
                             bg="light gray")]
            for j in range(config.COLUMN):
                lbl = tk.Label(self.__canvas,
                               width=config.SIZE_OF_CELL,
                               height=config.SIZE_OF_CELL,
                               relief="groove",
                               bg="slateblue" if real_field[i][j] != 0 else "aqua")
                temp.append(lbl)
            self.__labels.append(temp)
        self.__image_cross = ImageTk.PhotoImage(file=resource_path("src/cross.png"))
        self.__image_dot = ImageTk.PhotoImage(file=resource_path("src/dot.png"))

    def __create_labels(self):
        for i in range(config.ROW):
            for j in range(config.COLUMN + 1):
                self.__labels[i][j].pack(expand=False, side="top")
                self.__canvas.create_window(
                    (j * config.SIZE_OF_CELL + config.COLUMN *
                     config.SIZE_OF_CELL, i * config.SIZE_OF_CELL),
                    anchor="nw",
                    window=self.__labels[i][j])

    def view(self):
        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3,
                               height=config.SIZE_OF_CELL,
                               bg="white")
        label_frame.pack_propagate(False)
        lbl = tk.Label(label_frame,
                       relief="solid",
                       font=("Comic Sans MS", 13, "bold"),
                       text="Ваше поле",
                       justify="center",
                       borderwidth=1)
        lbl.pack(fill="both", expand=True)
        self.__canvas.create_window(((2 * config.COLUMN + 1) * config.SIZE_OF_CELL -
                                     ((2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3),
                                     config.ROW * config.SIZE_OF_CELL),
                                    anchor="nw",
                                    window=label_frame)
        self.__create_labels()

    def update(self, x, y):
        self._existence_of_raw_shot = False
        self._shot(x, y)
        for x in range(config.COLUMN):
            for y in range(config.ROW):
                if self._field[y][x] == "hit" and self.__labels[y][x + 1]["image"] == "":  # last move
                    self.__labels[y][x + 1].config(image=self.__image_cross,
                                                   relief="flat",
                                                   bg="orange")
                elif self._field[y][x] == "hit" and self.__labels[y][x + 1]["image"] != "":
                    self.__labels[y][x + 1].config(bg="slateblue")
                if self._field[y][x] == "miss" and self.__labels[y][x + 1]["image"] == "":
                    self.__labels[y][x + 1].config(image=self.__image_dot,
                                                   bg="limegreen")
                elif self._field[y][x] == "miss" and self.__labels[y][x + 1]["image"] != "":  # last move
                    self.__labels[y][x + 1].config(bg="aqua")
