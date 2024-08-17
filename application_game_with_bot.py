import tkinter as tk
from tkinter import messagebox

import config
from battlefield_bot import BattlefieldBotPlayer
from battlefield_player_view import BattlefieldPlayer
from battlefield_opponent_view import BattlefieldOpponent
from constructor_fields import ConstructorFields
from wrappers import Window
from wrappers import Canvas


class Application:
    __window = ["Window()"]
    __canvas = ["Canvas()"]

    __field = ["BattlefieldPlayer"]
    __foreign_field = ["BattlefieldBotOpponent"]
    __bot_field = ["BattlefieldBotPlayer"]

    __label_turn = ["tk.Label()"]
    __is_closing = False

    def __init__(self, is_need_for_randomness, is_my_first_move):
        self.__create_board(is_need_for_randomness)
        self.__draw_boards(is_my_first_move)
        self.__start_loops()

    def __create_board(self, is_need_for_randomness):
        constructor_field = ConstructorFields(is_need_for_randomness=is_need_for_randomness)
        constructor_field = constructor_field.get()
        if not constructor_field:
            self.__is_closing = True
            return
        self.__window = Window(is_game_field=True)
        self.__canvas = Canvas(self.__window, number_of_fields=2)
        # the order in which the fields are created is very important
        # it has to do with filling the canvas with buttons
        auto_field = ConstructorFields(is_need_for_randomness=True)
        self.__foreign_field = BattlefieldOpponent(real_field=auto_field.get(), canvas=self.__canvas)
        self.__field = BattlefieldPlayer(constructor_field, self.__canvas)
        self.__bot_field = BattlefieldBotPlayer(constructor_field)

    def __draw_boards(self, my_first_move):
        if self.__is_closing:
            return

        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3,
                               height=config.SIZE_OF_CELL,
                               bg="white")
        label_frame.pack_propagate(False)
        self.__label_turn = tk.Label(label_frame,
                                     relief="solid",
                                     font=("Comic Sans MS", 13, "bold"),
                                     text="Ваш ход",
                                     fg="green2",
                                     justify="center",
                                     borderwidth=1)
        if my_first_move:
            self.__foreign_field.let_me_move()
        else:
            self.__label_turn.configure(text="Ход противника", fg="red")
            self.__bot_field.take_a_shot()
        self.__label_turn.pack(fill="both", expand=True)
        self.__canvas.create_window(
            ((2 * config.COLUMN + 1) * config.SIZE_OF_CELL // 3,
             config.ROW * config.SIZE_OF_CELL),
            anchor="nw",
            window=label_frame)
        self.__foreign_field.view()
        self.__field.view()
        self.__window.resizable(width=False, height=False)
        self.__canvas.pack(fill="both", expand=True)

    def __start_loops(self):
        if self.__is_closing:
            return
        self.__window.after_idle(self.__loop, 0)  # start endless __loop
        self.__window.mainloop()

    def __loop(self, n):
        if self.__is_closing or self.__window.is_destroyed():
            return
        self.__click_processing()
        self.__check_game_over(n)

    def __click_processing(self):
        if self.__foreign_field.get_changes() and self.__label_turn["fg"] == "green2":
            if not self.__foreign_field.existence_hit_last_shot():
                self.__label_turn.configure(text="Ход противника", fg="red")
                self.__bot_field.take_a_shot()
        elif self.__bot_field.get_changes() and self.__label_turn["fg"] == "red":
            # objects in the tkinter can update more slowly than this cycle, so:
            self.__window.update()
            self.__canvas.after(config.TIME_WAITING_BOT_MOVE)
            self.__field.update(*self.__bot_field.get_last_shot())
            if not self.__bot_field.existence_hit_last_shot():
                self.__foreign_field.existence_hit_last_shot()
                self.__foreign_field.let_me_move()
                self.__label_turn.configure(text="Ваш ход", fg="green2")
            else:
                self.__bot_field.take_a_shot()

    def __check_game_over(self, n):
        if self.__foreign_field.get_run() and self.__bot_field.get_run():
            self.__window.after(1, self.__loop, n + 1)  # endless cycle!
        elif self.__bot_field.get_run():
            if messagebox.showinfo(title="Чел, хорош!",
                                   message="Вы победили!",
                                   parent=self.__window):
                self.__window.destroy()
        else:
            self.__field.update(*self.__bot_field.get_last_shot())
            if messagebox.showinfo(title="Трансформеры, общий сбор на НК",
                                   message="Восстание машин началось",
                                   parent=self.__window):
                self.__window.destroy()
