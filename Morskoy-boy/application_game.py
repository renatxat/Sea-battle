from battlefield_player_view import BattlefieldPlayer
from battlefield_bot_view import BattlefieldBotOpponent
from battlefield_bot import BattlefieldBotPlayer

import tkinter as tk
from tkinter import messagebox
import config


class Application:
    __window = ["tk.Tk()"]
    __canvas = ["tk.Canvas()"]

    __field = ["BattlefieldPlayer_1"]
    __foreign_field = ["BattlefieldOpponent_1"]

    __label_turn = ["tk.Label()"]

    def __init__(self, window, real_field):
        self.constructor_field = real_field
        self.__window = window
        self.__create_board()
        self.__draw_boards()
        self.__tune_window()

    def __create_board(self):
        self.__canvas = tk.Canvas(self.__window,
                                  width=(config.column * 2 + 1) * config.size_of_cell,
                                  height=(config.row + 1) * config.size_of_cell - 2)
        self.__foreign_field = BattlefieldBotOpponent(self.__canvas)
        real_field = self.constructor_field
        self.__field = BattlefieldPlayer(real_field, self.__canvas)
        self.__bot_field = BattlefieldBotPlayer(real_field)

    def __draw_boards(self):
        self.__field.view()
        self.__foreign_field.view()
        self.__label_turn = tk.Label(self.__canvas,
                                     font=("Comic Sans MS", 15, "bold"),
                                     text="<--- Ходите ", fg="lime",
                                     borderwidth=1, relief="solid")
        self.__label_turn.pack(fill="both", anchor="s")
        self.__canvas.create_window(((config.column - 2) * config.size_of_cell - 10,
                                     config.row * config.size_of_cell),
                                    anchor="nw", window=self.__label_turn)
        self.__canvas.pack()

    def __tune_window(self):
        self.__window.resizable(width=False, height=False)
        self.__window.title("Морской Бой")
        self.__window.tk.call("wm", "iconphoto", self.__window._w, tk.PhotoImage(file="main_icon.png"))
        self.__window.protocol("WM_DELETE_self.window", self.__on_closing)
        self.__window.after_idle(self.__loop, 0)  # start endless __loop
        self.__window.mainloop()

    def __on_closing(self):
        if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
            self.__window.destroy()

    def __loop(self, n):
        if self.__foreign_field.presence_of_changes() and self.__label_turn["fg"] == "lime":
            self.__foreign_field.get_last_shot()
            if not self.__foreign_field.exist_hit_last_shot():
                self.__label_turn.configure(text=" Ход противника-->", fg="red")
                self.__bot_field.take_a_shot()

        elif self.__bot_field.presence_of_changes() and self.__label_turn["fg"] == "red":
            self.__window.update()
            self.__canvas.after(800)
            self.__field.update(*self.__bot_field.get_last_shot())
            if not self.__bot_field.exist_hit_last_shot():
                self.__foreign_field.exist_hit_last_shot()
                self.__label_turn.configure(text="<--- Ходите ", fg="lime")
            else:
                self.__bot_field.take_a_shot()
        if self.__foreign_field.get_run() and self.__bot_field.get_run():
            self.__window.after(1, self.__loop, n + 1)  # endless __loop with delay
        elif self.__bot_field.get_run():
            if messagebox.showinfo(title="Чел, хорош!", message="Вы победили!"):
                self.__window.destroy()
        else:
            self.__bot_field.take_a_shot()
            self.__field.update(*self.__bot_field.get_last_shot())
            if messagebox.showinfo(title="Трансорфмеры, общий сбор на НК", message="Восстание машин началось"):
                self.__window.destroy()

# oval = self.canvas.create_oval(0, 0, 100, 100, fill="white")
# def move_oval(event):
#     self.canvas.coords(oval, event.x - 30, event.y - 30, event.x + 30, event.y + 30)
# self.canvas.tag_bind(oval, "<B1-Motion>", lambda: move_oval)
