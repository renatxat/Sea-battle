from battlefield_player_view import BattlefieldPlayer
from battlefield_bot_view import BattlefieldBotOpponent
from battlefield_bot import BattlefieldBotPlayer
import config

import tkinter as tk
from tkinter import messagebox
from sys import platform


class Application:
    __window = ["tk.Tk()"]
    __canvas = ["tk.Canvas()"]

    __field = ["BattlefieldPlayer_1"]
    __foreign_field = ["BattlefieldOpponent_1"]

    __label_turn = ["tk.Label()"]

    def __init__(self, window, real_field, is_my_first_move, is_game_bot):
        self.constructor_field = real_field
        self.__window = window
        if is_game_bot:
            self.__create_board()
            self.__draw_boards(is_my_first_move)
            self.__tune_window()

    def __create_board(self):
        if platform.startswith('win'):
            resizing_constant = 4
        else:
            resizing_constant = 2
        self.__canvas = tk.Canvas(self.__window,
                                  width=(config.column * 2 + 1) * config.size_of_cell - resizing_constant,
                                  height=(config.row + 1) * config.size_of_cell - resizing_constant)
        self.__foreign_field = BattlefieldBotOpponent(self.__canvas)
        real_field = self.constructor_field
        self.__field = BattlefieldPlayer(real_field, self.__canvas)
        self.__bot_field = BattlefieldBotPlayer(real_field)

    def __draw_boards(self, my_first_move):
        self.__field.view()
        self.__foreign_field.view()
        label_frame = tk.Frame(self.__canvas,
                               width=(2 * config.column + 1) * config.size_of_cell - 2 * (
                                       (2 * config.column + 1) * config.size_of_cell // 3),
                               height=config.size_of_cell,
                               bg="white")
        label_frame.pack_propagate(False)
        self.__label_turn = tk.Label(label_frame,
                                     relief="solid",
                                     font=("Comic Sans MS", 13, "bold"),
                                     text="Ваш ход",
                                     fg="lime",
                                     justify="center",
                                     borderwidth=1)
        if not my_first_move:
            self.__label_turn.configure(text="Ход противника", fg="red")
            self.__bot_field.take_a_shot()

        self.__label_turn.pack(fill="both", expand=True)
        self.__canvas.create_window(((2 * config.column + 1) * config.size_of_cell // 3,
                                     config.row * config.size_of_cell),
                                    anchor="nw",
                                    window=label_frame)
        self.__canvas.pack()

    def __tune_window(self):
        self.__window.resizable(width=False, height=False)
        self.__window.title("Морской Бой")
        self.__window.tk.call("wm", "iconphoto", self.__window._w, tk.PhotoImage(file="main_icon.png"))
        self.__window.protocol("WM_DELETE_self.window", self.__on_closing)
        self.__window.after_idle(self.__loop, 0)  # start endless __loop
        x = (self.__window.winfo_screenwidth() -
             self.__window.winfo_reqwidth()) / 2
        y = (self.__window.winfo_screenheight() -
             self.__window.winfo_reqheight()) / 2
        self.__window.wm_geometry(
            "+%d+%d" % (x - config.size_of_cell * config.column, y - config.size_of_cell * config.row // 2))
        self.__window.mainloop()

    def __on_closing(self):
        if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
            self.__window.destroy()

    def __loop(self, n):
        if self.__foreign_field.presence_of_changes() and self.__label_turn["fg"] == "lime":
            self.__foreign_field.get_last_shot()
            if not self.__foreign_field.existence_hit_last_shot():
                self.__label_turn.configure(text="Ход противника", fg="red")
                self.__bot_field.take_a_shot()

        elif self.__bot_field.presence_of_changes() and self.__label_turn["fg"] == "red":
            self.__window.update()
            self.__canvas.after(800)
            self.__field.update(*self.__bot_field.get_last_shot())
            if not self.__bot_field.existence_hit_last_shot():
                self.__foreign_field.existence_hit_last_shot()
                self.__label_turn.configure(text="Ваш ход", fg="lime")
            else:
                self.__bot_field.take_a_shot()
        if self.__foreign_field.get_run() and self.__bot_field.get_run():
            # endless __loop with delay
            self.__window.after(1, self.__loop, n + 1)
        elif self.__bot_field.get_run():
            if messagebox.showinfo(title="Чел, хорош!", message="Вы победили!"):
                self.__window.destroy()
        else:
            self.__field.update(*self.__bot_field.get_last_shot())
            if messagebox.showinfo(title="Трансорфмеры, общий сбор на НК", message="Восстание машин началось"):
                self.__window.destroy()
