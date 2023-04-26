import tkinter as tk
import config
from PIL import ImageTk
from battlefield import Battlefield


class BattlefieldOpponent(Battlefield):
    __canvas = ["tk.Canvas()"]
    # what the player sees
    __buttons = []
    # for each cell we store 0 or its ship
    __field = []
    __image_hit = "image.png"
    __image_miss = "image.png"

    def __init__(self, real_field, canvas):
        super().__init__(real_field)
        self.__canvas = canvas
        for i in range(config.row):
            temp = []
            for j in range(config.column):
                btn = tk.Button(self.__canvas,
                                width=config.size_of_cell,
                                height=config.size_of_cell,
                                relief="groove")
                temp.append(btn)
            self.__buttons.append(temp)
        for i in range(config.row):
            for j in range(config.column):
                self.__buttons[i][j]["command"] = lambda x=i, y=j: self.__shot_and_update(
                    x, y)
        self.__image_hit = ImageTk.PhotoImage(file="hit.png")
        self.__image_miss = ImageTk.PhotoImage(file="water.png")

    def __update(self):
        for x in range(config.row):
            for y in range(config.column):
                if self._field[x][y] == "hit" and self.__buttons[x][y]["command"] != 0:
                    self.__buttons[x][y].config(bg="crimson",
                                                command=0,
                                                image=self.__image_hit,
                                                relief="flat")
                if self._field[x][y] == "miss" and self.__buttons[x][y]["command"] != 0:
                    self.__buttons[x][y].config(bg="light blue",
                                                command=0,
                                                image=self.__image_miss)

    def __shot_and_update(self, x, y):
        self._shot(x, y)
        self.__update()

    def __create_buttons(self):
        for i in range(config.row):
            for j in range(config.column):
                self.__buttons[i][j].pack(side="left",
                                          fill=None,
                                          expand=False)
                self.__canvas.create_window((j * config.size_of_cell, i * config.size_of_cell),
                                            anchor="nw",
                                            window=self.__buttons[i][j])

    def view(self):
        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.column + 1) * config.size_of_cell // 3,
                               height=config.size_of_cell,
                               bg="white")
        label_frame.pack_propagate(False)
        lbl = tk.Label(label_frame,
                       relief="solid",
                       font=("Comic Sans MS", 13, "bold"),
                       text="Чужое поле",
                       justify="center",
                       borderwidth=1)
        lbl.pack(fill="both", expand=True)
        self.__canvas.create_window((0, config.row * config.size_of_cell),
                                    anchor="nw",
                                    window=label_frame)
        self.__create_buttons()
