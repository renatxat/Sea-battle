import tkinter as tk
from PIL import ImageTk

import config
from wrappers import Button
from battlefield import Battlefield
from wrappers import resource_path


class BattlefieldOpponent(Battlefield):
    """what the player sees from the left"""
    __canvas = ["Canvas()"]
    __buttons = []
    # for each cell we store 0 or its ship
    __image_hit = "image.png"
    __image_miss = "image.png"

    __quantity_call_let_me_move = 0

    def __init__(self, real_field, canvas):
        super().__init__(real_field)
        self.__canvas = canvas
        for i in range(config.ROW):
            temp = []
            for j in range(config.COLUMN):
                btn = Button(self.__canvas,
                             width=config.SIZE_OF_CELL,
                             height=config.SIZE_OF_CELL,
                             borderwidth=1,
                             bg="floral white",
                             activebackground="papaya whip")
                temp.append(btn)
            self.__buttons.append(temp)
        for i in range(config.ROW):
            for j in range(config.COLUMN):
                self.__buttons[i][j]["command"] = lambda x=j, y=i: self.__shot_and_update(x, y)
        self.__image_hit = ImageTk.PhotoImage(file=resource_path("src/hit.png"))
        self.__image_miss = ImageTk.PhotoImage(file=resource_path("src/water.png"))

    def __update(self):
        for x in range(config.COLUMN):
            for y in range(config.ROW):
                if self._field[y][x] == "hit" and self.__buttons[y][x]["command"] != 0:
                    self.__buttons[y][x].config(command=0,
                                                image=self.__image_hit,
                                                relief="flat",
                                                bg="crimson",
                                                activebackground="crimson")
                if self._field[y][x] == "miss" and self.__buttons[y][x]["command"] != 0:
                    self.__buttons[y][x].config(command=0,
                                                image=self.__image_miss,
                                                relief="flat",
                                                bg="light blue",
                                                activebackground="light blue")

    def __shot_and_update(self, x, y):
        if self.__quantity_call_let_me_move:
            self._shot(x, y)
            self.__update()

    def __create_buttons(self):
        for i in range(config.ROW):
            for j in range(config.COLUMN):
                self.__buttons[i][j].pack(side="bottom",
                                          fill=None,
                                          expand=False)
                self.__canvas.create_window((j * config.SIZE_OF_CELL, i * config.SIZE_OF_CELL),
                                            anchor="nw",
                                            window=self.__buttons[i][j])

    def view(self):
        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3,
                               height=config.SIZE_OF_CELL,
                               bg="white")
        label_frame.pack_propagate(False)
        lbl = tk.Label(label_frame,
                       relief="solid",
                       font=("Comic Sans MS", 13, "bold"),
                       text="Чужое поле",
                       justify="center",
                       borderwidth=1)
        lbl.pack(fill="both", expand=True)
        self.__canvas.create_window((0, config.ROW * config.SIZE_OF_CELL),
                                    anchor="nw",
                                    window=label_frame)
        self.__create_buttons()

    def let_me_move(self):
        if not self.__quantity_call_let_me_move:
            self._existence_of_raw_shot = False
        self.__quantity_call_let_me_move += 1
